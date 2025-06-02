# coding utf-8

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.domain.conf import app_conf

from src.domain.entities.core import IConfEnv

from src.interface.server.components import PixVerseRouter


def main() -> FastAPI:
    conf: IConfEnv = app_conf()

    app = FastAPI(**conf.app_config)
    app_router = PixVerseRouter(app, conf)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
    )
    app_router.create()

    return app


if __name__ == "__main__":
    main()
