# Wiggle Lunch Platform

A company lunch randomizer: Helps startups gel by randomly assigning eating arrangements 🍔 🍕 🍺



## Installation:

1. Install python3.6 - https://askubuntu.com/questions/865554/how-do-i-install-python-3-6-using-apt-get
2. Install pip - https://askubuntu.com/a/927494/642907 
3. Install pipenv - https://pipenv.readthedocs.io/en/latest/#install-pipenv-today
4. Clone this repo - `git clone https://github.com/selotape/TLP.git` 
5. `cd TLP`
6. Create pipenv env - `pipenv install -r requirements.txt`
6. Activate pipenv env - `pipenv shell`
6. Setup Oauth - https://console.developers.google.com/apis/credentials/oauthclient
6. Place secrets configuration in `TLP/google/oauth/google_secrets.py` labeled `CLIENT_ID` & `CLIENT_SECRET`
7. Run! `PYTHONPATH=. python TLP`
 

## TODO:
* Rewrite Json api to Gmail push notifications
* Slack integration
* Make serverless