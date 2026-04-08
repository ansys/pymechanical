
.. title:: PyMechanical

.. image:: /_static/logo/pymechanical-logo-light.png
   :class: only-light
   :alt: PyMechanical Logo Light
   :width: 580px
   :align: center

.. image:: /_static/logo/pymechanical-logo-dark.png
   :class: only-dark
   :alt: PyMechanical Logo Dark
   :width: 580px
   :align: center


Python API to interact with `Ansys Mechanical`_ (FEA software for structural engineering) in **2024 R2 and later**.


PyMechanical provides two distinct modes of interacting with Mechanical.
Choose the one that fits your workflow:

.. grid:: 2

    .. grid-item-card:: Embedding mode :fa:`microchip`
        :padding: 2 2 2 2
        :link: user_guide/embedding/overview
        :link-type: doc
        :class-card: sd-border-warning
        :class-title: sd-font-weight-bold sd-text-warning sd-fs-5

        Run Mechanical **directly in your Python process** with the ``App`` class.
        Provides full object-model access, fast startup, and is ideal for Jupyter notebooks
        and interactive scripting.

        .. code-block:: python

            from ansys.mechanical.core import App
            app = App(globals=globals()) #always batch mode
            print(app)

            Model.AddStaticStructuralAnalysis()

        :bdg-warning:`In-process` :bdg-warning:`Direct API` :bdg-warning:`fast`

    .. grid-item-card:: Remote session mode :fa:`server`
        :padding: 2 2 2 2
        :link: user_guide/remote_session/overview
        :link-type: doc
        :class-card: sd-border-warning
        :class-title: sd-font-weight-bold sd-text-warning sd-fs-5

        Launch Mechanical as a **separate server process** and communicate with gRPC.
        Provides process isolation, and optional GUI, and is ideal for CI/CD, Docker and automation.

        .. code-block:: python

            from ansys.mechanical.core import launch_mechanical
            app = launch_mechanical() # either batch or GUI mode
            print(app)

            app.run_python_script("Model.AddStaticStructuralAnalysis()")

        :bdg-warning:`gRPC` :bdg-warning:`GUI` :bdg-warning:`Remote`

If you are not sure which mode to pick, see :doc:`getting_started/choose_your_mode`.

----

.. grid:: 3


    .. grid-item-card:: Getting started :fa:`person-running`
        :padding: 2 2 2 2
        :link: getting_started/index
        :link-type: doc

        Install PyMechanical, choose your mode, and run your first script.

        :bdg-warning-line:`Install` :bdg-warning-line:`Choose mode` :bdg-warning-line:`Quick start`

    .. grid-item-card:: User Guide :fa:`window-maximize`
        :padding: 2 2 2 2
        :link: user_guide/index
        :link-type: doc

        Learn how to use embedding mode, remote sessions, scripting, and CLI tools.

        :bdg-warning-line:`Embedding` :bdg-warning-line:`Remote` :bdg-warning-line:`Scripting`

    .. grid-item-card:: Examples :fa:`scroll`
        :padding: 2 2 2 2
        :link: examples/index
        :link-type: doc

        Explore examples, which are organized by mode and simulation type.

        :bdg-warning-line:`Embedding` :bdg-warning-line:`Remote` :bdg-warning-line:`Advanced`

    .. grid-item-card:: API reference :fa:`book-bookmark`
        :padding: 2 2 2 2
        :link: api/index
        :link-type: doc

        Understand PyMechanical API endpoints and their capabilities.

        :bdg-warning-line:`Classes` :bdg-warning-line:`Methods` :bdg-warning-line:`Error handling`


    .. grid-item-card:: FAQs :fa:`fa-solid fa-circle-question`
        :padding: 2 2 2 2
        :link: faq
        :link-type: doc

        Frequently asked questions and their answers.

        :bdg-warning-line:`How` :bdg-warning-line:`Why` :bdg-warning-line:`What`

    .. grid-item-card:: Known issues and limitations :fa:`fa-solid fa-bug`
        :padding: 2 2 2 2
        :link: kil/index
        :link-type: doc

        See issues and limitations for both PyMechanical and Mechanical.

        :bdg-warning-line:`24R2` :bdg-warning-line:`25R1` :bdg-warning-line:`25R2` :bdg-warning-line:`26R1`

    .. grid-item-card:: Contribute :fa:`people-group`
        :padding: 2 2 2 2
        :link: contribute
        :link-type: doc

        Learn how to contribute to the PyMechanical codebase
        or documentation.

        :bdg-warning-line:`Test` :bdg-warning-line:`Documentation` :bdg-warning-line:`Issues`


.. toctree::
   :hidden:
   :maxdepth: 3

   getting_started/index
   user_guide/index
   examples/index
   API reference <api/ansys/mechanical/core/index>
   contribute
   faq
   kil/index
   changelog