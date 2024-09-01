import jwt
import uuid
from datetime import datetime, timedelta
from config.config import Settings

SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = "HS256"


def create_refresh_token(data: dict, exp_days: int = 30):

    unique_id = str(uuid.uuid4())

    refresh_token_payload = {
        "sub": unique_id,
        "data": data,
        "exp": datetime.now()
        + timedelta(days=exp_days),  # Refresh token valid for 30 days
    }

    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return refresh_token


def create_access_token_from_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        data = payload.get("data")

        if not data:
            raise ValueError("Invalid refresh token data")

        access_token_payload = {
            "sub": payload.get("sub"),
            "data": data,
            "exp": datetime.now()
            + timedelta(minutes=15),  # Access token valid for 15 minutes
        }

        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return access_token

    except jwt.ExpiredSignatureError:
        raise ValueError("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid refresh token")


def validate_access_token(access_token: str, refresh_token: str):
    try:
        # Decode the refresh token to get its payload
        refresh_payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Decode the access token to get its payload
        access_payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if the access token has expired
        if datetime.utcnow() > datetime.fromtimestamp(access_payload.get("exp")):
            raise ValueError("Access token has expired")

        # Check if the access token was issued with the same unique_id as the refresh token
        if access_payload.get("sub") != refresh_payload.get("sub"):
            raise ValueError("Access token was not issued with this refresh token")

        # Optionally: Ensure that the data in the access token matches the refresh token data
        if access_payload.get("data") != refresh_payload.get("data"):
            raise ValueError("Access token data does not match the refresh token data")

        # If all checks pass, the access token is valid
        return True

    except jwt.ExpiredSignatureError:
        raise ValueError("Access token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid access token")


# return token data if token is fine
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("data")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")