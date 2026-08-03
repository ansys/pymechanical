
.. title:: PyMechanical

.. raw:: html

   <div class="pymechanical-banner">
     <div class="pymechanical-banner-content">
       <h2>PyMechanical</h2>
       <p>
         Python API to interact with Ansys Mechanical (2024 R2 or later) for,
         making automation, scripting, and integration easier for engineers and developers.
       </p>
       <a href="getting_started/index.html" class="btn-banner">Get started</a>
       <a href="user_guide/index.html" class="btn-banner">User guide</a>
       <a href="examples/index.html" class="btn-banner">Examples</a>
       <a href="api/ansys/mechanical/core/index.html" class="btn-banner">API reference</a>
       <a href="faq.html" class="btn-banner">FAQs</a>
       <a href="kil/index.html" class="btn-banner">Known issues</a>
       <a href="contribute.html" class="btn-banner">Contribute</a>
     </div>
   </div>



PyMechanical provides two distinct modes of interacting with Mechanical.
Choose the one that fits your workflow:

.. grid:: 2

    .. grid-item-card:: Embedding mode :fa:`microchip`
        :padding: 2 2 2 2
        :link: user_guide/embedding/overview
        :link-type: doc
        :class-card: sd-border-info
        :class-title: sd-font-weight-bold sd-text-info sd-fs-5

        Run Mechanical **directly in your Python process** with the ``App`` class.
        Provides full object-model access, fast startup, and is ideal for Jupyter notebooks
        and interactive scripting.

        .. code-block:: python

            from ansys.mechanical.core import App
            app = App(globals=globals()) #always batch mode
            print(app)

            Model.AddStaticStructuralAnalysis()

        :bdg-info:`In-process` :bdg-info:`Direct API` :bdg-info:`fast`

    .. grid-item-card:: Remote session mode :fa:`server`
        :padding: 2 2 2 2
        :link: user_guide/remote_session/overview
        :link-type: doc
        :class-card: sd-border-info
        :class-title: sd-font-weight-bold sd-text-info sd-fs-5

        Launch Mechanical as a **separate server process** and communicate with gRPC.
        Provides process isolation, and optional GUI, and is ideal for CI/CD, Docker and automation.

        .. code-block:: python

            from ansys.mechanical.core import launch_mechanical
            app = launch_mechanical() # either batch or GUI mode
            print(app)

            app.run_python_script("Model.AddStaticStructuralAnalysis()")

        :bdg-info:`gRPC` :bdg-info:`GUI` :bdg-info:`Remote`

If you are not sure which mode to pick, see :doc:`getting_started/choose_your_mode`.

.. raw:: html

   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />

   <section class="examples-grid-section">
     <h2 class="examples-grid-heading">
       Examples gallery
       <a href="examples/index.html" class="examples-more-link">All examples</a>
     </h2>
     <div class="swiper examples-swiper">
       <div class="swiper-wrapper">

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/bolt_pretension.html">
             <img class="example-thumb" src="_images/sphx_glr_bolt_pretension_thumb.png" alt="Bolt pretension" />
             <div class="example-card-body">
               <p class="example-card-title">Bolt pretension</p>
               <p class="example-card-desc">Defines and solves a bolt-pretension analysis, then evaluates deformation, stress, contact, and bolt results.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/cooling_holes_thermal_analysis.html">
             <img class="example-thumb" src="_images/sphx_glr_cooling_holes_thermal_analysis_thumb.png" alt="Cooling holes thermal analysis" />
             <div class="example-card-body">
               <p class="example-card-title">Cooling holes thermal analysis</p>
               <p class="example-card-desc">Simulates steady-state thermal behavior of turbine blade cooling holes using Fluid116 elements.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/fracture_analysis_contact_debonding.html">
             <img class="example-thumb" src="_images/sphx_glr_fracture_analysis_contact_debonding_thumb.png" alt="Fracture analysis contact debonding" />
             <div class="example-card-body">
               <p class="example-card-title">Fracture analysis</p>
               <p class="example-card-desc">Demonstrates contact debonding with VCCT and CZM fracture models.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/harmonic_acoustics.html">
             <img class="example-thumb" src="_images/sphx_glr_harmonic_acoustics_thumb.png" alt="Harmonic acoustic analysis" />
             <div class="example-card-body">
               <p class="example-card-title">Harmonic acoustic analysis</p>
               <p class="example-card-desc">Performs harmonic acoustic analysis of a fluid-filled container driven by a pressure load.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/modal_acoustics_analysis.html">
             <img class="example-thumb" src="_images/sphx_glr_modal_acoustics_analysis_thumb.png" alt="Modal acoustics analysis" />
             <div class="example-card-body">
               <p class="example-card-title">Modal acoustics analysis</p>
               <p class="example-card-desc">Runs modal acoustic analysis of a fluid-filled container with acoustic-structural coupling.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/steady_state_thermal_analysis.html">
             <img class="example-thumb" src="_images/sphx_glr_steady_state_thermal_analysis_thumb.png" alt="Steady state thermal analysis" />
             <div class="example-card-body">
               <p class="example-card-title">Steady state thermal analysis</p>
               <p class="example-card-desc">Applies convection and heat flux boundary conditions and solves a steady-state thermal problem.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/topology_optimization_cantilever_beam.html">
             <img class="example-thumb" src="_images/sphx_glr_topology_optimization_cantilever_beam_thumb.png" alt="Topology optimization" />
             <div class="example-card-body">
               <p class="example-card-title">Topology optimization</p>
               <p class="example-card-desc">Performs structural topology optimization of a cantilever beam to minimize compliance.</p>
             </div>
           </a>
         </div>

         <div class="swiper-slide">
           <a class="example-card" href="examples/gallery_examples/01_basic/valve.html">
             <img class="example-thumb" src="_images/sphx_glr_valve_thumb.png" alt="Basic valve" />
             <div class="example-card-body">
               <p class="example-card-title">Basic valve</p>
               <p class="example-card-desc">Implements a basic valve with remote points and evaluates the structural response.</p>
             </div>
           </a>
         </div>

       </div>
       <div class="swiper-pagination examples-pagination"></div>
     </div>
   </section>

   <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
   <script>
     new Swiper(".examples-swiper", {
       slidesPerView: 4,
       spaceBetween: 16,
       loop: true,
       autoplay: { delay: 3000, disableOnInteraction: false },
       pagination: { el: ".examples-pagination", clickable: true },
       breakpoints: {
         320:  { slidesPerView: 1, spaceBetween: 12 },
         768:  { slidesPerView: 2, spaceBetween: 14 },
         1024: { slidesPerView: 4, spaceBetween: 16 },
       },
     });
   </script>

