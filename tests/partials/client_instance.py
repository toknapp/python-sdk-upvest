from environs import Env

from upvest.tenancy import UpvestTenancyAPI
from upvest.clientele import UpvestClienteleAPI

# Read .env into os.environ
env = Env()
env.read_env()

def create_tenancy_client():
    API_KEY = env.str('API_KEY')
    API_SECRET = env.str('API_SECRET')
    API_PASSPHRASE = env.str('API_PASSPHRASE')
    return UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE)


def create_oauth_client(username, password):
    CLIENT_SECRET = env.str('CLIENT_SECRET')
    CLIENT_ID = env.str('CLIENT_ID')
    return UpvestClienteleAPI(CLIENT_ID, CLIENT_SECRET, username, password)
