from fastapi import APIRouter
from typing import List
from ...crud.repositories import QuestionRepository
from ...models.game_model import QuestionRead

router = APIRouter()


@router.get("/get_random_question",
            response_model=QuestionRead,
            description="Get a random question",
            tags=["question"])
async def get_random_question_route():
    return await QuestionRepository.get_random()


@router.get("/get_all_questions",
            response_model=List[QuestionRead],
            description="List all available questions",
            tags=["question"])
async def get_all_questions_route():
    return await QuestionRepository.list()
