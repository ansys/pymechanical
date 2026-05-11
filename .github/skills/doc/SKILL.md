---
name: doc
description: 'Write, review, or edit PyMechanical documentation. Use when writing reStructuredText (RST) files, Python docstrings, Sphinx configurations, example scripts, README files, or any doc content for the PyMechanical library. This covers NumPy docstrings, RST file formatting, Google developer style guide rules, Sphinx extensions, Vale linting, and content structure.'
---
`
# PyMechanical Documentation Standards

All PyMechanical documentation follows the standards defined in the
[PyAnsys developer guide](https://dev.docs.pyansys.com). Apply these rules when writing or
reviewing documentation in any PyAnsys library.

---

## Writing Style (Google Developer Documentation Style Guide)

All prose in RST files, docstrings, and README files must follow the
[Google developer documentation style guide](https://developers.google.com/style):

- **Sentence case** for all headings and titles (capitalize first word and proper nouns only)
- **Active voice** and **present tense** wherever possible
- **Second person** — use "you"/"your"; avoid "we"
- **Short sentences** — one idea per sentence. Avoid semicolons. Break into two sentences instead.
- **American English** spelling and punctuation
- Omit "please" from instructions
- Replace "In order to" with "To"
- Vale enforces these rules in CI/CD (`doc/.vale.ini`)

---

## RST File Formatting

### Headings

Use this character hierarchy (must be at least as long as the heading text):

```rst
###############
Part title
###############

Section title
=============

Subsection
----------

Sub-subsection
~~~~~~~~~~~~~~

Sub-sub-subsection
++++++++++++++++++
```

### General Rules

- One blank line between paragraphs
- Blank line before and after every list
- No trailing whitespace; spaces not tabs for indentation
- Max line length follows library convention (commonly 79–120 chars)
- Use `..` prefix for RST comments; use `.. todo::` directive for tracked items

### Inline Formatting

| Need | RST syntax | Notes |
|------|-----------|-------|
| Code entities | `` ``double backticks`` `` | Functions, classes, variables — **never** single backtick (renders italic) |
| Bold | `**text**` | Use for UI elements; otherwise, use sparingly |
| Italic | `*text*` | Use for introducing terms |

### Code Blocks

```rst
.. code-block:: python

   import ansys.mechanical.core as pymechanical
   app = pymechanical.launch_mechanical()
```

Use `.. code-block:: console` for shell commands, `.. code-block:: python` for Python.

### Notices / Admonitions

```rst
.. note::

   Use notes for helpful but non-critical information.

.. warning::

   Use warnings for content that could cause data loss or unexpected behavior.

.. important::

   Use for critical information that must not be missed.
```

### Cross-References and Links

- Use Sphinx `:ref:` labels for internal cross-references: `` :ref:`my_label` ``
- Use `:func:`, `:class:`, `:meth:`, `:attr:` for API cross-references
- Use `.. _label_name:` above headings to define reference targets
- Use the `` `Link text <https://url>`_`` format for external URLs. The link text should match exact name of the article or section that the link takes you to, including capitalization. If the referenced content is within a larger document, append that for clarity. For example: For more information on creating NumPy arrays, see
`Array creation <https://numpy.org/doc/stable/user/basics.creation.html>`_ in the NumPy documentation.

### Images

```rst
.. figure:: /path/to/image.png
   :alt: Descriptive alt text
   :width: 500px

   Caption in sentence case.
```

---

## Documentation Content Structure

Every PyAnsys library documentation should have these top-level sections:

| Section | Purpose |
|---------|---------|
| **Getting started** | Installation, prerequisites, first steps |
| **User guide** | Conceptual explanations, how-to guides |
| **API reference** | Auto-generated from docstrings (AutoAPI or autodoc) |
| **Examples** | Standalone example scripts via Sphinx-Gallery |
| **Contribute** | Contribution workflow, coding and doc style links |

Toctree in `doc/source/index.rst` drives the top-level hierarchy. Each section has its own
`index.rst` with a local `toctree`. Section index filenames: short, descriptive, hyphen-separated.

---

## Python Docstrings (NumPy Style)

PyAnsys libraries use **NumPy-style docstrings** (not Google-style). NumPy style is preferred
because it is used by NumPy, SciPy, and pandas — the primary dependencies.

### Required Rules

- Always use triple double-quotes `"""` — never single quotes
- Lines ≤ 100 characters (keeps API summary tables readable)
- No trailing whitespace
- Use `""` for code entities (not `''` — single backtick renders italic in Sphinx)

### Sections Order

```
Short summary
Deprecation warning (if applicable)
Extended summary (if applicable)
Parameters (if applicable)
Returns (if applicable)
Raises (if applicable)
Examples (always required)
```

