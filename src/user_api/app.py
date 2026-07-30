from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI

from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler
from src.user_api.handler.exception_handler.account_exception_handler import InvalidCredentialDataHandler, IsAlreadyExistLoginIDHandler
from src.user_api.router.base_router import BaseRouter
from src.user_api.router.user_router import UserRouter



class UserAPI(FastAPI):
    def __init__(self):
        super().__init__(
            title = "User API",
            description = "user manage API",
            lifespan = self.lifespan
        )

        self._setup_exception_handlers()
        self._setup_routers()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        import src.user_api.model  # noqa: F401
        await DatabaseCreator().init_db()

        yield

        await DatabaseCreator().engine.dispose()

    def _setup_exception_handlers(self) -> None:
        handlers: List[BaseExceptionHandler] = [
            InvalidCredentialDataHandler(),
            IsAlreadyExistLoginIDHandler(),
        ]

        for handler in handlers:
            self.add_exception_handler(handler.get_status_code, handler)

        return None


    def _setup_routers(self) -> None:
        routers: List[BaseRouter] = [
            UserRouter(),
        ]

        for router in routers:
            self.include_router(router)



UserAPI = UserAPI()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:UserAPI", host = "0.0.0.0", port = 8080, workers = 8, log_level = "info", reload = True)