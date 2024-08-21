
.. image:: /_static/logo/pymechanical-logo-light.png
   :class: only-light
   :alt: PyMechanical Logo
   :width: 580px

.. image:: /_static/logo/pymechanical-logo-dark.png
   :class: only-dark
   :alt: PyMechanical
   :width: 580px


Provides a Python API to interact with `Ansys Mechanical`_ from **23R2** and later.

.. grid:: 3


    .. grid-item-card:: Getting started :fa:`person-running`
        :padding: 2 2 2 2
        :link: getting_started/index
        :link-type: doc

        Learn how to install and use PyMechanical. Explains architecture
        and background.

        :bdg-primary-line:`install` :bdg-primary-line:`architecture` :bdg-primary-line:`docker`

    .. grid-item-card:: Examples :fa:`scroll`
        :padding: 2 2 2 2
        :link: example/index
        :link-type: doc

        Dive into examples created using PyMechanical.

        :bdg-primary-line:`basic` :bdg-primary-line:`technology-showcase` :bdg-primary-line:`tips`

    .. grid-item-card:: API reference :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: api/index
        :link-type: doc

        Understand PyMechanical API endpoints and their capabilities

        :bdg-primary-line:`ansys.mechanical.core`


    .. grid-item-card:: Embedding instance :fa:`window-maximize`
        :padding: 2 2 2 2
        :link: user_guide_embedding/index
        :link-type: doc

        A Mechanical object implemented in .NET is directly loaded into Python memory.

        :bdg-primary-line:`Python.NET` :bdg-primary-line:`no-GUI`

    .. grid-item-card:: Remote session :fa:`window-restore`
        :padding: 2 2 2 2
        :link: user_guide_session/index
        :link-type: doc

        Using gRPC, Mechanical operates as a server, ready to respond to client requests.

        :bdg-primary-line:`gRPC` :bdg-primary-line:`GUI`


    .. grid-item-card:: Mechanical scripting :fa:`code`
        :padding: 2 2 2 2
        :link: user_guide_scripting/index
        :link-type: doc

        Overview of Mechanical scripting.

        :bdg-primary-line:`ACT` :bdg-primary-line:`threading`

    .. grid-item-card:: FAQs :fa:`fa-solid fa-circle-question`
        :padding: 2 2 2 2
        :link: faq
        :link-type: doc

        Frequently asked questions and their answers.

    .. grid-item-card:: Known issues and limitations :fa:`fa-solid fa-bug`
        :padding: 2 2 2 2
        :link: kil/index
        :link-type: doc

        Issues and limitations on both PyMechanical and Mechanical.

        :bdg-primary-line:`23R2` :bdg-primary-line:`24R1` :bdg-primary-line:`24R2`

    .. grid-item-card:: Contribute :fa:`people-group`
        :padding: 2 2 2 2
        :link: contributing
        :link-type: doc

        Learn how to contribute to the PyMechanical codebase
        or documentation.


.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   examples/index
   user_guide_session/index
   user_guide_embedding/index
   user_guide_scripting/index
   api/index
   kil/index
   faq
   contributing
   changelog