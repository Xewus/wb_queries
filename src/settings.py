from pydantic import BaseSettings, SecretStr, HttpUrl


class Settings(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

class BotSettings(Settings):
    TOKEN: SecretStr


class WdCettings(Settings):
    PAGINATION_PAGE: HttpUrl
    PRODUCT_JSON_CARD: HttpUrl


bot_config = BotSettings()
wb_config = WdCettings()
