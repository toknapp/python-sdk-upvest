import os

API_VERSION = "1.0"
OAUTH_PATH = "/clientele/oauth2/token"
ENCODING = "utf-8"
GRANT_TYPE = "password"
SCOPE = "read write echo transaction"

UPVEST_API_TARGET = os.getenv("UPVEST_API_TARGET", default="https://api.playground.upvest.co/")
PRIVATE_KEY_BASE64 = os.getenv("PRIVATE_KEY_BASE64")
