
from src.core.application.handlers.common_handlers import CommandHandler
from src.core.application.queries.user.get_user_by_id_query import GetUserByIdQueryRequest, GetUserByIdQueryResponse
from src.core.application.services.user_service import UserService
from src.core.domain.exceptions.user import UserNotFoundError
from src.utils.exceptions import CommandExecutionError


class GetUserByIdHandler(CommandHandler[GetUserByIdQueryRequest, GetUserByIdQueryResponse]):
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    
    async def handle(self, query: GetUserByIdQueryRequest) -> GetUserByIdQueryResponse:
        try:
            user = await self._user_service.get_user_by_id(user_id=query.user_id)
            return GetUserByIdQueryResponse.success_response(
                query_id=query.query_id,
                user=user
            )
        except UserNotFoundError as e:
            raise CommandExecutionError(message="User not found", cause=e) from e
        except Exception as e:
            raise CommandExecutionError("Unexpected error during fetching user", cause=e) from e
        

    async def __call__(self, query: GetUserByIdQueryRequest) -> GetUserByIdQueryResponse:
        return await self.handle(query)