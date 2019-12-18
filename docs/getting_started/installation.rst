.. _installation:

Installation
============

Using pip
---------

::

    pip install git+https://bitbucket.org/errequadro-red/pretoText.git


Using pipenv
------------

From CLI
~~~~~~~~

::

    pipenv install -e git+https://bitbucket.org/errequadro-red/pretoText.git#egg=pretoText


From Pipfile
~~~~~~~~~~~~

::

    [packages]
    pretoText = {git = "https://bitbucket.org/errequadro-red/pretoText.git", editable = true}


Using manual setup
------------------

Clone the repository in a folder::

    git clone https://bitbucket.org/errequadro-red/pretoText.git

Then start the setup::

    python setup.py


Tips for Jupyter
----------------

Using pip
~~~~~~~~~
::

    # Install a pip package in the current Jupyter kernel
    import sys
    !{sys.executable} -m pip install https://bitbucket.org/errequadro-red/pretoText.git
