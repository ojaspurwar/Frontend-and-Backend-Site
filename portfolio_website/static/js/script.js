// Simple JavaScript enhancements

// Mobile menu toggle functionality
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');

    if (navMenu && toggleBtn) {
        navMenu.classList.toggle('active');
        toggleBtn.classList.toggle('active');
    }
}

// Close mobile menu when clicking outside or on a link
document.addEventListener('click', function(event) {
    const navMenu = document.getElementById('navMenu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle');

    if (navMenu && toggleBtn) {
        // Close menu if clicking outside
        if (!event.target.closest('.navbar')) {
            navMenu.classList.remove('active');
            toggleBtn.classList.remove('active');
        }

        // Close menu when clicking on a nav link
        if (event.target.classList.contains('nav-link')) {
            navMenu.classList.remove('active');
            toggleBtn.classList.remove('active');
        }
    }
});

// Add active class to nav links based on current page
document.addEventListener('DOMContentLoaded', function() {
    const currentLocation = location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentLocation) {
            link.style.color = '#10b981';
            link.style.borderBottom = '2px solid #10b981';
        }
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.2)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.15)';
    }
});

// Prevent zoom on form inputs on mobile (iOS Safari)
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            // Add viewport meta tag if not present
            let viewport = document.querySelector('meta[name=viewport]');
            if (!viewport) {
                viewport = document.createElement('meta');
                viewport.name = 'viewport';
                viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
                document.head.appendChild(viewport);
            }
        });

        input.addEventListener('blur', function() {
            // Reset viewport after input blur
            setTimeout(() => {
                const viewport = document.querySelector('meta[name=viewport]');
                if (viewport) {
                    viewport.content = 'width=device-width, initial-scale=1.0';
                }
            }, 300);
        });
    });
});

// Add loading states for better UX
function showLoading(button) {
    const originalText = button.textContent;
    button.textContent = 'Sending...';
    button.disabled = true;

    return function reset() {
        button.textContent = originalText;
        button.disabled = false;
    };
}
