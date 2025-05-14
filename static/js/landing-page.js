document.addEventListener('DOMContentLoaded', function() {
    console.log('Landing page loaded');

    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Handle logo links in the landing page
    document.querySelectorAll('.navbar-brand, .footer-logo-link').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '/') {
                e.preventDefault();
                // Scroll to top of the page
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Animate hero image on hover
    const heroImage = document.querySelector('.hero-image');
    if (heroImage) {
        heroImage.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-10px)';
        });

        heroImage.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    }

    // Animate feature cards on hover
    const featureCards = document.querySelectorAll('.feature-card');

    featureCards.forEach(card => {
        card.addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Note: Get Started button and navigation links are now handled by page-transitions.js
    // This code is kept for reference but is no longer active

    // Handle mobile navigation
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking a nav link
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // Preload chat page for faster transition
    setTimeout(function() {
        const linkPreload = document.createElement('link');
        linkPreload.rel = 'prefetch';
        linkPreload.href = '/chat';
        document.head.appendChild(linkPreload);
        console.log('Chat page prefetched for faster loading');
    }, 3000);
});
