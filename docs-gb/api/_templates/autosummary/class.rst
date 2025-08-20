
{{ fullname }}
{{ "=" * fullname|length }}

.. currentmodule:: {{ module }}

.. _{{ fullname|replace(".", "-") }}:

**Module:** ``{{ module }}``  
**Class:** ``{{ objname }}``{% if bases %}  
**Bases:** {{ ", ".join(bases) }}{% endif %}

.. note::
   This page was auto-generated. Edit the docstring of ``{{ fullname }}`` for content changes.

Overview
--------

.. autoclass:: {{ fullname }}
   :show-inheritance:
   :member-order: bysource
   :special-members: __init__
   :inherited-members:
   :undoc-members:

Quick Reference
---------------

:ref:`Jump to Methods <{{ fullname|replace(".", "-") }}-methods>` ·
:ref:`Jump to Attributes <{{ fullname|replace(".", "-") }}-attributes>`{% if methods or attributes %} ·
:ref:`All Members <{{ fullname|replace(".", "-") }}-members>`{% endif %}

Signature
---------

.. autodata:: {{ fullname }}.__init__
   :no-value:

Source Link
-----------

.. rubric:: Where did this come from?

If :mod:`sphinx.ext.linkcode` is enabled, a "View source" link will appear near the class and members in GitBook.

.. _{{ fullname|replace(".", "-") }}-members:

All Members
-----------

.. autosummary::
   :toctree:
   :nosignatures:
   :template: attribute.rst
   {% for item in members %}
   {{ item }}
   {% endfor %}

.. _{{ fullname|replace(".", "-") }}-methods:

Methods
-------

.. autosummary::
   :toctree:
   :nosignatures:
   :template: method.rst
   {% for item in methods %}
   {{ item }}
   {% endfor %}

.. _{{ fullname|replace(".", "-") }}-attributes:

Attributes
----------

.. autosummary::
   :toctree:
   :nosignatures:
   :template: attribute.rst
   {% for item in attributes %}
   {{ item }}
   {% endfor %}

