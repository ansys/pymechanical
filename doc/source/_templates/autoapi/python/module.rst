.. vale off

{# ------------------------- Begin macros definition ----------------------- #}

{% macro tab_item_from_objects_list(objects_list, title="") -%}

    .. tab-item:: {{ title }}

        .. list-table::
          :header-rows: 0
          :widths: auto

          {% for obj in objects_list %}

              {% if obj.type in own_page_types %}
          * - :py:obj:`~{{ obj.id }}`
              {% else %}
          * - :py:obj:`~{{ obj.short_name }}`
              {% endif %}
            - {{ obj.summary }}

          {% endfor %}

{%- endmacro %}

{% macro toctree_from_objects_list(objects_list, icon="") -%}

.. toctree::
   :titlesonly:
   :maxdepth: 1
   :hidden:

    {% for obj in objects_list %}
    <span class="{{ icon }}"></span> {{ obj.short_name }}<{{ obj.include_path }}>
    {% endfor %}
{%- endmacro %}

{# --------------------------- End macros definition ----------------------- #}

{% if not obj.display %}
:orphan:
{% endif %}

{% if is_own_page %}

    {% if obj.name.split(".") | length == 3 %}
The ``{{ obj.name }}`` library
{{ "================" + "=" * obj.name|length }}
    {% else %}
    {% if obj.type == "package" %}
The ``{{ obj.short_name }}`` package
{{ "====================" + "=" * obj.short_name|length }}
    {% else %}
The ``{{ obj.short_name }}.py`` module
{{ "==================" + "=" * obj.short_name|length }}
    {% endif %}
    {% endif %}
{% endif %}

.. py:module:: {{ obj.name }}

{# ---------------------- Begin module summary -------------------- #}

Summary
-------

{% if obj.all is not none %}
{% set visible_children = obj.children|selectattr("short_name", "in", obj.all)|list %}
{% elif obj.type is equalto("package") %}
{% set visible_children = obj.children|selectattr("display")|list %}
{% else %}
{% set visible_children = obj.children|selectattr("display")|rejectattr("imported")|list %}
{% endif %}

{% set visible_subpackages = obj.subpackages|selectattr("display")|list %}
{% set visible_submodules = obj.submodules|selectattr("display")|list %}

{% set visible_classes_and_interfaces = visible_children|selectattr("type", "equalto", "class")|list %}
{% set visible_functions = visible_children|selectattr("type", "equalto", "function")|list %}
{% set visible_attributes_and_constants = visible_children|selectattr("type", "equalto", "data")|list %}
{% set visible_exceptions = visible_children|selectattr("type", "equalto", "exception")|list %}

{% set visible_classes = [] %}
{% set visible_interfaces = [] %}
{% set visible_enums = [] %}
{% for element in visible_classes_and_interfaces %}

    {#
        HACK: there is not built-in "startswith" test, no "break" statement, and
        no limited scope for variables inside blocks, see:
        https://stackoverflow.com/questions/4870346/can-a-jinja-variables-scope-extend-beyond-in-an-inner-block
    #}
    {% set has_enum_base = [] %}
    {% for base in element.bases %}
        {% if base.startswith("enum.") %}
            {% set _ = has_enum_base.append(true) %}
        {% endif %}
    {% endfor %}

    {% if has_enum_base %}
        {% set _ = visible_enums.append(element) %}
    {% elif element.name.startswith("I") and element.name[1].isupper() and not has_enum_base %}
        {% set _ = visible_interfaces.append(element) %}
    {% else %}
        {% set _ = visible_classes.append(element) %}
    {% endif %}
{% endfor %}

{% set visible_attributes = [] %}
{% set visible_constants = [] %}
{% for element in visible_attributes_and_constants %}
    {% if element.name.isupper() %}
        {% set _ = visible_constants.append(element) %}
    {% else %}
        {% set _ = visible_attributes.append(element) %}
    {% endif %}
{% endfor %}

{% set module_objects = visible_subpackages + visible_submodules + visible_classes + visible_interfaces + visible_enums + visible_exceptions + visible_functions + visible_constants + visible_attributes %}

{# ---------------------- End module summary -------------------- #}
{# ---------------------- Begin module tabset -------------------- #}
{% if module_objects %}

.. py:currentmodule:: {{ obj.short_name }}
.. tab-set::

{% if visible_subpackages %}
    {{ tab_item_from_objects_list(visible_subpackages, "Subpackages") }}
{% endif %}

{% if visible_submodules %}
    {{ tab_item_from_objects_list(visible_submodules, "Submodules") }}
{% endif %}

{% if visible_interfaces %}
    {{ tab_item_from_objects_list(visible_interfaces, "Interfaces") }}
{% endif %}

{% if visible_classes %}
    {{ tab_item_from_objects_list(visible_classes, "Classes") }}
{% endif %}

{% if visible_enums %}
    {{ tab_item_from_objects_list(visible_enums, "Enums") }}
{% endif %}

{% if visible_exceptions %}
    {{ tab_item_from_objects_list(visible_exceptions, "Exceptions") }}
{% endif %}

{% if visible_functions %}
    {{ tab_item_from_objects_list(visible_functions, "Functions") }}
{% endif %}

{% if visible_attributes %}
    {{ tab_item_from_objects_list(visible_attributes, "Attributes") }}
{% endif %}

{% if visible_constants %}
    {{ tab_item_from_objects_list(visible_constants, "Constants") }}
{% endif %}
{% endif %}

{# ---------------------- End module tabset -------------------- #}
{# ------------------------ Begin toctree definition ----------------------- #}

{% block subpackages %}
{% if visible_subpackages %}
{{ toctree_from_objects_list(visible_subpackages, "nf nf-md-package") }}
{% endif %}
{% endblock %}

{% block submodules %}
{% if visible_submodules %}
{{ toctree_from_objects_list(visible_submodules, "nf nf-fa-file") }}
{% endif %}
{% endblock %}

{% block class %}
{% if own_page_types and "class" in own_page_types %}
{% if visible_interfaces %}
{{ toctree_from_objects_list(visible_interfaces, "nf nf-cod-symbol_interface") }}
{% endif %}

{% if visible_classes %}
{{ toctree_from_objects_list(visible_classes, "nf nf-cod-symbol_class") }}
{% endif %}

{% if visible_enums %}
{{ toctree_from_objects_list(visible_enums, "nf nf-cod-symbol_enum") }}
{% endif %}

{% if visible_exceptions %}
{{ toctree_from_objects_list(visible_exceptions, "nf nf-md-lightning_bolt") }}
{% endif %}
{% endif %}
{% endblock %}

{% block functions %}
{% if own_page_types and visible_functions and "function" in own_page_types %}
{{ toctree_from_objects_list(visible_functions, "nf nf-md-function_variant") }}
{% endif %}
{% endblock %}

{% block constants %}
{% if own_page_types and visible_constants and "constant" in own_page_types %}
{{ toctree_from_objects_list(visible_constants, "nf nf-cod-symbol_constant") }}
{% endif %}
{% endblock %}

{# ------------------------- End toctree definition ------------------------ #}


{# ------------------------ Begin module description ----------------------- #}

{% if obj.docstring %}
Description
-----------

{{ obj.docstring }}
{% endif %}

{# ------------------------- End module description ------------------------ #}


{# -------------------------- Begin module detail -------------------------- #}

{% set module_objects_in_this_page = visible_classes + visible_interfaces + visible_enums + visible_exceptions + visible_functions + visible_constants + visible_attributes %}
{% if module_objects_in_this_page %}
{% set visible_objects_in_this_page = [] %}

{% if own_page_types %}
    {% for obj in module_objects_in_this_page %}
        {% if obj.type not in own_page_types %}
        {% set _ = visible_objects_in_this_page.append(obj) %}
        {% endif %}
    {% endfor %}
{% else %}
    {% set visible_objects_in_this_page = module_objects_in_this_page %}
{% endif %}

{% if visible_objects_in_this_page %}
Module detail
-------------

    {% for obj in visible_objects_in_this_page %}
{{ obj.render() }}
    {% endfor %}

{% endif %}
{% endif %}

{# ---------------------- End module detail description -------------------- #}

.. vale on