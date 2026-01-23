
from typing import Annotated
from fastapi import APIRouter, Depends

from src.service.test_service import TestService
from src.scheme.user import UserRole
from src.api.dependecy import get_user, require_role, SessionDep
from src.scheme.test import QuestionAnswerCreate, QuestionAnswerRead, QuestionRead, QuestionCreate, QuestionUpdate, TestCreate, TestRead



session_router = APIRouter(prefix="/session")

router = APIRouter(prefix="/test", 
                   tags=["Тестирование"], 
                   dependencies=[Depends(get_user)])

router.include_router(session_router)


def get_serivce(session: SessionDep):
    return TestService(session=session)

TestServiceDep = Annotated[TestService, Depends(get_serivce)]

@router.post("/", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])])
async def create_test(test: TestCreate, service: TestServiceDep):
    return await service.add_test(test)

@router.get("/{id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])])
async def get_test(id: int, service: TestServiceDep) -> TestRead:
    return await service.find_one(id)

@router.post("/{id}/question", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])])
async def add_test_question(id:int, question: QuestionCreate, service: TestServiceDep):
    return await service.add_question(id, question)


@router.delete("/{id}", dependencies=[require_role([UserRole.ADMIN, UserRole.EDITOR])])
async def delete_test(id: int, service: TestServiceDep):
    return await service.delete_test(id)



