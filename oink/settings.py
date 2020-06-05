from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    http_port: int = 8080
    grpc_port: int = 8081
