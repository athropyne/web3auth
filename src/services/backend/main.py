import asyncio
from contextlib import asynccontextmanager

import fastapi_cli.cli
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import core.config
import services.accounts.dto
from core.config import logger
from core.infrastructures import Database, w3
from core.schema import metadata
from services.accounts.routes import router as accounts_router
from services.security.routes import router as security_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not w3.is_address(core.config.settings.ROOT_ADDRESS):
        raise ValueError("Неверный адрес корневого кошелька")
    logger.debug("конревой адрес подтвержден")
    database = Database()
    await database.init(metadata)
    logger.debug("база данных проинициализирована")
    yield
    await database.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(accounts_router)
app.include_router(security_router)

if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    fastapi_cli.cli.run(
        host=core.config.settings.SERVER_HOST,
        port=core.config.settings.SERVER_PORT
    )
