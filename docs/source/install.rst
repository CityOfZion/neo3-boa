Installation
============

This version of the compiler requires Python 3.7 or later

.. note::
   Make sure you have installed MSVC v142 - Build tools VS 2019 C++ x64/x86 (v14.24). You can do this by installing `Visual Studio`_ and adding C++ development features.

Set Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^

Make a Python 3 virtual environment and activate it:

On Linux/Mac OS::

    $ python3 -m venv venv
    $ source venv/bin/activate


On Windows::

    $ python3 -m venv venv
    $ venv\Scripts\activate.bat

Pip (Recomended)
^^^^^^^^^^^^^^^^

::

    pip install neo3-boa


Build from Source (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If neo3-boa is not available via pip, you can build it from source.

::

    git clone https://github.com/CityOfZion/neo3-boa.git
    pip install -e .


.. _Visual Studio: https://visualstudio.microsoft.com/
