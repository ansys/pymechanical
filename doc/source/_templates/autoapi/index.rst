API reference
=============

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item-card:: PyMechanical API reference :fa:`book-bookmark`
      :padding: 2 2 2 2
      :link: ansys/mechanical/core/index
      :link-type: doc

      Understand ``{{ project_name }}`` endpoints, their capabilities, and how
      to interact with them programmatically.

      :bdg-info:`Classes` :bdg-info:`Methods` :bdg-info:`Error handling`

   .. grid-item-card:: Mechanical scripting API :fa:`code`
      :padding: 2 2 2 2
      :link: https://scripting.mechanical.docs.pyansys.com/version/stable/api/ansys/mechanical/stubs/v261/index.html

      Browse the full Mechanical 2026 R1 scripting API — objects,
      methods, and properties exposed inside Mechanical.

      :bdg-info:`Mechanical API` :bdg-info:`2026 R1`

.. toctree::
   :titlesonly:
   :maxdepth: 3
   :hidden:

   {% for page in pages %}
   {% set length = autoapi_depth | int %}
   {% if (page.top_level_object or page.name.split('.') | length == length) and page.display %}
   <span class="nf nf-md-package"></span> {{ page.name }}<{{ page.include_path }}>
   {% endif %}
   {% endfor %}
