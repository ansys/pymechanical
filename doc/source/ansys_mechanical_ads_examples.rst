.. _ansys_mechanical_ads_examples:

Ansys Mechanical Ads Examples
=============================

This page demonstrates how to use the custom Ansys Mechanical promotional directives in your documentation.

Inline Ad Example
-----------------

You can insert an inline ad using the ``ansys-mechanical-ad`` directive:

.. ansys-mechanical-ad::
   :type: inline
   :ad_id: mechanical-pro

Custom Promotional Content
--------------------------

Create custom promotional sections using the ``ansys-mechanical-promo`` directive:

.. ansys-mechanical-promo:: Ansys Mechanical Student Version
   :description: Free access to industry-leading finite element analysis software for students worldwide.
   :url: https://www.ansys.com/academic/students
   :cta_text: Download Free Version
   :features: Full FEA capabilities, Advanced material models, Nonlinear analysis, Educational resources

   Perfect for learning structural simulation, completing coursework, and building your engineering portfolio.

Advanced Promo with Image
-------------------------

.. ansys-mechanical-promo:: Ansys Mechanical Professional
   :description: Complete structural simulation solution for complex engineering challenges.
   :url: https://www.ansys.com/products/structures/ansys-mechanical
   :cta_text: Learn More
   :image_url: https://www.ansys.com/content/dam/product-images/mechanical/mechanical-hero.jpg
   :features: Advanced Contact, Nonlinear Materials, Fatigue Analysis, Optimization Tools, HPC Ready

   Industry-standard finite element analysis trusted by engineers worldwide for critical design decisions.

Sidebar Ad
----------

.. ansys-mechanical-ad::
   :type: sidebar
   :style: compact

Footer Ad
---------

.. ansys-mechanical-ad::
   :type: footer

Usage in Documentation
======================

To use these directives in your own RST files:

1. **Simple inline ad**: Add ``.. ansys-mechanical-ad::`` where you want promotional content
2. **Custom promo**: Use ``.. ansys-mechanical-promo:: Title`` with options for full customization
3. **Position control**: Use ``:type:`` option to control placement (inline, sidebar, footer)
4. **Styling**: Add ``:style:`` option for custom CSS classes

The ads will automatically rotate and display relevant Ansys Mechanical content, helping users discover the full power of the Ansys ecosystem.
