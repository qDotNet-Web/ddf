from fastapi import APIRouter, HTTPException
from ...schemas.user_schema import UserCreate, UserDisplay
from ...crud.user_crud import create_user, get_user_by_email

router = APIRouter()


@router.post("/users/", response_model=UserDisplay)
async def create_user_route(user: UserCreate):
    db_user = await get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email bereits registriert")
    return await create_user(user)


@router.get("/users/{user_id}", response_model=UserDisplay)
async def read_user_route(user_id: str):
    db_user = await get_user_by_email(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User nicht gefunden")
    return db_user
