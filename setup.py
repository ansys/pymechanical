import setuptools

for package in setuptools.find_namespace_packages('src'):
    print(package)


setuptools.setup(
    name="pymechanical",
    version="0.0.1",
    description="This package provides Pythonic access to the Mechanical process running locally or remotely",
    packages=setuptools.find_namespace_packages('src'),
    package_dir={'': 'src'},
    license='MIT',
    author='ANSYS, Inc',
    install_requires=['grpcio-tools>=1.44.0'],
    python_requires='>=3.7.11'
)
