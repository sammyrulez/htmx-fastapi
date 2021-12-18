from typing import Any, Type
from fastapi import FastAPI, Request, Form
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic.fields import ModelField
import inspect

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


class OwnerCreate(BaseModel):
    name: str


class Owner(OwnerCreate):
    id: int


class Pet(BaseModel):
    id: int
    name: str
    owner: Owner


owners = [Owner(id=1, name="Sam"), Owner(id=2, name="Max")]


def find_owner(id: int):
    for i, e in enumerate(owners):
        if e.id == id:
            return i


pets = []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/owners/", response_class=HTMLResponse)
async def get_owners_list(request: Request):
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})


@app.get("/owners/new", response_class=HTMLResponse)
async def get_owner_detail(request: Request):
    return templates.TemplateResponse("owner_new.html", {"request": request})


@app.post("/owners/", response_class=HTMLResponse)
async def get_owner_detail(request: Request, form_data: OwnerCreate):
    owners.append(Owner(id=len(owners), name=form_data.name))
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})


@app.get("/owners/{id}", response_class=HTMLResponse)
async def get_owner_detail(request: Request, id: int):
    owner = owners[find_owner(id)]
    print(owner)
    return templates.TemplateResponse("owner_edit.html", {"request": request, "owner": owner})


@app.post("/owners/{id}", response_class=HTMLResponse)
async def get_owner_detail(request: Request, id: int, form_data: Owner):
    owners[find_owner(id)] = form_data
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})
