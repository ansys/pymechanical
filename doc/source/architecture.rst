.. _ref_architecture:

PyMechanical architecture
=========================

PyMechanical provides a Python interface to Ansys Mechanical. Mechanical is a
polyglot [#f1]_ desktop app whose graphical user interface (GUI) runs on either
the Windows or Linux operating system. Mechanical's APIs are implemented in C#
using .NET Framework 4.x. They are exposed to both C# and two implementations
[#f2]_ of Python, namely IronPython [#f3]_ and CPython.

Within Mechanical, Python scripting enables you to automate repetitive GUI
actions. This is not unlike other apps developed either by Ansys or other
software companies. Python scripting leverages the Mechanical API.

Mechanical, like some other apps, is customizable. Using the same API that you
would use for scripting, you can implement extensions that add to the
capabilities of Mechanical. For example, buttons can be added to the GUI and
custom objects can be added to the data model. Even third-party or in-house
solvers can be integrated into Mechanical and can take advantage of the
powerful meshing, generic CAD reader, and the intuitive pre- and post-
processing experience of Mechanical.

Before discussing how Mechanical's API is implemented, we discuss a software
design pattern known as the *command pattern*. This pattern can be used in many
programming languages. A general description (using the Java programming
language) can be found here in the *HowToDoInJava* newsletter:
https://howtodoinjava.com/design-patterns/behavioral/command-pattern/. Our own
brief explanation follows.

Command pattern
---------------

Many interactive apps use the command pattern. It turns anything that the user
does within the app turns into a command object, which is immediately executed.
This approach carries some additional benefits [#f4]_.

More relevant to this discussion is how command patterns can be used to
implement automation APIs. If every action is a command, then that Command can
serve as the API. So long as the Commands can be encoded in text, a scripting
language can be used to execute them. In fact, this approach is roughly how the
Ansys Electronics Desktop, Ansys Mechanical APDL, and the Ansys Workbench apps
implement automation APIs for scripting.

Using the command pattern as a scripting API has disadvantages. Most
importantly, command APIs are not symmetric. The four fundamental operations on
data within a software app are ``Create``, ``Read``, ``Update``, and
``Delete``. These are often abbreviated as CRUD. While you can conceptually
update, create, and delete using commands, you can not read using a command.
This makes it difficult to "visit" the app's data model.

Mechanical API implementation
-----------------------------

Mechanical's API serves the needs of both *automation* and *customization*. For
customization, it is necessary to read the data model. For example, when
integrating a third-party solver, you must access boundary conditions,
geometry, material properties, mesh, and connections to properly input them to
the solver. As discussed earlier, the command pattern does not allow this kind
of access. Due to this fact, the Mechanical API exposes its data model directly
to the user. This is how a hypothetical command-based API would look for
renaming an object.

.. code:: python

    RenameCommand(id=100, name="New name")

Instead, an API based on a data model, like mechanical's API, looks like this:

.. code:: python

    obj = GetObject(id=100)
    print(obj.Name)
    obj.Name = "New name"

Notice that you could print the name by Reading a property of the object. A
command-based API can not provide the same experience.


PyMechanical remote interface
-----------------------------

One way to interact with the Mechanical API from Python is as a remote session.
You can run Mechanical as a server and send a *Remote Procedure Call* (RPC).
The server handles the RPC and returns the response to the client. Currently,
sending commands as a string and getting the result as a string is the only
option.

PyMechanical embedded instance
--------------------------------

The embedded instance used by PyMechanical embeds an entire instance of the
Mechanical app in-memory inside of a Python program. There is no additional
running process associated with it. Mechanical's data model is directly
available within Python, which means that the fully CRUD data model of the
mechanical API can be used.



Distributed systems
===================

This section contains a very basic explanation of *distributed systems*. It is
not meant be exhaustive and rigorous, but it instead introduces just the topics
necessary to understand the choices made by the designers of PyMechanical.

A distributed system is a software system that uses a network to distribute
software across physical machines. With a distributed system, the individual
pieces of that system do not share an address space and therefore cannot call
functions of each other directly. Instead, they communicate with each other by
sending messages in packets.

Distributed systems have unique characteristics when compared to classical
software systems that share an address space. For instance, in a distributed
system, any call can fail because of a problem with the network, and the caller
can not always know whether a call has failed. For this reason, features of
interest to distributed system designers, such as fault tolerance and
idempotency, are not emphasized by classical software systems.

Examples include email, multiplayer games, web apps, and high-performance
computing, among other things. Historically, there are three major categories
of remote APIs: Message passing, resource based, and Remote Method Invocation.


Message passing
---------------

Message passing is the original model of remote APIs, and in fact the other two
categories are implemented using message passing underneath. RPCs are initiated
by the client and sent to the server as a message, or a sequence of bytes.
There must be some understanding on both sides of the channel as to what
information is in these bytes. This is usually handled by a protocol (such as
HTTP or TCP) and usually also a higher-level library (such as gRPC or zeroMQ)
implemented using the protocol. The server may send back a series of messages
to the client to indicate that a message was received, that it is executing,
that it has executed, and with a response, if any. The protocol and library
determine the expected sequence of messages, their ordering, and any failure
handling.

Resource-based APIs
-------------------

Resource-based APIs were popularized by REST, and has been shown to be, for
practical purposes, infinitely scalable. They are traditionally implemented
using HTTP or HTTPS, but implementations can exist in any transport protocol.

The fundamental concept behind REST is the separation of verbs and resources.
Verbs include ``GET``, ``PUT``, ``UPDATE``, ``DELETE``, and ``POST``, while
resources are any uniquely identifiable entity.

REST can scale because servers can make assumptions about the data it serves
based on the verb and resource. For instance, if a GET was done on the resource
"/a/b/c", and then no mutating verbs (PUT, UPDATE, DELETE, POST) are run on
that or any child resource (such as "/a/b/c/d"), the server can reuse the
result of the previous request rather than recompute the result. When using the
HTTP protocol, this is called HTTP caching and is a fundamental property of the
internet.

Remote method invocation
------------------------

In the 1990s, *Object Oriented Programming* (OOP) exploded in popularity.
Among other things, OOP allows programmers to add abstractions on top of data
in their code using objects. When done well, objects can reduce code complexity
and makes large scale software easier to reason about. It was thought that even
the difference between RPCs and calls made in a program's address space could
be abstracted. In effect, the user of an object does not need to know whether
an object exists remotely or locally. Operations on that object could be done
in the same way, regardless. To scale the system to be distributed over a
network, some middleware would be responsible for load-balancing and allocating
these objects remotely.

This approach is known as Remote Method Invocation (RMI). RMI was widely
implemented using CORBA, DCOM, Remoting (.NET), and Java RMI. However, this
approach has fallen out of favor with the rise of the internet, as it was
observed that it does not scale. As a practical example, recent versions of
.NET do not implement the Remoting library, and COM/DCOM are not used in modern
web stacks.

For illuminating discussion of the problems with RMI, see `Microservices and
the First Law of Distributed Objects
<https://martinfowler.com/articles/distributed-objects-microservices.html>`_ on
Martin Fowler's website.

Remote mechanical
=================

Mechanical's official API is that of an object model, and PyMechanical provides
exactly that API to Python. Because object models are not suitable as remote
APIs, PyMechanical does not provide that API in a remote fashion. This is why
the remote session API is based on strings, while the embedded instance API can
provide the Mechanical API directly to Python.

Another remote API
------------------

An alternative remote API for Mechanical is practical so long as it is based on
message passing or REST. In fact, Mechanical uses a REST API internaly as part
of its GUI. This is not the official Mechanical API and is not currently
documented. An API like that is not an immediate goal of PyMechanical.

Using PyMechanical in a distributed system
------------------------------------------

You can still build a distributed system where Mechanical is run remotely using
the embedded instance of Mechanical in PyMechanical. For this to work, Python
itself would run remotely, and therefore the embedded instance would run
remotely. The communication across the network in that system would be done in
Python.


.. rubric:: Footnotes

.. [#f1] This means that it is implemented using more than one programming language.
.. [#f2] The Python programming language is in fact only a specification of a language. CPython is the reference implementation developed by the creator of Python. There are others, including IronPython, PyPy, Cinder, and GraalPy.
.. [#f3] IronPython is an implementation of the Python programming language using the DLR from .NET. It does not implement the Python/C API, which is why many Python packages cannot run within IronPython. It also currently only implements Python2.7.
.. [#f4] *Undo* and *redo* are often implemented using a command pattern. They store all executed commands in a stack. Each command not only has the ability to execute, it also has the ability to undo itself. Undo and redo are then implemented by walking up and down the stack and executing the Command or its inverse function.