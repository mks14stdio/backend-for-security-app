from src.api.dependecy import ArticleServiceDep, require_role
from src.scheme.user import UserRole

from .article import router


@router.put("/{id}/test", dependencies=[require_role(UserRole.ADMIN, UserRole.EDITOR)])
async def put_article_test(
    id: int, test: None, service: ArticleServiceDep
): ...  # TODO: Make put test endpoint


@router.delete(
    "/{id}/test", dependencies=[require_role(UserRole.ADMIN, UserRole.EDITOR)]
)
async def delete_artcile_test(id: int, service: None): ...  # TODO: Make delete test