Sections rarely used in PyAnsys: `Yields`, `Receives`, `Other Parameters`, `Warns`,
`Warnings`, `See Also`, `Notes`, `References`.

### Short Summary Rules

| Object | Verb rule | Example |
|--------|-----------|---------|
| **Class** | Verb ending in **"s"** | `"""Provides the EMIT application interface."""` |
| **Method / function** | Verb **not** ending in "s" | `"""Export mesh statistics to a file."""` |
| **`@property`** | Noun phrase | `"""Path to the working directory."""` |

### Parameters Section

```python
Parameters
----------
obj : str
    Name of the object to assign the material to.
mat : str
    Name of the material.
timeout : float, optional
    Time in seconds to wait. The default is ``30``.
```

- Mark optional parameters with `, optional`
- Describe the default behavior for optional parameters
- Use `The default is ``value``.` at the end of optional parameter descriptions

### Returns Section

```python
Returns
-------
bool
    ``True`` when successful, ``False`` when failed.
str
    Path to the exported file.
```

### Examples Section

Examples **must be doctest-compliant** — they are run as regression tests via pytest
(`addopts = "--doctest-modules"` in `pyproject.toml`).

```python
Examples
--------
Launch a Mechanical instance and get its version.

>>> import ansys.mechanical.core as pymechanical
>>> app = pymechanical.launch_mechanical()
>>> app.version
"2024 R1"
```

### `@property` Docstring

No `Parameters` section. No docstring on the setter. Described as a noun.

```python
@property
def working_directory(self):
    """Path to the working directory."""
    return self._working_directory
```

### Protected Methods

Protected methods (single leading underscore `_`) still need clear docstrings even though
Sphinx does not render them publicly.


## Deprecation

When deprecating a method or class:

1. Have the old method call the new method and raise `DeprecationWarning`
2. Add a `.. deprecated::` directive in the docstring
3. After a minor release or two, raise `AttributeError` or a custom `DeprecationError`

```python
import warnings

class FieldAnalysis2D:
    def assignmaterial(self, obj, mat):
        """Assign a material to one or more objects.

        .. deprecated:: 0.4.0
           Use :func:`FieldAnalysis2D.assign_material` instead.

        Parameters
        ----------
        obj : str
            Name of the object.
        mat : str
            Name of the material.
        """
        warnings.warn(
            "`assignmaterial` is deprecated. Use `assign_material` instead.",
            DeprecationWarning,
        )
        self.assign_material(obj, mat)
```

For full removal, raise a custom error:

```python
class DeprecationError(RuntimeError):
    """Used for deprecated methods and functions."""

    def __init__(self, message="This feature has been deprecated."):
        RuntimeError.__init__(self, message)
```


## Documentation Tooling

| Tool | Purpose | Key usage |
|------|---------|-----------|
| `blacken-docs` | Format code blocks in RST | `blacken-docs -l 100 doc/**/*.rst` |
| `codespell` | Fix common misspellings | `codespell --write-changes --ignore-words=<FILE>` |
| `docformatter` | Format docstrings per PEP 257 | `docformatter -r -i --wrap-summaries 100 --wrap-descriptions 100` |
| `numpydoc` | Validate NumPy-style docstrings via Sphinx | `numpydoc_validation_checks = {"GL08"}` in `conf.py` |
| `interrogate` | Measure docstring coverage | `[tool.interrogate]` in `pyproject.toml` |
| `Vale` | Prose linting for RST/MD | `.vale.ini` in `doc/`; enforces Google style guide + Ansys custom rules |

### Vale Commands

```bash
vale --config=doc/.vale.ini sync    # Download/update styles
vale --config=doc/.vale.ini .       # Check whole repo
vale --config=doc/.vale.ini doc/source/   # Check only doc directory
```

---

## Sphinx Build Configuration

Minimum required `SPHINXOPTS` flags in `Makefile` / `make.bat`:

| Flag | Purpose |
|------|---------|
| `-j auto` | Auto-detect CPU cores for parallel builds |
| `-W` | Treat warnings as errors |
| `--keep-going` | Continue rendering even after a warning |

---

## Coding Style Quick Reference (for Code in Docs)

All code in examples and docstrings must follow PEP 8:

- **Line length:** 100 characters (configured via `ruff`)
- **Imports:** stdlib → third-party → local; one import per line; no wildcard imports
- **Naming:** `snake_case` for functions/methods/variables, `CamelCase` for classes,
  `UPPER_CASE` for constants, `lowercase` for packages/modules
- **Strings:** double quotes (configured via `ruff`)
- **Indentation:** 4 spaces, no tabs

---

## README Files

- Prefer `.rst` over `.md` — RST content can be reused in Sphinx docs via `.. include::`
- MD content cannot be included in RST files
- Partial reuse: use `:start-after:` / `:end-before:` with explicit RST targets for selective inclusion
