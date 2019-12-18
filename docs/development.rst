Development
===========

Initialisation
--------------

Clone the RED Toolkit repository into your favorite folder::

    git clone https://bitbucket.org/errequadro-red/pretoText.git


Afterwards, it's a good habit to install all requested packages inside a Python virtual environment. This can be done by using virtualenv or pipenv.

virtualenv
~~~~~~~~~~

::

    pip install --user virtualenv
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt


pipenv
~~~~~~

::

    pip install --user pipenv
    pipenv install --dev


Best Practices
--------------

Code Formatting
~~~~~~~~~~~~~~~

RED Toolkit uses [Black](https://github.com/python/black) for an automated code formatting fixing. Black is activated by command line with:

::

    black pretoText


Tests Coverage
~~~~~~~~~~~~~~

In order to run a full code tests coverage task::

    coverage run --omit=tests/ pretoText/

Reports can be created by::

    coverage [html xml]
