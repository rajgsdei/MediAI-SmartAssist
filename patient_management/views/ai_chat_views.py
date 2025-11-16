from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
try:
    from transformers import pipeline
except Exception:
    pipeline = None

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None
from patient_management.models.appointment_model import Appointment
from patient_management.models.auth_user_model import MediAIUser
from patient_management.models.patient_model import Patient
from patient_management.models.medication_model import Medication
from patient_management.models.allergy_model import Allergy
from datetime import datetime
import re

# Attempt to load NLP models once at module level. If any model fails to load
# (missing packages, native build issues, or download problems), catch the
# exception, log a warning, and set the variables to None so the app can start.
sentence_model = None
intent_classifier = None
chatbot = None
nlp = None
try:
    if SentenceTransformer is not None:
        sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    else:
        sentence_model = None
except Exception as e:
    print("[ai_chat_views] Warning: SentenceTransformer failed to load:", e)
try:
    if pipeline is not None:
        intent_classifier = pipeline("zero-shot-classification", model="distilbert-base-uncased")
    else:
        intent_classifier = None
except Exception as e:
    print("[ai_chat_views] Warning: zero-shot intent classifier failed to load:", e)
try:
    if pipeline is not None:
        chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium", tokenizer="microsoft/DialoGPT-medium")
    else:
        chatbot = None
except Exception as e:
    print("[ai_chat_views] Warning: DialoGPT chatbot pipeline failed to load:", e)
# Note: spaCy nlp is optional here. If you need it, install spaCy and load
# en_core_web_sm in this try/except block (kept as None if unavailable).
try:
    import spacy
    try:
        nlp = spacy.load('en_core_web_sm')
    except Exception:
        # spaCy model not present
        nlp = None
except Exception:
    nlp = None

INTENT_LABELS = [
    "list_appointments", "list_medications", "list_doctors", "list_allergies", "patient_allergies"
]


class AIChatView(View):
    def get(self, request):
        return render(request, 'ai_chat/chat_window.html')

    def post(self, request):
        user_message = request.POST.get('message', '').strip()
        if not user_message:
            return JsonResponse({'success': False, 'error': 'Message cannot be empty.'})

        try:
            # 1. Intent classification (use ML model if available, otherwise simple keyword fallback)
            if intent_classifier is not None:
                intent_result = intent_classifier(user_message, INTENT_LABELS)
                intent = intent_result['labels'][0]
            else:
                lower = user_message.lower()
                if any(w in lower for w in ['appointment', 'schedule', 'visit']):
                    intent = 'list_appointments'
                elif any(w in lower for w in ['medication', 'drug', 'prescription']):
                    intent = 'list_medications'
                elif any(w in lower for w in ['doctor', 'physician']):
                    intent = 'list_doctors'
                elif 'allergy' in lower:
                    intent = 'list_allergies'
                elif 'patient' in lower:
                    intent = 'patient_allergies'
                else:
                    intent = 'fallback'

            # 2. Entity extraction (very basic): use spaCy if available, otherwise fall back to regex heuristics
            entities = {
                "patient": None,
                "doctor": None,
                "date": None,
                "allergy": None,
                "medication": None
            }
            if nlp is not None:
                doc = nlp(user_message)
                # Extract patient/doctor names (PERSON), date, allergy, medication
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        if not entities["patient"]:
                            entities["patient"] = ent.text
                    if ent.label_ == "DATE":
                        entities["date"] = ent.text
                    if ent.label_ == "ORG":
                        entities["doctor"] = ent.text
            else:
                # Very small heuristic: look for YYYY-MM-DD or common date-like words
                m = re.search(r"(\d{4}-\d{2}-\d{2})", user_message)
                if m:
                    entities['date'] = m.group(1)
                # patient name: look for 'for <Name>' or 'patient <Name>' patterns
                m2 = re.search(r"(?:for|patient|named)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", user_message)
                if m2:
                    entities['patient'] = m2.group(1)

            # 3. Route to DB logic
            if intent == "list_appointments":
                qs = Appointment.objects.all()
                # Filter by date if present
                if entities["date"]:
                    try:
                        date_obj = datetime.strptime(entities["date"], "%Y-%m-%d").date()
                        qs = qs.filter(appointment_date__date=date_obj)
                    except Exception:
                        pass
                data = [{
                    'patient': a.patient.full_name if a.patient else 'N/A',
                    'doctor': f"{a.doctor.first_name} {a.doctor.last_name}" if a.doctor else 'N/A',
                    'time': a.appointment_date.strftime('%Y-%m-%d %H:%M'),
                    'reason': a.reason,
                } for a in qs]
                return JsonResponse({'success': True, 'data': data})

            elif intent == "list_medications":
                qs = Medication.objects.all()
                data = [{'name': m.name, 'dosage': m.dosage, 'start_date': m.start_date, 'end_date': m.end_date} for m in qs]
                return JsonResponse({'success': True, 'data': data})

            elif intent == "list_doctors":
                qs = MediAIUser.objects.filter(role='Doctor')
                data = [{'name': f"{d.first_name} {d.last_name}", 'email': d.email} for d in qs]
                return JsonResponse({'success': True, 'data': data})

            elif intent == "list_allergies":
                qs = Allergy.objects.all()
                data = [{'name': a.name, 'description': a.description} for a in qs]
                return JsonResponse({'success': True, 'data': data})

            elif intent == "patient_allergies":
                patient_name = entities.get("patient")
                if not patient_name:
                    return JsonResponse({'success': True, 'message': "Please provide a patient name to look up allergies."})
                qs = Patient.objects.filter(full_name__icontains=patient_name)
                if qs.exists():
                    allergies = qs.first().allergies.all()
                    data = [{'name': a.name, 'description': a.description} for a in allergies]
                    return JsonResponse({'success': True, 'data': data})
                else:
                    return JsonResponse({'success': True, 'message': f"No patient found with name {patient_name}"})

            # Fallback: Use DialoGPT for a generic response if available, otherwise return a canned fallback
            if chatbot is not None:
                conversation = chatbot(user_message, max_length=100, num_return_sequences=1)
                response = conversation[0].get('generated_text') if isinstance(conversation, list) and conversation else str(conversation)
                return JsonResponse({'success': True, 'message': response})
            else:
                return JsonResponse({'success': True, 'message': "Medi-AI assistant is currently unavailable (models not loaded). Please ask about appointments, medications, doctors, or allergies."})

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'success': False, 'error': str(e)})