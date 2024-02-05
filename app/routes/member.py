from fastapi import APIRouter

member_router = APIRouter()

@member_router.get('/join')
def join():
    return {'msg': 'Hello, Join!'}

@member_router.get('/login')
def login():
    return {'msg': 'Hello, login!'}

@member_router.get('/myinfo')
def myinfo():
    return {'msg': 'Hello, myinfo!'}



