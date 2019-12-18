

# pretoText - NLP toolkit for Technical Text Analysis

A repo containing a Toolkit for Research & Development on Technical Text.

## Usage

### Installing

#### Using pip

```
pip install git+https://bitbucket.org/errequadro_red/red-toolkit.git
```

#### Using pipenv

From CLI:
```
pipenv install -e git+https://bitbucket.org/errequadro_red/red-toolkit.git#egg=redtoolkit
```

From Pipfile:
```
[packages]
redtoolkit = {git = "https://bitbucket.org/errequadro_red/red-toolkit.git", editable = true}
```
#### Using manual setup

Clone the repository in a folder:
```
git clone https://bitbucket.org/errequadro_red/red-toolkit.git
```
Then start the setup through:
```
python setup.py
```

#### Tips for Jupyter

Using pip:
```
# Install a pip package in the current Jupyter kernel
import sys
!{sys.executable} -m pip install https://bitbucket.org/errequadro_red/red-toolkit.git
```

#### Examples from inside a project
```
from redtoolkit.textanalysis import similarities

df_sim_wn = similarities.wordnet.ranking_by_wordnet_from_gsheet(
	gsheet_id,
	parallelisation=2,
	sorting=True,
	column="a_column",
	sheet_name="a_sheet_name"
)
```
#### Examples from a CLI
If using pipenv, ```pipenv run``` must precede the command or ```pipenv shell``` must be called in order to activate the environment.
```
python redtoolkit ranking_by_wordnet_from_gsheet gsheet_id --parallelisation=2 --sorting=True --column=a_column --sheet_name=a_sheet_name
```
## Development

### Initialisation

Clone the RED Toolkit repository into your favorite folder:
```
git clone https://bitbucket.org/errequadro_red/red-toolkit.git
```

Afterwards, it's a good habit to install all requested packages inside a Python virtual environment. This can be done by using virtualenv or pipenv.

#### virtualenv

```
pip install --user virtualenv
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

#### pipenv

```
pip install --user pipenv
pipenv install --dev
```

### Best Practices
#### Code Formatting
RED Toolkit uses [Black](https://github.com/python/black) for an automated code formatting fixing. Black is activated by command line with:
```
black redtoolkit
```

#### Tests Coverage

In order to run a full code tests coverage task:
```
coverage run --omit=tests/ redtoolkit/
```

Reports can be created by:
```
coverage [html xml]
```
