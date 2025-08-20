{{ objname }}
============

.. currentmodule:: {{ module }}

**Qualified name:** ``{{ fullname }}``{% if bases %}  
**Bases:** {{ ", ".join(bases) }}{% endif %}

Overview
--------
.. autoclass:: {{ fullname }}
   :noindex:
   :member-order: bysource

{# Normalize helpers: attributes/methods may be strings or objects #}
{% set _attrs = attributes or [] %}
{% set _meths = methods or [] %}

{% if "__init__" in (_meths if _meths and (_meths[0] is string) else (_meths | map(attribute="name") | list)) %}
Constructor
-----------
.. automethod:: {{ fullname }}.__init__
   :noindex:
{% endif %}

{% set has_pub_attrs = false %}
{% for a in _attrs %}
  {% set aname = a if (a is string) else a.name %}
  {% if not aname.startswith('_') %}{% set has_pub_attrs = true %}{% endif %}
{% endfor %}

{% if has_pub_attrs %}
Fields
------
{% for a in _attrs %}
  {% set aname = a if (a is string) else a.name %}
  {% if not aname.startswith('_') %}
.. autoattribute:: {{ fullname }}.{{ aname }}
   :noindex:
  {% endif %}
{% endfor %}
{% endif %}

{% set has_pub_methods = false %}
{% for m in _meths %}
  {% set mname = m if (m is string) else m.name %}
  {% if not mname.startswith('_') and mname != "__init__" %}{% set has_pub_methods = true %}{% endif %}
{% endfor %}

{% if has_pub_methods %}
Methods
-------
{% for m in _meths %}
  {% set mname = m if (m is string) else m.name %}
  {% if not mname.startswith('_') and mname != "__init__" %}
.. automethod:: {{ fullname }}.{{ mname }}
   :noindex:
  {% endif %}
{% endfor %}
{% endif %}
