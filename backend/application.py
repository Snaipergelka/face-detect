from fastapi import FastAPI
from backend.containers import Container
from backend.handlers import router


def create_app() -> FastAPI:
    container = Container()

    description = "Сервис, реализующий возможность найти лица на фото и выделить их."
    app = FastAPI(title="FaceDetection",
                  description=description)
    app.include_router(router)

    app.container = container
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
