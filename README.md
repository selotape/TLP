# TLP
Wiggle Lunch Platform.

I'll tell you all about it when it's good and ready!

## Installation:


1. Install Python3.6 - https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get
2. Install Pip - https://askubuntu.com/a/927494/642907 
3. Install Pipenv - https://pipenv.readthedocs.io/en/latest/#install-pipenv-today
4. Clone the repo - `git clone https://github.com/selotape/TLP.git` 
5. `cd TLP`
6. Create pipenv - `pipenv install -r requirements.txt`
6. Activate pipenv - `pipenv shell`
6. Place secrets configuration in `TLP/google/oauth/google_secrets.py`
7. Run! `PYTHONPATH=. python` 
 

## TODO:
* Use flask-sqlalchemy
* Rewrite Json api to Gmail push notifications