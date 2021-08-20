# Gets GitLab runner registration token from root account
Horrible boiler plate to get the token. It is designed to be embedded in another repo with the following structure:
```
parent_repo
|_get-gitlab-runner-registration-token
|_src/creds.txt
|_src/hardcoded_variables.txt
```
And it will output:
```
parent_repo
|_get-gitlab-runner-registration-token
|_src/creds.txt
|_src/hardcoded_variables
|_src/runner_registration_token.txt
```
## Requirements
0. Next to this repository create a `src` folder.
1. In that src folder create the `src/creds.txt` file with content:
```
gitlab_server_account=root
gitlab_server_password=yoursecretrootpasswordofyourgitlabserver
```

2. In that same src folder create the `src/hardcoded_variables.txt` file with content:
```
RUNNER_REGISTRATION_TOKEN_FILEPATH=src/runner_registration_token.txt
```
That's it.

## Usage: do once
Download/clone this repository.
0. If you don't have pip: open Anaconda prompt and browse to the directory of this readme:
```
cd /home/<your path to the repository folder>/
```

1. To use this package, first make a new conda environment and activate (it this automatically installs everything you need)
```
conda env create --file environment.yml
```

## Usage: do every time you start Anaconda:

3. Activate the conda environment you created:
```
conda activate batch_copy_issues
```

## Usage: do every run:

3. Performe a run for assignment 1 (named project1) of main code (in `main.py`, called from `__main__.py`)
```
python -m code.project1.src
```

## Testing

4. Testing is as simple as running the following command in the root directory of this repository in Anaconda prompt:
```
python -m pytest
```
from the root directory of this project.

<!-- Un-wrapped URL's below (Mostly for Badges) -->
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[python_badge]: https://img.shields.io/badge/python-3.8-blue.svg