.. ----

.. .. grid:: 3


..     .. grid-item-card:: Getting started :fa:`person-running`
..         :padding: 2 2 2 2
..         :link: getting_started/index
..         :link-type: doc

..         Install PyMechanical, choose your mode, and run your first script.

..         :bdg-info:`Install` :bdg-info:`Choose mode` :bdg-info:`Quick start`

..     .. grid-item-card:: User guide :fa:`window-maximize`
..         :padding: 2 2 2 2
..         :link: user_guide/index
..         :link-type: doc

..         Learn how to use embedding mode, remote sessions, scripting, and CLI tools.

..         :bdg-info:`Embedding` :bdg-info:`Remote` :bdg-info:`Scripting`

..     .. grid-item-card:: Examples :fa:`scroll`
..         :padding: 2 2 2 2
..         :link: examples/index
..         :link-type: doc

..         Explore examples, which are organized by mode and simulation type.

..         :bdg-info:`Embedding` :bdg-info:`Remote` :bdg-info:`Advanced`

..     .. grid-item-card:: API reference :fa:`book-bookmark`
..         :padding: 2 2 2 2
..         :link: api/index
..         :link-type: doc

..         Understand PyMechanical API endpoints and their capabilities.

..         :bdg-info:`Classes` :bdg-info:`Methods` :bdg-info:`Error handling`

..     .. grid-item-card:: Mechanical scripting API :fa:`code`
..         :padding: 2 2 2 2
..         :link: https://scripting.mechanical.docs.pyansys.com/

..         Do you need Mechanical API scripting support? Have a look
..         at its API.

..         :bdg-info:`Mechanical API`

..     .. grid-item-card:: FAQs :fa:`fa-solid fa-circle-question`
..         :padding: 2 2 2 2
..         :link: faq
..         :link-type: doc

..         Frequently asked questions and their answers.

..         :bdg-info:`How` :bdg-info:`Why` :bdg-info:`What`

..     .. grid-item-card:: Known issues and limitations :fa:`fa-solid fa-bug`
..         :padding: 2 2 2 2
..         :link: kil/index
..         :link-type: doc

..         See issues and limitations for both PyMechanical and Mechanical.

..         :bdg-info:`24R2` :bdg-info:`25R1` :bdg-info:`25R2` :bdg-info:`26R1`

..     .. grid-item-card:: Contribute :fa:`people-group`
..         :padding: 2 2 2 2
..         :link: contribute
..         :link-type: doc

..         Learn how to contribute to the PyMechanical codebase
..         or documentation.

..         :bdg-info:`Test` :bdg-info:`Documentation` :bdg-info:`Issues`

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
