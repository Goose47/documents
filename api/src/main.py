from fastapi import Request
import uvicorn
from fastapi import FastAPI

from src.api.responses.api_response import ApiResponse
from src.config.app.config import settings_app
from src.utils.validator.exceptions import AppValidationException

from src.utils.redis import redis
from src.api.routers.documents import router as docs_router
from src.api.routers.files import router as files_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings_app.APP_NAME,
        debug=settings_app.DEBUG,
        version=settings_app.APP_VERSION
    )

    application.include_router(docs_router)
    application.include_router(files_router)

    return application


app = get_application()

# admin = setup_admin(app, db_manager.engine)


@app.on_event("startup")
async def startup_event():
    await redis.init_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await redis.close_pool()


@app.exception_handler(AppValidationException)
async def validation_failed(request: Request, exc: AppValidationException):
    return ApiResponse.errors(exc.errors, status_code=422)

if __name__ == "__main__":
    uvicorn.run(
        app=settings_app.UVICORN_APP_NAME,
        host=settings_app.UVICORN_HOST,
        port=settings_app.UVICORN_PORT,
        reload=settings_app.UVICORN_RELOAD
    )
