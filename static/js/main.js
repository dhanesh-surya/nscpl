// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        offset: 100
    });
    
    // Initialize Hero Carousel
    initHeroCarousel();
});

function initHeroCarousel() {
    const heroCarousel = document.getElementById('heroCarousel');
    if (heroCarousel) {
        heroCarousel.addEventListener('mouseenter', function() {
            const carouselInstance = bootstrap.Carousel.getInstance(this);
            if (carouselInstance) {
                carouselInstance.pause();
            }
        });

        heroCarousel.addEventListener('mouseleave', function() {
            const carouselInstance = bootstrap.Carousel.getInstance(this);
            if (carouselInstance) {
                carouselInstance.cycle();
            }
        });
        // Add smooth transitions
        const carouselItems = heroCarousel.querySelectorAll('.carousel-item');
        carouselItems.forEach(item => {
            item.style.transition = 'transform 0.6s ease-in-out';
        });
        
        // Add fade effect to indicators
        const indicators = heroCarousel.querySelectorAll('.carousel-indicators button');
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', function() {
                // Remove active class from all indicators
                indicators.forEach(ind => ind.classList.remove('active'));
                // Add active class to clicked indicator
                this.classList.add('active');
            });
        });
    }
}

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

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});

// Gallery filter functionality
function filterGallery(category, tag) {
    const items = document.querySelectorAll('.gallery-item');
    const categoryFilter = category || 'all';
    const tagFilter = tag || 'all';
    
    items.forEach(item => {
        const itemCategory = item.dataset.category;
        const itemTags = item.dataset.tags;
        
        let showItem = true;
        
        if (categoryFilter !== 'all' && itemCategory !== categoryFilter) {
            showItem = false;
        }
        
        if (tagFilter !== 'all' && !itemTags.includes(tagFilter)) {
            showItem = false;
        }
        
        if (showItem) {
            item.style.display = 'block';
            item.classList.add('fade-in-up');
        } else {
            item.style.display = 'none';
            item.classList.remove('fade-in-up');
        }
    });
}

// Contact form validation
function validateContactForm() {
    const form = document.querySelector('#contactForm');
    if (!form) return;
    
    const name = form.querySelector('input[name="name"]');
    const email = form.querySelector('input[name="email"]');
    const subject = form.querySelector('input[name="subject"]');
    const message = form.querySelector('textarea[name="message"]');
    
    let isValid = true;
    
    // Clear previous error states
    [name, email, subject, message].forEach(field => {
        field.classList.remove('is-invalid');
    });
    
    // Validate name
    if (!name.value.trim()) {
        name.classList.add('is-invalid');
        isValid = false;
    }
    
    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.value.trim() || !emailRegex.test(email.value)) {
        email.classList.add('is-invalid');
        isValid = false;
    }
    
    // Validate subject
    if (!subject.value.trim()) {
        subject.classList.add('is-invalid');
        isValid = false;
    }
    
    // Validate message
    if (!message.value.trim()) {
        message.classList.add('is-invalid');
        isValid = false;
    }
    
    return isValid;
}

// Add loading state to forms
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Sending...';
    button.disabled = true;
    
    // Remove loading state after 3 seconds (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 3000);
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('#searchInput');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const searchableItems = document.querySelectorAll('[data-searchable]');
        
        searchableItems.forEach(item => {
            const searchableText = item.dataset.searchable.toLowerCase();
            if (searchableText.includes(searchTerm)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    initPopovers();
    initSearch();

    // Show popup modal on page load if it exists
    // Initialize and show the popup modal if it exists
    const popupModalElement = document.getElementById('popupModal');
    if (popupModalElement) {
        // Add a small delay to ensure Bootstrap's JS is fully loaded and initialized
        setTimeout(() => {
            const popupModal = new bootstrap.Modal(popupModalElement);
            popupModal.show();
            // Initialize image popup for zoom functionality after the modal is shown and image is loaded
            const popupImage = popupModalElement.querySelector('.zz_image');
            if (popupImage) {
                if (popupImage.complete) {
                    // If image is already loaded, initialize immediately
                    $(popupImage).imagePopup();
                } else {
                    // Otherwise, wait for the image to load
                    popupImage.addEventListener('load', function() {
                        $(this).imagePopup();
                    });
                }
            }
        }, 100);
    }
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in-up');
    });
    
    // Add click handlers for gallery filters
    const categoryFilters = document.querySelectorAll('[data-filter-category]');
    categoryFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const category = this.dataset.filterCategory;
            filterGallery(category);
            
            // Update active state
            categoryFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Logo enlarge modal: open modal when elements with .hero-logo-trigger are clicked
    const logoTriggers = document.querySelectorAll('.hero-logo-trigger');
    if (logoTriggers.length) {
        const logoModalEl = document.getElementById('logoModal');
        const logoModalImg = logoModalEl ? logoModalEl.querySelector('#logoModalImage') : null;

        logoTriggers.forEach(trigger => {
            trigger.addEventListener('click', function (e) {
                const logoUrl = this.dataset && this.dataset.logoUrl ? this.dataset.logoUrl : null;
                if (!logoUrl || !logoModalEl || !logoModalImg) return;
                // set image src and show modal
                logoModalImg.src = logoUrl;
                const logoModal = new bootstrap.Modal(logoModalEl);
                logoModal.show();

                // clear image src when modal is hidden to free memory
                logoModalEl.addEventListener('hidden.bs.modal', function () {
                    logoModalImg.src = '';
                }, { once: true });
            });
        });
    }
    
    const tagFilters = document.querySelectorAll('[data-filter-tag]');
    tagFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const tag = this.dataset.filterTag;
            filterGallery(null, tag);
            
            // Update active state
            tagFilters.forEach(f => f.classList.remove('active'));
            this.classList.add('active');
        });
    });

});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Export functions for global use
window.filterGallery = filterGallery;
window.validateContactForm = validateContactForm;
window.addLoadingState = addLoadingState;
window.showNotification = showNotification;
