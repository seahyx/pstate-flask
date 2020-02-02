# Parade State - Flask Server

Use SSH to access the raspberry pi flask server. You must be connected to the same network to access the raspberry pi for SSH.

Port: (TBD) (Static)
Username: (TBD)
Password: (Written on the raspberry pi case)

The flask server is hosted on the raspberry pi using tmux.

## Accessing raspberry pi with ssh

If using cmd, SSH with the command

`ssh -l pi 192.168.198.100`

then after login,

`tmux a`

to attach to a running tmux instance. Otherwise, just call `tmux` to open an instance.

## Setting up the environment

### Python

Check if python is installed with

`python --version` or `py --version`

If not, install [python 3](https://www.python.org/downloads/).

### Pip

Pip framework should be installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4. Check if pip is installed using

`pip --version`

If not, follow this [installation guide](https://pip.pypa.io/en/stable/installing/).

### Python virtual environment

Choice of virtual environment is up to you. [venv](https://docs.python.org/3/library/venv.html) is default in Python 3.3 or later.

For windows, it is recommended to install [virtualenvwrapper-win](https://pypi.org/project/virtualenvwrapper-win/). To install using pip, run

`pip install virtualenvwrapper-win`

The next few steps assumes you are using virtualenvwrapper.

Create a virtual environment. `env-name` can be replaced with anything.

`mkvirtualenv env-name`

To view the list of virtual environments, run

`workon`

Access the virtual environment you created with

`workon env-name`

Open the project directory in your terminal. Set the project directory for the virtual environment with

`setprojectdir .`

Install all the dependencies for the project with

`pip install -r requirements.txt`

Set up is now complete.

### Deactivating

To deactivate the virtual environment, simply close the terminal, or use

`deactivate`

## Updating dependencies and requirements.txt

To update dependencies, pull the updated requirements.txt and run

`pip install -r requirements.txt`

To update requirements.txt, enter the virtual environment for the project and run

`pip freeze > requirements.txt`

Commit and push when done.

## Accessing database

Database can be accessed through a query using SQLAlchemy.

In root folder, enter the python interpreter. Then, run

`from app.models import User`

to obtain User database instance, which can be queried.

To query all:

`User.query.all()`

## Account type information

*Root* - cannot be deleted normally, has all admin rights. Password is TBD.

*Admin* - Manage user database. No restrictions.

## DDNS service info

DDNS service is provided by FreeDNS.

Router is configured to update its public IP address every 21 days unless otherwise configured.
