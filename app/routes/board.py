from fastapi import APIRouter

board_router = APIRouter()

@board_router.get('/list')
def list():
    return {'msg': 'Hello, Board List!'}

@board_router.get('/write')
def write():
    return {'msg': 'Hello, Board Write!'}

@board_router.get('/view')
def view():
    return {'msg': 'Hello, Board View!'}



