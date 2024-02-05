from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

member_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
member_router.mount('/static', StaticFiles(directory='views/static'), name='static')

@member_router.get('/join', response_class=HTMLResponse)
def join(req: Request):
    return templates.TemplateResponse(
        'join.html', {'request': req})

@member_router.get('/login', response_class=HTMLResponse)
def login(req: Request):
    return templates.TemplateResponse(
        'login.html', {'request': req})

@member_router.get('/myinfo', response_class=HTMLResponse)
def myinfo(req: Request):
    return templates.TemplateResponse(
        'myinfo.html', {'request': req})



