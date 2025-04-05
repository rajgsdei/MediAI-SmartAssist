class SharedCRUD {
    constructor(options) {
        this.options = {
            baseUrl: options.baseUrl,
            entityName: options.entityName,
            containerId: options.containerId,
            formFields: options.formFields || [],
            urls: {
                detail: options.urls?.detail || ((id) => `${options.baseUrl}${id}/`),
                delete: options.urls?.delete || ((id) => `${options.baseUrl}${id}/delete/`)
            },
            ...options
        };
        
        this.modal = new bootstrap.Modal(document.getElementById('entityModal'));
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Create button
        $(`#create${this.options.entityName}`).on('click', () => this.showModal('create'));

        // Table actions
        $(document).on('click', '.view-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.showModal('view', id);
        });

        $(document).on('click', '.edit-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.showModal('edit', id);
        });

        $(document).on('click', '.delete-btn', (e) => {
            const id = $(e.currentTarget).data('id');
            this.confirmDelete(id);
        });

        // Save entity
        $('#saveEntity').on('click', () => this.saveEntity());

        // Search functionality
        $('#searchInput').on('input', (e) => {
            const searchTerm = e.target.value.trim();
            this.loadData({ search: searchTerm });
        });

        // Sort functionality
        $(document).on('click', '.sortable', (e) => {
            const column = $(e.currentTarget).data('sort');
            this.handleSort(column);
        });
    }

    showModal(mode, id = null) {
        const modalEl = document.getElementById('entityModal');
        const title = `${mode.charAt(0).toUpperCase() + mode.slice(1)} ${this.options.entityName}`;
        modalEl.querySelector('.modal-title').textContent = title;

        // Show loader and hide form
        $('.modal-loader').removeClass('d-none');
        $('#entityForm').addClass('d-none');

        if (mode === 'create') {
            this.resetForm();
            this.generateFormFields();
            // Set default values for new records
            this.options.formFields.forEach(field => {
                if (field.type === 'checkbox' && field.name === 'is_active') {
                    $(`#${field.name}`).prop('checked', true);
                }
            });
            // Hide loader and show form for create mode
            $('.modal-loader').addClass('d-none');
            $('#entityForm').removeClass('d-none');
        } else {
            this.loadEntityData(id, mode === 'view');
        }

        this.modal.show();
    }

    generateFormFields() {
        const formFieldsContainer = document.getElementById('formFields');
        formFieldsContainer.innerHTML = '';
    
        this.options.formFields.forEach(field => {
            // Create column div
            const colDiv = document.createElement('div');
            colDiv.className = field.type === 'checkbox' ? 'col-12' : 'col-md-6'; // Full width for checkbox, half for others
    
            // Create form group
            const formGroup = document.createElement('div');
            //formGroup.className = field.type === 'checkbox' ? 'form-check mb-3' : 'form-group mb-3';
            formGroup.className = field.type === 'checkbox' ? 'form-group top-margin' : 'form-group top-margin';
    
            // Label
            const label = document.createElement('label');
            label.htmlFor = field.name;
            label.className = field.type === 'checkbox' ? 'form-check-label' : 'form-label';
            label.textContent = field.label;
            if (field.required) {
                label.innerHTML += ' <span class="text-danger">*</span>';
            }
    
            // Input
            const input = document.createElement('input');
            input.type = field.type || 'text';
            input.className = field.type === 'checkbox' ? 'form-check-input' : 'form-control';
            input.id = field.name;
            input.name = field.name;
            input.required = field.required || false;
    
            // Add to form group in correct order
            if (field.type === 'checkbox') {
                formGroup.appendChild(input);
                formGroup.appendChild(label);
            } else {
                formGroup.appendChild(label);
                formGroup.appendChild(input);
            }
    
            // Add form group to column
            colDiv.appendChild(formGroup);
            // Add column to container
            formFieldsContainer.appendChild(colDiv);
        });
    }

    loadData(params = {}) {
        params.ajax = true;  // Always request partial content
        const $container = $(`#${this.options.containerId}`);
        const $loader = $container.find('.div-loader');
        
        $loader.show();
        $.get(this.options.baseUrl, params)
            .done(response => {
                $container.html(response);
            })
            .fail(() => {
                alert('Error loading data');
            })
            .always(() => {
                $loader.hide();
            });
    }

    loadEntityData(id, readonly = false) {
        const url = this.options.urls.detail.call(this, id);
        $.get(url)
            .done(response => {
                this.populateForm(response.data, readonly);
            })
            .fail(() => {
                alert('Error loading data');
                $('#entityModal').modal('hide');
            })
            .always(() => {
                // Hide loader and show form
                $('.modal-loader').addClass('d-none');
                $('#entityForm').removeClass('d-none');
            });
    }

    populateForm(data, readonly = false) {
        const form = $('#entityForm');
        form.data('id', data.id);
        
        // Reset form and generate fields first
        this.resetForm();
        this.generateFormFields();
        
        // Populate each field
        this.options.formFields.forEach(field => {
            const input = $(`#${field.name}`);
            if (input.length) {
                if (field.type === 'checkbox') {
                    input.prop('checked', data[field.name]);
                } else {
                    input.val(data[field.name]);
                }
                
                // Handle readonly state
                if (readonly) {
                    input.prop('disabled', true);
                }
            }
        });
        
        // Update modal title and button visibility
        $('#entityModalLabel').text(`${readonly ? 'View' : 'Edit'} ${this.options.entityName}`);
        $('#saveButton').toggle(!readonly);
    }

    saveEntity() {
        const form = $('#entityForm');
        const formData = new FormData(form[0]);
        const id = form.data('id');
        
        const url = id ? this.options.urls.detail.call(this, id) : this.options.baseUrl;
        
        // Get CSRF token from cookie
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        $.ajax({
            url: url,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: (response) => {
                if (response.success) {
                    // Remove focus from any button before hiding modal
                    const activeElement = document.activeElement;
                    if (activeElement && activeElement.tagName === 'BUTTON') {
                        activeElement.blur();
                    }
                    
                    // Hide modal and remove backdrop
                    const modalElement = document.getElementById('entityModal');
                    modalElement.addEventListener('hidden.bs.modal', () => {
                        this.loadData();
                    }, { once: true });
                    
                    this.modal.hide();
                } else {
                    this.showErrors(response.errors);
                }
            },
            error: (xhr) => {
                console.error('Save error:', xhr.responseText);
                alert('Error saving data');
            }
        });
    }

    confirmDelete(id) {
        if (confirm(`Are you sure you want to delete this ${this.options.entityName.toLowerCase()}?`)) {
            const url = this.options.urls.delete.call(this, id);
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            $.ajax({
                url: url,
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: () => {
                    this.loadData()
                },
                error: () => alert('Error deleting item')
            });
        }
    }

    // Helper methods
    resetForm() {
        $('#entityForm')[0].reset();
        $('#modalErrors').addClass('d-none').empty();
    }

    showErrors(errors) {
        const errorDiv = $('#modalErrors');
        errorDiv.removeClass('d-none').empty();
        
        Object.entries(errors).forEach(([field, messages]) => {
            errorDiv.append(`<p>${field}: ${messages.join(', ')}</p>`);
        });
    }

    handleSort(column) {
        this.loadData({ sort: column });
    }
}