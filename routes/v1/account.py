from fastapi import APIRouter, HTTPException
from mongomock import DuplicateKeyError
from models.user import User, CreateUser, UpdateUser
from beanie import PydanticObjectId

from utils import functions as utils_functions


router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/account")
async def get_account(userID: PydanticObjectId):
    user = await User.get(userID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.model_dump()


@router.post("/account", status_code=201)
async def create_account(user: CreateUser):
    user = User(**user.model_dump())
    try:
        await user.insert()

    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating user")

    refresh_token = utils_functions.create_refresh_token(
        data={
            "email": user.email,
        }
    )

    access_token = utils_functions.create_access_token_from_refresh_token(refresh_token)

    return {"access_token": access_token}


@router.put("/account")
async def update_account(userID: PydanticObjectId, user: UpdateUser):
    user = await User.get(userID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.update(user.model_dump())
    await user.save()
    return user.model_dump()


@router.delete("/account")
async def delete_account(userID: PydanticObjectId):
    user = await User.get(userID)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": "User deleted"}
