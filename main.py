from fastapi import FastAPI

from app.routes.board import board_router
from app.routes.member import member_router

app = FastAPI()

# 외부 route 파일 불러오기
app.include_router(member_router)
app.include_router(board_router, prefix='/board')


@app.get("/")
async def index():
    return {"message": "Hello World"}



if __name__ == '_main__':
    import uvicorn
    uvicorn.run('main.app', reload=True)

