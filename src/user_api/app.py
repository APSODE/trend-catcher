from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.user_api.auth import OAuth2Client
from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.router.internal import INTERNAL_ROUTERS
from src.user_api.router.external import EXTERNAL_ROUTERS
from user_api.handler.exception_handler import register_exception_handlers


class UserAPI(FastAPI):
    def __init__(self):
        super().__init__(
            title = "User API",
            description = "user manage API",
            lifespan = self.lifespan
        )
        self._set_up_middlewares()
        self._setup_exception_handlers()
        self._setup_routers()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        import src.user_api.model  # noqa: F401
        await DatabaseCreator().init_db()

        yield
        await OAuth2Client.close()
        await DatabaseCreator().engine.dispose()

    def _setup_exception_handlers(self) -> None:
        register_exception_handlers(self)

    def _set_up_middlewares(self):
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routers(self) -> None:
        routers = INTERNAL_ROUTERS + EXTERNAL_ROUTERS

        for router in routers:
            self.include_router(router)



UserAPI = UserAPI()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:UserAPI", host = "0.0.0.0", port = 5175, workers = 8, log_level = "info", reload = True)