from fastapi import APIRouter, HTTPException
from mongomock import DuplicateKeyError
from models.user import User, CreateUser


router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}},
)


@router.get("/account")
async def get_account():
    return {"account": "account"}


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
    return user.model_dump()
