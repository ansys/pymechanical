.. post:: 2026-07-28
   :tags: docker, linux, ci-cd, embedding
   :category: How-to
   :author: ANSYS
   :location: World
   :language: English

.. _blog_docker_embedding_cicd:

#####################################################################
Run PyMechanical embedding in CI/CD with a Linux Mechanical image
#####################################################################

Containerizing Mechanical lets you reproduce simulation environments
reliably across developer machines and CI runners without managing
Ansys installations on every host. This post shows how to build a
minimal Linux image and plug it into a GitHub Actions pipeline using
PyMechanical's embedding mode.

Workflow overview
=================

The process splits into two phases: **build once** on a local Linux
machine, then **run on every CI commit**.

.. mermaid::

   flowchart TB
       subgraph build ["Build phase (local, one-time)"]
           direction LR
           A(["Download installer\nCustomer Portal"]) --> B(["Install Mechanical\nUbuntu 22.04"])
           B --> C(["docker build"])
           C --> D(["Push to registry\nGHCR / private"])
       end

       subgraph ci ["CI/CD phase (every commit)"]
           direction LR
           E(["Pull image"]) --> F(["Run container\nbash entrypoint"])
           F --> G(["xvfb-run mechanical-env\npython simulate.py"])
           G --> H(["Upload artifacts"])
       end

       D --> E

       classDef buildNode fill:#e8f0fe,stroke:#4a6fa5,stroke-width:1px,color:#1a237e
       classDef ciNode fill:#e6f4ea,stroke:#3d8b5f,stroke-width:1px,color:#1b5e20

       class A,B,C,D buildNode
       class E,F,G,H ciNode

       style build fill:#f4f7fc,stroke:#4a6fa5,stroke-width:1px
       style ci fill:#f2f9f4,stroke:#3d8b5f,stroke-width:1px

Part 1: Build the Mechanical Docker image
==========================================

Requirements
------------

- Ubuntu 22.04 machine with Docker installed
- Valid Ansys account to download the installer from
  `download.ansys.com <https://download.ansys.com>`_
- The `PyMechanical repository <https://github.com/ansys/pymechanical>`_
  cloned locally (provides the ``Dockerfile`` and ``.dockerignore``)

Steps
-----

Install Mechanical on your Ubuntu machine. To keep the image small,
install only the Mechanical and LS-DYNA solvers:

.. code-block:: console

   sh /path/to/INSTALL \
       -silent -overwrite_preview -mechapdl -lsdyna \
       -install_dir /install/ansys_inc/

Then build and push the image. Replace ``261`` with your version number:

.. code-block:: console

   export VERSION=261
   export TAG=ghcr.io/your-org/mechanical:v${VERSION}

   # Go to the directory where Mechanical is installed
   cd /install/

   # Copy the Dockerfile and .dockerignore from the PyMechanical repo
   cp /path/to/pymechanical/docker/${VERSION}/Dockerfile .
   cp /path/to/pymechanical/docker/${VERSION}/.dockerignore .

   # Build and push
   docker build -t ${TAG} --build-arg VERSION=${VERSION} .
   docker push ${TAG}

The
`Dockerfile <https://github.com/ansys/pymechanical/tree/main/docker/261/Dockerfile>`_
copies the installation directory into an Ubuntu 22.04 base image and sets the
required environment variables and virtual display configuration.

Part 2: Use the image in GitHub Actions (embedding mode)
=========================================================

Set the Mechanical image as the job ``container`` and override the
entrypoint to ``/bin/bash``. This lets the CI step run arbitrary
commands inside the container instead of starting the gRPC server.

.. code-block:: yaml

   jobs:
     simulate:
       runs-on: ubuntu-latest
       container:
         image: ghcr.io/your-org/mechanical:v261
         options: --entrypoint /bin/bash
       steps:
         - uses: actions/checkout@v4

         - name: Set up Python and install PyMechanical
           env:
             DEBIAN_FRONTEND: noninteractive
             TZ: Etc/UTC
           run: |
             apt update
             apt install -y git curl
             curl -LsSf https://astral.sh/uv/install.sh | sh
             export PATH="$HOME/.local/bin:$PATH"
             uv python install python3.12
             uv venv .venv
             . .venv/bin/activate
             uv pip install --upgrade pip
             uv pip install ansys-mechanical-core

         - name: Run simulation
           env:
             ANSYSLMD_LICENSE_FILE: 1055@${{ secrets.LICENSE_SERVER }}
           run: |
             export PATH="$HOME/.local/bin:$PATH"
             . .venv/bin/activate
             xvfb-run mechanical-env python simulate.py

         - name: Upload results
           uses: actions/upload-artifact@v4
           with:
             name: results
             path: results/

``mechanical-env`` sets the environment variables that PyMechanical needs
to locate the Mechanical installation.
``xvfb-run`` provides an in-memory virtual display — required because
Mechanical initialises OpenGL even in batch mode.

Your simulation script uses the standard embedding API:

.. code-block:: python

   from ansys.mechanical.core import App
   import pathlib

   RESULTS_DIR = pathlib.Path("results")
   RESULTS_DIR.mkdir(exist_ok=True)

   app = App(globals=globals())

   # Set up the model
   Model.AddStaticStructuralAnalysis()
   # ... geometry, materials, mesh, boundary conditions

   Model.Analyses[0].Solution.Solve(True)

   # Save results
   app.save(str(RESULTS_DIR / "model.mechdb"))

Key points
==========

- **No license file in the image.** Pass ``ANSYSLMD_LICENSE_FILE`` at
  runtime via an environment variable or a GitHub Actions secret.
- **Embedding mode runs in-process.** There is no separate gRPC server to
  start or port to expose, which simplifies the pipeline.
- **Match versions.** The Mechanical version in the image must match the
  PyMechanical package you install. Mismatches cause ``App()`` to fail
  at initialisation.

Why this workflow benefits Mechanical customers
===============================================

Reproducible simulation environments
-------------------------------------

Pinning a specific Mechanical version in a Docker image eliminates
"works on the same machine" failures. Every engineer on the team and every CI
runner executes simulations against the same solver binary, libraries,
and environment variables, so result differences are always caused by
model changes, not environment drift.

Faster setup for new contributors
----------------------------------

A new team member or a fresh CI runner needs only Docker and a registry
credential to start running simulations. There is no manual Ansys
installer wizard, no environment variable configuration, and no concern
about incompatible system libraries.

Traceable results
------------------

Because the image tag is pinned in the workflow YAML (for example,
``mechanical:v261``), every simulation result in your artifact store
is linked to an exact solver version. Reproducing a result from six
months ago is as simple as checking out the commit and re-running the
pipeline.

Safe solver upgrades
---------------------

Upgrading Mechanical is a controlled, reviewable change: build a new
image, update one line in the workflow YAML, open a pull request, and
run the full regression suite before merging. There is no risk of an
unintended solver update affecting production simulation results.

Lower infrastructure cost
--------------------------

Linux container runners are cheaper than Windows runners on most CI
platforms and require no GUI license server infrastructure. Embedding
mode also avoids the network overhead of a gRPC remote session, so
simulations start faster and use fewer system resources per job.

See also
========

- :doc:`/getting_started/docker`: advanced Docker configuration options
- :doc:`/user_guide/embedding/overview`: full embedding API reference
