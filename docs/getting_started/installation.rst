.. _installation:

Installation
============

Using pip
---------

::

    pip install git+https://bitbucket.org/errequadro-red/redtoolkit.git


Using pipenv
------------

From CLI
~~~~~~~~

::

    pipenv install -e git+https://bitbucket.org/errequadro-red/redtoolkit.git#egg=redtoolkit


From Pipfile
~~~~~~~~~~~~

::

    [packages]
    redtoolkit = {git = "https://bitbucket.org/errequadro-red/redtoolkit.git", editable = true}


Using manual setup
------------------

Clone the repository in a folder::

    git clone https://bitbucket.org/errequadro-red/redtoolkit.git

Then start the setup::

    python setup.py


Tips for Jupyter
----------------

Using pip
~~~~~~~~~
::

    # Install a pip package in the current Jupyter kernel
    import sys
    !{sys.executable} -m pip install https://bitbucket.org/errequadro-red/redtoolkit.git
