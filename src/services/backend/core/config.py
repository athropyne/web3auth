import logging

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "web3"
    POSTGRES_SOCKET: str = "localhost:5432"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24 * 15
    TOKEN_SECRET_KEY: str = "supersecretkey"
    ETH_NODE_HTTP_PROVIDER_URI: HttpUrl = "https://mainnet.infura.io/v3/13bc3152bbde404583eb96f7f771d10e"
    ROOT_ADDRESS: str
    RAW_MESSAGE_FOR_SING: str = "sign this message please"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False


settings = Settings()

logger = logging.getLogger()
logger.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(console_handler)
