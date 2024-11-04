# Copyright (C) 2022 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# #
# #
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# # of this software and associated documentation files (the "Software"), to deal
# # in the Software without restriction, including without limitation the rights
# # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# # copies of the Software, and to permit persons to whom the Software is
# # furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included in all
# # copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# # SOFTWARE.
# """Mechanical service."""

# import rpyc
# import toolz

# from .utils import get_remote_methods


# class MechanicalService(rpyc.Service):
#     """Starts Mechanical app services."""

#     def __init__(self, app, poster, functions=[], impl=None):
#         """Initialize the service."""
#         super().__init__()
#         self._app = app
#         self._poster = poster
#         self._install_functions(functions)
#         self._install_class(impl)

#     def _install_functions(self, methods):
#         """Install the given list of methods."""
#         [self._install_function(method) for method in methods]

#     def _install_class(self, impl):
#         """Install methods from the given implemented class."""
#         if impl is None:
#             return
#         for methodname, method in get_remote_methods(impl):
#             print(f"installing {methodname} of {impl}")
#             self._install_method(method)

#     def on_connect(self, conn):
#         """Handle client connection."""
#         print("Client connected")
#         print(self._app)

#     def on_disconnect(self, conn):
#         """Handle client disconnection."""
#         print("Client disconnected")

#     def _curry_method(self, method, realmethodname):
#         """Curry the given method."""

#         def posted(*args):
#             def curried():
#                 original_method = getattr(method._owner, realmethodname)
#                 result = original_method(*args)
#                 return result

#             return self._poster.post(curried)

#         return posted

#     def _curry_function(self, methodname):
#         """Curry the given function."""
#         wrapped = getattr(self, methodname)
#         curried_method = toolz.curry(wrapped)

#         def posted(*args):
#             def curried():
#                 return curried_method(self._app, *args)

#             return self._poster.post(curried)

#         return posted

#     def _install_method(self, method):
#         """Install methods of impl with inner and exposed pairs."""
#         exposed_name = f"exposed_{method.__name__}"
#         inner_name = f"inner_{method.__name__}"

#         def inner_method(*args):
#             """Convert to inner method."""
#             result = method(*args)
#             return result

#         def exposed_method(*args):
#             """Convert to exposed method."""
#             f = self._curry_method(method, method.__name__)
#             result = f(*args)
#             return result

#         setattr(self, inner_name, inner_method)
#         setattr(self, exposed_name, exposed_method)

#     def _install_function(self, function):
#         """Install a functions with inner and exposed pairs."""
#         print(f"Installing {function}")
#         exposed_name = f"exposed_{function.__name__}"
#         inner_name = f"inner_{function.__name__}"

#         def inner_method(app, *args):
#             """Convert to inner method."""
#             return function(app, *args)

#         def exposed_method(*args):
#             """Convert to exposed method."""
#             f = self._curry_function(inner_name)
#             return f(*args)

#         setattr(self, inner_name, inner_method)
#         setattr(self, exposed_name, exposed_method)
