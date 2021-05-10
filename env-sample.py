# create a env.py file from this file (cp env-sample.py env.py) and fill the missing values
# make sure you have pipenv (pip install pipenv) and the latest packages installed (pipenv install)

SECRET_KEY = "token"
# to generate a secret key use the following command
# python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'


# ask the maintainers for these keys
API_KEY = "token"
API_SECRETKEY = "token"
BEARER_TOKEN = "token"
ACCESS_TOKEN = "token"
ACCESS_TOKEN_SECRET = "token"

# public key, nothing secret
MAPBOX_PUB_KEY = "pk.eyJ1IjoiYW5kdGVyOTkiLCJhIjoiY2tueWR0N2o4MWZkYjJvcm1hNXU4eHJqbiJ9.cWh9lYnPyEjGPQF9a1UWuQ"