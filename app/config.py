from pydantic import BaseSettings

class Settings(BaseSettings):
    cvm_mongodb_url: str = "mongodb://root:root@127.0.0.1:27017/cvm_extractor?retryWrites=true&w=majority&authSource=admin"
    cvm_mongodb_db_name: str = "cvm_extractor"

settings = Settings()