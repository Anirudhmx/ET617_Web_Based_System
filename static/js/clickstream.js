// Clickstream tracking functionality
class ClickTracker {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.initializeTracking();
    }

    generateSessionId() {
        // Generate a unique session ID
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    initializeTracking() {
        // Track clicks on all elements
        document.addEventListener('click', (event) => {
            this.trackClick(event);
        });

        // Track page views
        this.trackPageView();

        // Track form submissions
        document.addEventListener('submit', (event) => {
            this.trackFormSubmission(event);
        });

        // Track navigation
        window.addEventListener('popstate', () => {
            this.trackPageView();
        });

        // Track scroll events (throttled)
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                this.trackScroll();
            }, 1000);
        });
    }

    trackClick(event) {
        const target = event.target;
        const clickData = {
            page_url: window.location.href,
            element_id: target.id || '',
            element_class: target.className || '',
            element_text: this.getTextContent(target),
            click_x: event.clientX,
            click_y: event.clientY,
            timestamp: new Date().toISOString()
        };

        this.sendClickData(clickData);
    }

    trackPageView() {
        const pageData = {
            page_url: window.location.href,
            element_id: 'page_view',
            element_class: 'navigation',
            element_text: document.title,
            click_x: null,
            click_y: null,
            timestamp: new Date().toISOString()
        };

        this.sendClickData(pageData);
    }

    trackFormSubmission(event) {
        const formData = {
            page_url: window.location.href,
            element_id: event.target.id || 'form_submission',
            element_class: 'form_submit',
            element_text: 'Form submitted',
            click_x: null,
            click_y: null,
            timestamp: new Date().toISOString()
        };

        this.sendClickData(formData);
    }

    trackScroll() {
        const scrollData = {
            page_url: window.location.href,
            element_id: 'scroll_event',
            element_class: 'user_interaction',
            element_text: `Scrolled to ${Math.round(window.scrollY)}px`,
            click_x: null,
            click_y: null,
            timestamp: new Date().toISOString()
        };

        this.sendClickData(scrollData);
    }

    getTextContent(element) {
        // Get meaningful text content from element
        let text = '';
        
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            text = element.placeholder || element.value || element.name;
        } else if (element.tagName === 'BUTTON') {
            text = element.textContent || element.innerText || element.value;
        } else if (element.tagName === 'A') {
            text = element.textContent || element.innerText || element.href;
        } else {
            text = element.textContent || element.innerText || element.title;
        }

        // Limit text length
        return text ? text.substring(0, 200) : '';
    }

    async sendClickData(data) {
        try {
            const response = await fetch('/track_click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                console.warn('Failed to track click:', response.status);
            }
        } catch (error) {
            console.warn('Error tracking click:', error);
        }
    }

    // Method to manually track specific events
    trackCustomEvent(eventName, additionalData = {}) {
        const customData = {
            page_url: window.location.href,
            element_id: 'custom_event',
            element_class: eventName,
            element_text: `Custom event: ${eventName}`,
            click_x: null,
            click_y: null,
            timestamp: new Date().toISOString(),
            ...additionalData
        };

        this.sendClickData(customData);
    }
}

// Initialize click tracking when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.clickTracker = new ClickTracker();
    
    // Add tracking to specific interactive elements
    const trackableElements = document.querySelectorAll('[data-track]');
    trackableElements.forEach(element => {
        element.addEventListener('click', (event) => {
            const trackData = element.dataset.track;
            if (trackData) {
                window.clickTracker.trackCustomEvent('custom_track', {
                    element_text: trackData,
                    element_id: element.id || '',
                    element_class: element.className || ''
                });
            }
        });
    });
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ClickTracker;
}
