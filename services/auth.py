from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.config import Config
from config.config import Settings
from authlib.integrations.starlette_client import OAuth

GOOGLE_CLIENT_ID = Settings().GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = Settings().GOOGLE_CLIENT_SECRET


if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set")

config_data = {
    "GOOGLE_CLIENT_ID": GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": GOOGLE_CLIENT_SECRET,
}


startlette_config = Config(".env")

oauth = OAuth(startlette_config)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"

oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account",  # force to select account
    },
)
oauth_bearer = OAuth2PasswordBearer(tokenUrl="token")
