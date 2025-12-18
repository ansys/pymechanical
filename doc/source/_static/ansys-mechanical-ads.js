/**
 * Ansys Mechanical Custom Ads System
 * Displays promotional content for Ansys Mechanical products and services
 */

(function() {
    'use strict';

    // Ansys Mechanical Ads Configuration
    const AdsConfig = {
        // Rotation interval in milliseconds (30 seconds)
        rotationInterval: 30000,
        
        // Enable analytics tracking
        enableAnalytics: true,
        
        // Custom analytics endpoint (set this to your analytics server)
        analyticsEndpoint: null, // e.g., 'https://your-analytics-server.com/api/ads'
        // To enable: analyticsEndpoint: 'https://your-server.com/api/track-ads',
        
        // Base URLs for Ansys resources
        baseUrls: {
            mechanical: 'https://www.ansys.com/products/structures/ansys-mechanical',
            download: 'https://www.ansys.com/academic/students',
            training: 'https://www.ansys.com/training',
            community: 'https://forum.ansys.com/',
            documentation: 'https://ansyshelp.ansys.com/',
            pymechanical: 'https://github.com/ansys/pymechanical'
        }
    };

    // Ad Content Database
    const AdContent = {
        sidebar: [
            {
                id: 'mechanical-pro',
                title: 'Ansys Mechanical',
                description: 'Industry-leading finite element analysis for structural simulation.',
                cta: 'Learn More',
                url: AdsConfig.baseUrls.mechanical,
                priority: 1
            },
            {
                id: 'student-version',
                title: 'Free Student Version',
                description: 'Get Ansys Mechanical Student for learning and non-commercial use.',
                cta: 'Download Free',
                url: AdsConfig.baseUrls.download,
                priority: 2
            },
            {
                id: 'training',
                title: 'Ansys Training',
                description: 'Master Mechanical with expert-led courses and tutorials.',
                cta: 'Start Learning',
                url: AdsConfig.baseUrls.training,
                priority: 3
            },
            {
                id: 'community',
                title: 'Ansys Community',
                description: 'Connect with engineers and get expert help on the forum.',
                cta: 'Join Forum',
                url: AdsConfig.baseUrls.community,
                priority: 4
            },
            {
                id: 'pymechanical-github',
                title: 'PyMechanical on GitHub',
                description: 'Contribute to the open-source Pythonic interface for Mechanical.',
                cta: 'View Repository',
                url: AdsConfig.baseUrls.pymechanical,
                priority: 5
            }
        ],
        
        footer: [
            {
                id: 'mechanical-suite',
                title: 'Discover Ansys Mechanical Suite',
                description: 'Complete structural simulation solution for complex engineering challenges. From linear static analysis to advanced nonlinear simulations.',
                features: [
                    'Advanced Material Models',
                    'Contact & Friction Simulation',
                    'Nonlinear Analysis',
                    'Fatigue & Durability',
                    'Optimization Tools'
                ],
                ctas: [
                    {
                        text: 'Try Mechanical',
                        url: AdsConfig.baseUrls.mechanical,
                        primary: true
                    },
                    {
                        text: 'View Documentation',
                        url: AdsConfig.baseUrls.documentation,
                        primary: false
                    }
                ]
            },
            {
                id: 'academic-program',
                title: 'Ansys Academic Program',
                description: 'Free access to industry-standard simulation software for students and educators worldwide.',
                features: [
                    'Full-Featured Software',
                    'Educational Resources',
                    'Curriculum Support',
                    'Research Licenses',
                    'Global Community'
                ],
                ctas: [
                    {
                        text: 'Get Student License',
                        url: AdsConfig.baseUrls.download,
                        primary: true
                    },
                    {
                        text: 'Educator Resources',
                        url: AdsConfig.baseUrls.training,
                        primary: false
                    }
                ]
            }
        ]
    };

    // Main AnsysMechanicalAds object
    window.AnsysMechanicalAds = {
        currentSidebarIndex: 0,
        currentFooterIndex: 0,
        rotationTimer: null,
        
        /**
         * Initialize the ads system
         */
        init: function() {
            console.log('Initializing Ansys Mechanical Ads System');
            
            // Create ad containers if they don't exist
            this.createAdContainers();
            
            // Check if containers exist
            const sidebarContainer = document.getElementById('ansys-mechanical-sidebar-ad');
            const footerContainer = document.getElementById('ansys-mechanical-footer-ad');
            
            console.log('Sidebar container found:', !!sidebarContainer);
            console.log('Footer container found:', !!footerContainer);
            
            // Show ads only if not hidden
            if (this.shouldShowAd('sidebar') && sidebarContainer) {
                console.log('Rendering sidebar ad...');
                this.renderSidebarAd();
                sidebarContainer.style.display = 'block';
            }
            
            if (this.shouldShowAd('footer') && footerContainer) {
                console.log('Rendering footer ad...');
                this.renderFooterAd();
                footerContainer.style.display = 'block';
            }
            
            this.startRotation();
            this.bindEvents();
            
            console.log('Ads system initialization completed');
        },

        /**
         * Create ad containers dynamically
         */
        createAdContainers: function() {
            // Create wrapper if it doesn't exist
            let wrapper = document.getElementById('ansys-mechanical-ads-wrapper');
            if (!wrapper) {
                wrapper = document.createElement('div');
                wrapper.id = 'ansys-mechanical-ads-wrapper';
                wrapper.className = 'ansys-mechanical-ads-wrapper';
                wrapper.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 1000;';
                document.body.appendChild(wrapper);
            }

            // Create sidebar ad container
            let sidebarAd = document.getElementById('ansys-mechanical-sidebar-ad');
            if (!sidebarAd) {
                sidebarAd = document.createElement('div');
                sidebarAd.id = 'ansys-mechanical-sidebar-ad';
                sidebarAd.className = 'ansys-mechanical-ad-container sidebar-ad';
                sidebarAd.style.cssText = 'position: fixed; top: 100px; right: 20px; max-width: 280px; z-index: 1001; pointer-events: auto; display: none;';
                sidebarAd.innerHTML = '<div class="loading-spinner">Loading Ansys Content...</div>';
                wrapper.appendChild(sidebarAd);
            }

            // Create footer ad container
            let footerAd = document.getElementById('ansys-mechanical-footer-ad');
            if (!footerAd) {
                footerAd = document.createElement('div');
                footerAd.id = 'ansys-mechanical-footer-ad';
                footerAd.className = 'ansys-mechanical-ad-container content-ad';
                footerAd.style.cssText = 'position: fixed; bottom: 20px; left: 20px; right: 20px; max-width: 600px; margin: 0 auto; z-index: 1001; pointer-events: auto; display: none;';
                footerAd.innerHTML = '<div class="loading-spinner">Loading Ansys Content...</div>';
                wrapper.appendChild(footerAd);
            }
        },
        
        /**
         * Render sidebar advertisement
         */
        renderSidebarAd: function() {
            const container = document.getElementById('ansys-mechanical-sidebar-ad');
            if (!container) return;
            
            const ad = AdContent.sidebar[this.currentSidebarIndex];
            container.innerHTML = `
                <button class="ad-close" onclick="AnsysMechanicalAds.hideAd('sidebar')" title="Close">&times;</button>
                <div class="ad-title">${ad.title}</div>
                <div class="ad-description">${ad.description}</div>
                <a href="${ad.url}" class="ad-cta" target="_blank" rel="noopener" data-ad-id="${ad.id}">
                    ${ad.cta}
                </a>
            `;
        },
        
        /**
         * Render content advertisement
         */
        renderFooterAd: function() {
            const container = document.getElementById('ansys-mechanical-footer-ad');
            if (!container) return;
            
            const ad = AdContent.footer[this.currentFooterIndex];
            const featuresHtml = ad.features.map(feature => 
                `<div class="ad-feature">${feature}</div>`
            ).join('');
            
            const ctasHtml = ad.ctas.map(cta => 
                `<a href="${cta.url}" class="ad-cta ${cta.primary ? 'primary' : 'secondary'}" target="_blank" rel="noopener" data-ad-id="${ad.id}">
                    ${cta.text}
                </a>`
            ).join('');
            
            container.innerHTML = `
                <button class="ad-close" onclick="AnsysMechanicalAds.hideAd('footer')" title="Close">&times;</button>
                <div class="ad-title">${ad.title}</div>
                <div class="ad-description">${ad.description}</div>
                <div class="ad-features">${featuresHtml}</div>
                <div class="ad-ctas">${ctasHtml}</div>
            `;
        },
        
        /**
         * Start automatic rotation of ads
         */
        startRotation: function() {
            this.rotationTimer = setInterval(() => {
                this.rotateSidebarAd();
                // Rotate footer ads less frequently
                if (Math.random() < 0.3) {
                    this.rotateFooterAd();
                }
            }, AdsConfig.rotationInterval);
        },
        
        /**
         * Rotate sidebar advertisement
         */
        rotateSidebarAd: function() {
            this.currentSidebarIndex = (this.currentSidebarIndex + 1) % AdContent.sidebar.length;
            this.renderSidebarAd();
        },
        
        /**
         * Rotate footer advertisement
         */
        rotateFooterAd: function() {
            this.currentFooterIndex = (this.currentFooterIndex + 1) % AdContent.footer.length;
            this.renderFooterAd();
        },
        
        /**
         * Bind event listeners for analytics and interactions
         */
        bindEvents: function() {
            document.addEventListener('click', (event) => {
                if (event.target.classList.contains('ad-cta')) {
                    this.trackAdClick(event.target.dataset.adId);
                }
            });
            
            // Track ad impressions
            this.trackAdImpression();
        },
        
        /**
         * Track ad click events
         */
        trackAdClick: function(adId) {
            if (!AdsConfig.enableAnalytics) return;
            
            console.log('Ad clicked:', adId);
            
            // Send analytics data (implement your preferred analytics solution)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'ad_click', {
                    'ad_id': adId,
                    'event_category': 'ansys_mechanical_ads',
                    'event_label': adId
                });
            }
            
            // You can also send data to your own analytics endpoint
            this.sendAnalytics('click', adId);
        },
        
        /**
         * Track ad impression events
         */
        trackAdImpression: function() {
            if (!AdsConfig.enableAnalytics) return;
            
            console.log('Ads displayed on page');
            
            if (typeof gtag !== 'undefined') {
                gtag('event', 'ad_impression', {
                    'event_category': 'ansys_mechanical_ads',
                    'page_url': window.location.href
                });
            }
            
            this.sendAnalytics('impression', 'page_load');
        },
        
        /**
         * Send analytics data to custom endpoint
         */
        sendAnalytics: function(eventType, adId) {
            // Enhanced analytics data
            const analyticsData = {
                event: eventType,
                ad_id: adId,
                page_url: window.location.href,
                page_title: document.title,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                referrer: document.referrer,
                screen_resolution: screen.width + 'x' + screen.height,
                session_id: this.getSessionId()
            };
            
            // Log to console for debugging
            console.log('Analytics Event:', analyticsData);
            
            // Store locally for fallback
            this.storeAnalyticsLocally(analyticsData);
            
            // Send to custom analytics endpoint (uncomment and configure)
            if (AdsConfig.analyticsEndpoint) {
                fetch(AdsConfig.analyticsEndpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(analyticsData)
                }).catch(err => {
                    console.warn('Analytics endpoint error:', err);
                    // Fallback: could send to a different endpoint or queue for retry
                });
            }
        },

        /**
         * Store analytics data locally for reporting
         */
        storeAnalyticsLocally: function(data) {
            try {
                const stored = JSON.parse(localStorage.getItem('ansys_ads_analytics') || '[]');
                stored.push(data);
                
                // Keep only last 100 events to avoid storage bloat
                if (stored.length > 100) {
                    stored.splice(0, stored.length - 100);
                }
                
                localStorage.setItem('ansys_ads_analytics', JSON.stringify(stored));
            } catch (e) {
                console.warn('Could not store analytics locally:', e);
            }
        },

        /**
         * Get or create session ID
         */
        getSessionId: function() {
            let sessionId = sessionStorage.getItem('ansys_ads_session');
            if (!sessionId) {
                sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                sessionStorage.setItem('ansys_ads_session', sessionId);
            }
            return sessionId;
        },

        /**
         * Get analytics report from local storage
         */
        getAnalyticsReport: function() {
            try {
                const data = JSON.parse(localStorage.getItem('ansys_ads_analytics') || '[]');
                const report = {
                    total_events: data.length,
                    clicks: data.filter(e => e.event === 'click').length,
                    impressions: data.filter(e => e.event === 'impression').length,
                    unique_sessions: [...new Set(data.map(e => e.session_id))].length,
                    ad_performance: {}
                };
                
                // Calculate performance per ad
                data.forEach(event => {
                    if (event.ad_id && event.ad_id !== 'page_load') {
                        if (!report.ad_performance[event.ad_id]) {
                            report.ad_performance[event.ad_id] = { clicks: 0, impressions: 0 };
                        }
                        if (event.event === 'click') {
                            report.ad_performance[event.ad_id].clicks++;
                        } else if (event.event === 'impression') {
                            report.ad_performance[event.ad_id].impressions++;
                        }
                    }
                });
                
                return report;
            } catch (e) {
                console.error('Error generating analytics report:', e);
                return { error: 'Could not generate report' };
            }
        },
        
        /**
         * Hide an ad
         */
        hideAd: function(type) {
            const containerId = type === 'sidebar' ? 'ansys-mechanical-sidebar-ad' : 'ansys-mechanical-footer-ad';
            const container = document.getElementById(containerId);
            if (container) {
                container.style.display = 'none';
                // Store preference to not show again this session
                sessionStorage.setItem(`ansys_ads_hidden_${type}`, 'true');
            }
        },
        
        /**
         * Check if ads should be shown
         */
        shouldShowAd: function(type) {
            return !sessionStorage.getItem(`ansys_ads_hidden_${type}`);
        },

        /**
         * Stop ad rotation (cleanup)
         */
        destroy: function() {
            if (this.rotationTimer) {
                clearInterval(this.rotationTimer);
                this.rotationTimer = null;
            }
        }
    };
    
    // Expose analytics functions globally for easy access
    window.AnsysAdsAnalytics = {
        getReport: function() {
            return window.AnsysMechanicalAds.getAnalyticsReport();
        },
        exportData: function() {
            const data = localStorage.getItem('ansys_ads_analytics');
            const blob = new Blob([data || '[]'], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ansys_ads_analytics_' + new Date().toISOString().split('T')[0] + '.json';
            a.click();
            URL.revokeObjectURL(url);
        },
        clearData: function() {
            localStorage.removeItem('ansys_ads_analytics');
            sessionStorage.removeItem('ansys_ads_session');
            console.log('Analytics data cleared');
        },
        viewConsoleReport: function() {
            console.table(this.getReport());
        }
    };

    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, initializing ads...');
            setTimeout(function() {
                if (window.AnsysMechanicalAds) {
                    window.AnsysMechanicalAds.init();
                } else {
                    console.error('AnsysMechanicalAds not found on window object');
                }
            }, 100);
        });
    } else {
        console.log('DOM already ready, initializing ads immediately...');
        setTimeout(function() {
            if (window.AnsysMechanicalAds) {
                window.AnsysMechanicalAds.init();
            } else {
                console.error('AnsysMechanicalAds not found on window object');
            }
        }, 100);
    }
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
        if (window.AnsysMechanicalAds) {
            window.AnsysMechanicalAds.destroy();
        }
    });
    
})();
