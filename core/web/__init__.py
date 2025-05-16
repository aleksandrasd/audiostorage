from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

frontend_router = APIRouter()


@frontend_router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    with open("frontend/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@frontend_router.get("/login", response_class=HTMLResponse)
def read_root(request: Request):
    with open("frontend/login.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@frontend_router.get("/list", response_class=HTMLResponse)
def read_root(request: Request):
    with open("frontend/list.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@frontend_router.get("/search", response_class=HTMLResponse)
def read_root(request: Request):
    with open("frontend/search.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@frontend_router.get("/user", response_class=HTMLResponse)
def read_root(request: Request):
    with open("frontend/user.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)