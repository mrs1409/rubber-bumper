/**
 * Page Transitions
 * Handles smooth transitions between pages
 */

class PageTransition {
    constructor() {
        this.isAnimating = false;
        this.duration = 600; // Duration in ms
        this.overlay = null;
        this.init();
    }

    init() {
        // Create overlay element if it doesn't exist
        if (!document.querySelector('.page-transition-overlay')) {
            this.overlay = document.createElement('div');
            this.overlay.className = 'page-transition-overlay';
            document.body.appendChild(this.overlay);
        } else {
            this.overlay = document.querySelector('.page-transition-overlay');
        }

        // Add fade-in animation to the current page
        document.body.classList.add('fade-in-page');

        // Initialize navigation event listeners
        this.initNavigationEvents();
    }

    initNavigationEvents() {
        // Handle all navigation links
        document.querySelectorAll('a[href^="/"]').forEach(link => {
            // Skip links that open in new tabs or have special behavior
            if (link.getAttribute('target') === '_blank' ||
                link.getAttribute('download') ||
                link.getAttribute('rel') === 'external') {
                return;
            }

            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');

                // Skip if it's a hash link on the same page
                if (href.startsWith('#') || href === window.location.pathname) {
                    return;
                }

                // Prevent default navigation
                e.preventDefault();

                // Perform transition
                this.goToPage(href);
            });
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.url) {
                this.goToPage(e.state.url, true);
            }
        });
    }

    goToPage(href, isPopState = false) {
        // Prevent multiple transitions at once
        if (this.isAnimating) return;
        this.isAnimating = true;

        // Log the transition
        console.log(`Transitioning to: ${href}`);

        // Add exit animation to current page
        document.body.classList.add('page-transition-exit');

        // Animate overlay
        this.overlay.classList.add('active');

        // Wait for animation to complete
        setTimeout(() => {
            // Navigate to the new page
            if (!isPopState) {
                window.history.pushState({ url: href }, '', href);
            }
            window.location.href = href;
        }, this.duration);
    }

    // Method to be called when the page loads
    onPageLoad() {
        // Add enter animation to the new page
        document.body.classList.add('page-transition-enter');

        // Remove the overlay with a slight delay
        setTimeout(() => {
            if (this.overlay) {
                this.overlay.classList.remove('active');
            }

            // Add active class to trigger animation
            document.body.classList.add('page-transition-enter-active');

            // Remove classes after animation completes
            setTimeout(() => {
                document.body.classList.remove('page-transition-enter');
                document.body.classList.remove('page-transition-enter-active');
                this.isAnimating = false;
            }, this.duration);
        }, 100);
    }
}

// Initialize page transition
let pageTransition;

document.addEventListener('DOMContentLoaded', () => {
    // Handle preloader
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        // Hide preloader after page is fully loaded
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.classList.add('fade-out');

                // Initialize page transition after preloader is hidden
                setTimeout(() => {
                    pageTransition = new PageTransition();

                    // Call onPageLoad to handle entrance animation
                    pageTransition.onPageLoad();
                }, 500);
            }, 500);
        });

        // Fallback: Hide preloader after a maximum time (3 seconds)
        setTimeout(() => {
            if (!preloader.classList.contains('fade-out')) {
                preloader.classList.add('fade-out');

                // Initialize page transition
                if (!pageTransition) {
                    pageTransition = new PageTransition();
                    pageTransition.onPageLoad();
                }
            }
        }, 3000);
    } else {
        // If no preloader, initialize page transition immediately
        pageTransition = new PageTransition();
        pageTransition.onPageLoad();
    }

    // Handle all navigation links with the transition system
    document.querySelectorAll('a[href^="/"]').forEach(link => {
        // Skip links that already have click handlers or special attributes
        if (link.getAttribute('target') === '_blank' ||
            link.getAttribute('download') ||
            link.getAttribute('rel') === 'external' ||
            link.hasAttribute('onclick')) {
            return;
        }

        // Remove any existing onclick attributes
        if (link.hasAttribute('onclick')) {
            link.removeAttribute('onclick');
        }

        // Add click event listener
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');

            // Skip if it's a hash link on the same page
            if (href.startsWith('#') || href === window.location.pathname) {
                return;
            }

            // Prevent default navigation
            e.preventDefault();

            // Log the click
            console.log(`Link clicked: ${href}`);

            // Perform transition
            if (pageTransition) {
                pageTransition.goToPage(href);
            } else {
                // Fallback if pageTransition is not initialized
                window.location.href = href;
            }
        });
    });

    // Special handling for Get Started button
    const getStartedBtn = document.querySelector('.get-started-btn');
    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', (e) => {
            e.preventDefault();

            // Add clicked class for visual feedback
            getStartedBtn.classList.add('clicked');

            // Log the click
            console.log('Get Started button clicked, transitioning to chat page');

            // Perform transition
            if (pageTransition) {
                pageTransition.goToPage('/chat');
            } else {
                // Fallback if pageTransition is not initialized
                setTimeout(() => {
                    window.location.href = '/chat';
                }, 300);
            }
        });
    }
});
