.. vale off

API reference
=============

This section describes {{ project_name }} endpoints, their capabilities, and how
to interact with them programmatically. See the API reference for ``ansys-tools-path``
`here <path.html>`_.

.. toctree::
   :titlesonly:
   :maxdepth: 3

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   <span class="nf nf-md-package"></span> {{ page.name }}<{{ page.include_path }}>
   {% endif %}
   {% endfor %}

.. vale on