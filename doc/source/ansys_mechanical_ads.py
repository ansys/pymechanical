"""
Ansys Mechanical Ads Sphinx Extension

This extension adds custom Ansys Mechanical promotional content 
to the generated Sphinx documentation.
"""

def setup(app):
    """Setup the Ansys Mechanical Ads extension."""
    
    # Add CSS and JS files
    app.add_css_file('ansys-mechanical-ads.css')
    app.add_js_file('ansys-mechanical-ads.js')
    
    print("✅ Ansys Mechanical Ads extension loaded successfully")
    
    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
