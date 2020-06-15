"""
Starts an inference server.
"""
from .server import MLServer
from .settings import Settings


def main():
    # TODO: Build from CLI flags
    settings = Settings()

    server = MLServer(settings)
    server.start()


if __name__ == "__main__":
    main()
