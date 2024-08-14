
.. image:: /_static/logo/pymechanical-logo-light.png
   :class: only-light
   :alt: PyMechanical Logo
   :width: 580px

.. image:: /_static/logo/pymechanical-logo-dark.png
   :class: only-dark
   :alt: PyMechanical
   :width: 580px


Provides a Python API to interact with `Ansys Mechanical`_ from **23R2** and later.

.. grid:: 1 2 2 2


    .. grid-item-card:: Getting started :fa:`person-running`
        :padding: 2 2 2 2
        :link: getting_started/index
        :link-type: doc

        Learn how to install and use PyMechanical. Explains architecture
        and background.

        :bdg-primary-line:`install` :bdg-primary-line:`architecture` :bdg-primary-line:`docker` :bdg-primary-line:`wsl`

    .. grid-item-card:: Examples :fa:`scroll`
        :padding: 2 2 2 2
        :link: example/index
        :link-type: doc

        Dive into examples created using PyMechanical.

        :bdg-primary-line:`basic` :bdg-primary-line:`technology-showcase` :bdg-primary-line:`tips`

    .. grid-item-card:: Embedding instance :fa:`book-open-reader`
        :padding: 2 2 2 2
        :link: user_guide_embedding/index
        :link-type: doc

        Using Python.NET, a Mechanical object implemented in .NET is directly loaded into Python memory,
        making the entire Mechanical data model accessible from Python code without starting a new process.

        :bdg-primary-line:`Python.NET` :bdg-primary-line:`no-GUI`

    .. grid-item-card:: Remote session :fa:`people-group`
        :padding: 2 2 2 2
        :link: user_guide_session/index
        :link-type: doc

        Using gRPC, Mechanical operates as a server, ready to respond to client requests.
        PyMechanical provides a client to connect to the Mechanical server and make API calls.

        :bdg-primary-line:`gRPC` :bdg-primary-line:`GUI`

    .. grid-item-card:: API reference :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: api/index
        :link-type: doc

        Understand PyMechanical API endpoints and their capabilities

    .. grid-item-card:: API reference :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: api/index
        :link-type: doc

        Understand PyMechanical API endpoints and their capabilities

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