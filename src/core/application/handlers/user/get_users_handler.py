
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.application.queries.user.get_users_query import GetUsersQueryRequest, GetUsersQueryResponse
from src.core.application.services.user_service import UserService
from src.core.domain.exceptions.user import UsersNotFoundError
from src.utils.exceptions import CommandExecutionError


class GetUsersHandler(CommandHandler[GetUsersQueryRequest, GetUsersQueryResponse]):
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    
    async def handle(self, query: GetUsersQueryRequest) -> GetUsersQueryResponse:
        try:
            users = await self._user_service.get_users(query=query)
            return GetUsersQueryResponse.success_response(
                query_id=query.query_id,
                users=users
            )
        except UsersNotFoundError as e:
            raise CommandExecutionError(message="Users not found", cause=e) from e
        except Exception as e:
            print(e)
            raise CommandExecutionError("Unexpected error during fetching user", cause=e) from e
        

    async def __call__(self, query: GetUsersQueryRequest) -> GetUsersQueryResponse:
        return await self.handle(query)