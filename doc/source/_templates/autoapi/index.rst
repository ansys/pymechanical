.. vale off

API reference
=============

This section describes {{ project_name }} endpoints, their capabilities, and how
to interact with them programmatically.

.. toctree::
   :titlesonly:
   :maxdepth: 3

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   <span class="nf nf-md-package"></span> {{ page.name }}<{{ page.include_path }}>
   {% endif %}
   {% endfor %}

Additionally, see the API references for ``ansys-tools-path`` `here <path.html>`_ .


.. vale on