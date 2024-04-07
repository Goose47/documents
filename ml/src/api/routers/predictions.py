from fastapi import APIRouter, Request
from src.api.responses.api_response import ApiResponse

from src.database.session_manager import db_manager
from sqlalchemy.future import select

from src.database.models.file import File
from src.config.app.config import settings_app

router = APIRouter()


@router.post("/predict")
async def predict(request: Request):
    data = await request.json()
    if 'image_id' not in data:
        return ApiResponse.error('image_id must be present.')

    async with db_manager.get_session() as session:
        q = select(File).where(File.id == data['image_id'])
        res = await session.execute(q)
        file: File = res.scalar()

    if not file:
        return ApiResponse.error('Image does not exist', 404)

    from fastapi.responses import FileResponse
    image_path = settings_app.APP_PATH + '/storage/' + file.path + file.extension
    return FileResponse(image_path)


    return ApiResponse.payload({'message': 'hellow'})
