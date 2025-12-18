"""
Ansys Mechanical Ads Sphinx Extension

This extension adds custom Ansys Mechanical promotional content 
to the generated Sphinx documentation.
"""

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class AnsysMechanicalAdDirective(SphinxDirective):
    """Directive to insert Ansys Mechanical promotional content."""
    
    has_content = False
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'type': str,  # 'sidebar', 'footer', 'inline'
        'ad_id': str,  # specific ad to display
        'style': str,  # custom styling class
    }

    def run(self):
        ad_type = self.options.get('type', 'inline')
        ad_id = self.options.get('ad_id', '')
        custom_style = self.options.get('style', '')
        
        # Create the ad container with appropriate classes
        classes = f"ansys-mechanical-ad-container {ad_type}-ad {custom_style}".strip()
        
        if ad_id:
            ad_html = f'<div class="{classes}" data-ad-id="{ad_id}"><div class="loading-spinner">Loading Ansys Content...</div></div>'
        else:
            ad_html = f'<div class="{classes}"><div class="loading-spinner">Loading Ansys Content...</div></div>'
        
        # Create the ad container node
        ad_node = nodes.raw(
            '',
            ad_html,
            format='html'
        )
        
        return [ad_node]


class AnsysMechanicalPromoDirective(SphinxDirective):
    """Directive to insert specific Ansys Mechanical promotional content."""
    
    has_content = True
    required_arguments = 1  # title
    optional_arguments = 0
    option_spec = {
        'description': str,
        'url': str,
        'cta_text': str,
        'image_url': str,
        'features': str,  # comma-separated list
    }

    def run(self):
        title = self.arguments[0]
        description = self.options.get('description', '')
        url = self.options.get('url', '#')
        cta_text = self.options.get('cta_text', 'Learn More')
        image_url = self.options.get('image_url', '')
        features = self.options.get('features', '').split(',') if self.options.get('features') else []
        
        # Process content if any
        content_html = ''
        if self.content:
            content_html = '<div class="promo-content">' + '\n'.join(self.content) + '</div>'
        
        # Build features HTML
        features_html = ''
        if features:
            features_items = ''.join([f'<div class="promo-feature">{feature.strip()}</div>' for feature in features])
            features_html = f'<div class="promo-features">{features_items}</div>'
        
        # Build image HTML
        image_html = ''
        if image_url:
            image_html = f'<div class="promo-image"><img src="{image_url}" alt="{title}" /></div>'
        
        # Create complete promotional content
        promo_html = f'''
        <div class="ansys-mechanical-promo-container">
            {image_html}
            <div class="promo-content-wrapper">
                <div class="promo-title">{title}</div>
                {f'<div class="promo-description">{description}</div>' if description else ''}
                {content_html}
                {features_html}
                <div class="promo-actions">
                    <a href="{url}" class="promo-cta" target="_blank" rel="noopener">{cta_text}</a>
                </div>
            </div>
        </div>
        '''
        
        # Create the promotional node
        promo_node = nodes.raw(
            '',
            promo_html,
            format='html'
        )
        
        return [promo_node]


def add_custom_css_js(app, config):
    """Add custom CSS and JS files for Ansys Mechanical ads."""
    # Add CSS file
    app.add_css_file('ansys-mechanical-ads.css')
    
    # Add JavaScript file
    app.add_js_file('ansys-mechanical-ads.js')


def setup(app: Sphinx):
    """Setup the Ansys Mechanical Ads extension."""
    
    # Add directives
    app.add_directive('ansys-mechanical-ad', AnsysMechanicalAdDirective)
    app.add_directive('ansys-mechanical-promo', AnsysMechanicalPromoDirective)
    
    # Connect to config-inited event to add CSS/JS
    app.connect('config-inited', add_custom_css_js)
    
    # Add custom CSS for the promotional content
    css_content = '''
    /* Ansys Mechanical Promotional Content */
    .ansys-mechanical-promo-container {
        margin: 20px 0;
        padding: 20px;
        background: linear-gradient(135deg, #0078d4 0%, #1ba1e2 100%);
        border-radius: 12px;
        color: white;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.2);
    }
    
    .promo-image img {
        max-width: 150px;
        height: auto;
        border-radius: 8px;
    }
    
    .promo-content-wrapper {
        flex: 1;
    }
    
    .promo-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 10px;
        color: #ffffff;
    }
    
    .promo-description {
        font-size: 14px;
        margin-bottom: 15px;
        color: #e6f3ff;
        line-height: 1.4;
    }
    
    .promo-features {
        margin: 15px 0;
    }
    
    .promo-feature {
        font-size: 13px;
        color: #e6f3ff;
        margin: 5px 0;
    }
    
    .promo-feature::before {
        content: '✓ ';
        color: #00ff88;
        font-weight: bold;
    }
    
    .promo-cta {
        background: #ffffff;
        color: #0078d4;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .promo-cta:hover {
        background: #f8f9fa;
        transform: scale(1.05);
        text-decoration: none;
    }
    
    @media (max-width: 768px) {
        .ansys-mechanical-promo-container {
            flex-direction: column;
            text-align: center;
        }
    }
    '''
    
    # Write CSS to static directory during build
    def write_custom_css(app, exception):
        if exception is None:  # Only if build was successful
            static_path = app.outdir + '/_static'
            css_file = static_path + '/ansys-promo.css'
            try:
                import os
                os.makedirs(static_path, exist_ok=True)
                with open(css_file, 'w') as f:
                    f.write(css_content)
                app.add_css_file('ansys-promo.css')
            except Exception as e:
                print(f"Warning: Could not write custom CSS: {e}")
    
    app.connect('build-finished', write_custom_css)
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
