// Main JavaScript file for Veterinaria a Domicilio

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add custom validation styles
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 9) {
                value = value.replace(/(\d{3})(\d{3})(\d{3})/, '$1 $2 $3');
            }
            e.target.value = value;
        });
    });
    
    // Auto-generate slug from title
    const titleInput = document.getElementById('titulo');
    const slugInput = document.getElementById('slug');
    
    if (titleInput && slugInput) {
        titleInput.addEventListener('input', function(e) {
            const slug = e.target.value
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-')
                .trim();
            slugInput.value = slug;
        });
    }
});

// Loading states for forms
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Enviando...';
    button.disabled = true;
    
    return function() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Date/time validation for appointments
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('fecha_pref');
    const timeInput = document.getElementById('hora_pref');
    
    if (dateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        
        // Set maximum date to 3 months from now
        const maxDate = new Date();
        maxDate.setMonth(maxDate.getMonth() + 3);
        dateInput.setAttribute('max', maxDate.toISOString().split('T')[0]);
    }
    
    if (timeInput) {
        // Set working hours constraints
        timeInput.addEventListener('change', function(e) {
            const time = e.target.value;
            const hour = parseInt(time.split(':')[0]);
            
            if (hour < 9 || hour > 18) {
                alert('Por favor, selecciona una hora entre las 9:00 y las 18:00');
                e.target.value = '';
            }
        });
    }
});