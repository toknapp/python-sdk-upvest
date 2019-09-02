from environs import Env

from upvest.clientele import UpvestClienteleAPI
from upvest.tenancy import UpvestTenancyAPI
from upvest.__pkginfo__ import DEFAULT_USERAGENT

# Read .env into os.environ
env = Env()
env.read_env()


def create_tenancy_client():
    API_KEY = env.str("API_KEY")
    API_SECRET = env.str("API_SECRET")
    API_PASSPHRASE = env.str("API_PASSPHRASE")
    return UpvestTenancyAPI(API_KEY, API_SECRET, API_PASSPHRASE, user_agent="%s SDK Tests" % DEFAULT_USERAGENT)


def create_oauth_client(username, password):
    CLIENT_SECRET = env.str("CLIENT_SECRET")
    CLIENT_ID = env.str("CLIENT_ID")
    return UpvestClienteleAPI(
        CLIENT_ID, CLIENT_SECRET, username, password, user_agent="%s SDK Tests" % DEFAULT_USERAGENT
    )
