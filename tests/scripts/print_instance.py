"""Print instance of PyMechanical embedding app."""
#!/usr/bin/env python
import sys

import ansys.mechanical.core as pymechanical

version = int(sys.argv[1])
app = pymechanical.App(version=version)
print(app)
