.. _ref_architecture:

=========================
PyMechanical Architecture
=========================

PyMechanical provides a Python interface to Ansys Mechanical. Mechanical is a
polyglot [#f1]_ desktop application whose graphical user interface (GUI) runs
on either the Windows or Linux operating system. Mechanical's APIs are
implemented in C# using .NET Framework 4.x. They are exposed to both C# and
two implementations [#f2]_ of Python, IronPython [#f3]_ and CPython.

Within Mechanical, Python scripting enables you to automate repetitive GUI
actions. This is not unlike other applications developed either by Ansys or
other software companies. Python scripting leverages the Mechanical API.

Mechanical, like some other applications, is customizable. Using the same
Mechanical API that you use for scripting, you can implement extensions that
add to the capabilities of Mechanical. For example, buttons can be added to the
GUI and custom objects can be added to the data model. Even third-party or
in-house solvers can be integrated into Mechanical and can take advantage of
the powerful meshing, generic CAD reader, and the intuitive pre- and post-
processing experience of Mechanical.

Before discussing how Mechanical's API is implemented, a design pattern known
as the "Command Pattern" is discussed. This is an abstract pattern that can be
used in any object oriented system in many programming languages. A high level
explanation of the pattern (using the Java programming language) can be found
here: https://howtodoinjava.com/design-patterns/behavioral/command-pattern/.
A brief explanation follows.

Command pattern
---------------
Many interactive applications use the Command pattern. In a nutshell, anything
the user does within the application turns into a Command object, and then the
Command object is immediately executed. This approach carries some benefits.
For example, applications that work in this way can choose to implement undo
and redo by storing an 'inverse' function within the Command and storing a
stack of executed commands. Undo/Redo is then implemented by walking up and
down the stack and executing the Command or its inverse function.

More relevant to this discussion is how command patterns can be used to
implement automation APIs. If every user action is a Command, then that Command
can serve as an API. In this way, everything the user does can be trivially
recorded as textual representations of those Commands. These can then be
replayed using a scripting language supported by the application. In fact, this
exact command pattern is how the Ansys Electronics Desktop, Ansys Mechanical
APDL, and the Ansys Workbench applications implement automation APIs for
scripting.

Using the command pattern as a scripting API does come with some disadvantages.
Most importantly, command APIs are not symmetric. The four fundamental
operations on data within a software application are Create, Read, Update, and
Delete. These are often abbreviated as CRUD. While you can conceptually Update,
Create, and Delete using Commands, you can not Read. This makes it difficult to
"visit" the application's data model.

Mechanical API Implementation
-----------------------------
Mechanical's API serves the needs of both *automation* and *customization*. For
customization, it is necessary to Read the data model. Automation alone is not
sufficient. For example, when integrating a third-party solver, you will need
to access all of the boundary conditions, geometry, material properties, mesh,
and connections to properly input them to the solver. As discussed above, the
command pattern does not allow this kind of access pattern. Due to this fact,
the Mechanical API exposes its data model directly to the user. This is how a
hypothetical command-based API would look for renaming an object.

.. code:: python

    RenameCommand(Id=100, Name="New name")

Instead, an API based on a data model, like mechanical, looks like this:

.. code:: python

    obj = DataModel.GetObjectById(100)
    print(obj.Name)
    obj.Name = "New name"

Notice that the old name could be printed by accessing a property of the
object. This has no equivalent if the API used a command pattern.


PyMechanical Remote Interface
-----------------------------
One way to interfact with the Mechanical API from CPython is as a Remote
Session. A session of Mechanical runs as a server and can receive a Remote
Procedure Call (RPC). The RPC is handled by the server and then the response
is returned back to the client.

PyMechanical Embeddeded Instance
--------------------------------
The embedded instance used by PyMechanical embeds an entire instance of the
Mechanical application in-memory inside of a CPython program. There is no
additional running process associated with it. Here, only the CPython interface
to the Mechanical API can be used.

===================
Distributed Systems
===================

This section contains a very basic explanation of Distributed Systems. It is
not meant be exhaustive and rigorous, but instead introduces just the topics
necessary to understand the choices made by PyMechanical.

The term Distributed System is used to describe a software system that uses
a network to distribute software across multiple physical machines. With a
Distributed System, the individual pieces of that system do not share an
address space, and therefore cannot call functions of each other directly.
Instead, they communicate with each other by sending messages in packets.

There are unique characteristics of distributed systems relative to classical
software systems that share an address space. For instance, in a distributed
system, any call can fail because of a problem with the network, and the caller
can not always know whether a call has failed. For this reason, features of
interest to distributed system designers such as fault tolerance and
idempotency are not necessarily important in classical software systems.

These systems are used by email, multiplayer games, web applications, and high
performance computing, among other things. Historically, there are three major
categories of remote APIs, Message passing, resource-based, and Remote Method
Invocation.

Message passing
---------------
Message passing is the original model of remote APIs, and in fact the other two
are implemented using message passing underneath. RPCs are initiated by the
client and sent to the server as a message, or a sequence of bytes. There must
be some understanding on both sides of the channel as to what information is in
these bytes. This is usually handled by a protocol (such as HTTP or TCP) and
usually also a higher level library (such as gRPC or zeroMQ) implemented using
the protocol. The server may send back a series of messages to the client to
indicate that a message was recieved, that it is executing, that it has
executed, and with a response, if any. The protocol and library determine the
expected sequence of messages, their ordering, and any failure handling.

Resource-based APIs
-------------------
Resource-based APIs were popularized by REST, and has been shown to be, for
practical purposes, infinitely scalable. They are traditionally implemented
using HTTP or HTTPS but implementations can exist in any transport protocol.

The fundamental concept behind REST is the separation of verbs and resources.
Verbs include GET, PUT, UPDATE, DELETE, and POST, while resources are any
uniquely identifiable entity.

REST can scale because servers can make assumptions about the data it serves
based on the verb and resource. For instance, if a GET was done on the resource
"/a/b/c", and then no mutating verbs (PUT, UPDATE, DELETE, POST) have been run
on that or any child resource (such as "/a/b/c/d"), the server can reuse the
result of the previous request rather than recompute the result. When using the
HTTP protocol, this is called HTTP caching and is a fundamental property of the
internet.

Remote method invocation
------------------------
In the 1990s, OOP exploded in popularity. With it, came a very tempting idea.
OOP allows programmers to provide abstractions on top of data in their code.
It was thought that even the difference between RPC calls and calls made in
a program's addresss space could be abstracted. The user of the library does
not need to know whether an object exists remotely or locally, the call can
just be made in the same way, and to scale the system to be distributed over a
network, some middleware would be responsible for load-balancing and allocating
these objects remotely.

This technique is known as Rmeote Method Invocation (RMI). RMI was widely
implemented, using CORBA, DCOM, Remoting (.NET), and Java RMI. However, this
approach has fallen out of favor with the rise of the internet, as it was
observed that this paradigm does not scale. As a practical example, recent
versions of .NET do not implement the Remoting library, and COM/DCOM are not
used in modern web stacks.

An illuminating discussion of the problems with RMI can be found at
https://martinfowler.com/articles/distributed-objects-microservices.html

=================
Remote Mechanical
=================

Mechanical's official API is that of an object model, and PyMechanical provides
exactly that API to Python. Because Object Models are not suitable as remote
APIs, PyMechanical does not provide that API in a remote fashion. This is why
the remote session API is based on strings, while the embedded instance API can
provide the Mechanical API directly to Python.

Another Remote API
------------------
Amother remote API for Mechanical is definitely possible to provide, so long as
it is based on message passing or REST. In fact, Mechanical uses a REST API
internally as part of its GUI. This is not the official Mechanical API and is
not currently documented. But such an API is not an immediate goal of the
PyMechanical project.

Using PyMechanical in a distributed system
------------------------------------------
It is still possible to build a distributed system where Mechanical is run
remotely using the embedded instance of Mechanical in PyMechanical. For this to
work, Python itself would run remotely, and therefore the embedded instance
would run remotely. The communication across the network in that system would
be done in Python.


.. rubric:: Footnotes

.. [#f1] This means that it is implemented using more than one programming language.
.. [#f2] The Python programming language is in fact only a specification of a language. CPython is the reference implementation developed by the creator of Python. There are others, including IronPython, PyPy, Cinder, and GraalPy.
.. [#f3] IronPython is an implementation of the Python programming language using the DLR from .NET. It does not implement the Python/C API, which is why many python packages can not run within IronPython. It also currently only implements Python2.7.
