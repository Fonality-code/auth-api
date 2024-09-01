from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
import jwt

from config.config import Settings
from utils import functions as utils_functions
from models.user import User


GOOGLE_CLIENT_ID = Settings().GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = Settings().GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = Settings().GOOGLE_REDIRECT_URI


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


router = APIRouter(
    prefix="",
    tags=["google"],
    responses={404: {"description": "Not found"}},
)


@router.get("/google/login", tags=["google"])
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/google/auth/", tags=["google"])
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    print(user_info.json())

    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Invalid code")

    user_email = user_info.json().get("email")

    # check if user exists
    user = await User.find_one({"email": user_email})
    if not user:
        user = User(
            email=user_email,
            google_id=user_info.json().get("id"),
            first_name=user_info.json().get("given_name"),
            last_name=user_info.json().get("family_name"),
            picture=user_info.json().get("picture"),
            email_verified=True,
        )

        await user.insert()

    refresh_token = utils_functions.create_refresh_token(
        data={
            "email": user.email,
        }
    )
    # TODO store refresh token in database

    access_token = utils_functions.create_access_token_from_refresh_token(refresh_token)

    return {"access_token": access_token}


@router.get("/token")
async def get_token(token: str):
    data = utils_functions.decode_token(token)

    email = data["email"]

    user = await User.find_one({"email": email})
    if user:
        refresh_token = user.refresh_token
        if not refresh_token:
            raise HTTPException(status_code=403, detail="No refresh token found")
        if not utils_functions.validate_access_token(token, refresh_token):
            raise HTTPException(status_code=403, detail="Invalid token")
    else:
        raise HTTPException(status_code=403, detail="User not found")

    return utils_functions.create_access_token_from_refresh_token(refresh_token)
