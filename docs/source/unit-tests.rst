Tests
=====

Install `neo3-boa <install.html>`_ and the `TestEngine <testengine.html>`_ and run the following command

.. note::
   If you didn't install TestEngine in neo3-boa's root folder, you need to change the value of `TEST_ENGINE_DIRECTORY` in [this file](/env.py)

::

    python -m unittest discover boa3_test
