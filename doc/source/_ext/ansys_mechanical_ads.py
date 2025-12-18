"""Sphinx extension for Ansys Mechanical promotional ads."""

from pathlib import Path
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging

logger = logging.getLogger(__name__)


def add_ads_assets(app: Sphinx, pagename: str, templatename: str, context: dict, doctree) -> None:
    """Add Ansys Mechanical ads assets and HTML to every page."""
    if app.builder.format != 'html':
        return
        
    # Add CSS and JS to the page
    app.add_css_file('ansys-mechanical-ads.css')
    app.add_js_file('ansys-mechanical-ads.js')
    
    # Add ads HTML to the body
    ads_html = '''
    <!-- Ansys Mechanical Ads -->
    <div class="ansys-mechanical-ads-wrapper" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 1000;">
        <!-- Sidebar Ad -->
        <div id="ansys-mechanical-sidebar-ad" class="ansys-mechanical-ad-container sidebar-ad" style="position: fixed; top: 100px; right: 20px; max-width: 280px; z-index: 1001; pointer-events: auto;">
            <div class="loading-spinner">Loading Ansys Content...</div>
        </div>
        
        <!-- Content Area Ad -->
        <div id="ansys-mechanical-footer-ad" class="ansys-mechanical-ad-container content-ad" style="position: fixed; bottom: 20px; left: 20px; right: 20px; max-width: 600px; margin: 0 auto; z-index: 1001; pointer-events: auto;">
            <div class="loading-spinner">Loading Ansys Content...</div>
        </div>
    </div>

    <!-- Initialize Ads -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Initializing Ansys Mechanical Ads...');
            if (typeof AnsysMechanicalAds !== 'undefined') {
                AnsysMechanicalAds.init();
            } else {
                console.warn('AnsysMechanicalAds not loaded');
            }
        });
    </script>
    '''
    
    # Inject ads HTML at the end of the body
    if 'body' not in context:
        context['body'] = ''
    context['body'] += ads_html


def setup(app: Sphinx) -> dict:
    """Set up the Sphinx extension."""
    app.connect('html-page-context', add_ads_assets)
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
