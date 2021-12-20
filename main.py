from typing import Any, List, Optional, Type, ForwardRef
import uuid
from fastapi import FastAPI, Request, Form
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic.fields import ModelField
import inspect

from pydantic.types import UUID1

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


OwnerPetModel = ForwardRef("Owner")


class Pet(BaseModel):
    id: int
    name: str
    owner: Optional[OwnerPetModel] = None


class OwnerCreate(BaseModel):
    name: str
    pets: Optional[List[Pet]] = []


class Owner(OwnerCreate):
    id: int


owners = [Owner(id=1, name="Sam", pets=[Pet(id=0, name="Chicca")]),
          Owner(id=2, name="Max")]


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
async def new_owner(request: Request):
    return templates.TemplateResponse("owner_form.html", {"request": request,"owner":Owner(id=0,name="")})


@app.post("/owners/", response_class=HTMLResponse)
async def new_owner_save(request: Request, form_data: OwnerCreate):
    new_owner = Owner(id=1 + len(owners), name=form_data.name)
    owners.append(new_owner)
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})

@app.delete("/owners/{id}", response_class=HTMLResponse)
async def delete_owner(request: Request,id: int):
    owner = owners[find_owner(id)]
    owners.remove(owner)
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})


@app.get("/owners/{id}", response_class=HTMLResponse)
async def get_owner_detail(request: Request, id: int):
    owner = owners[find_owner(id)]
    return templates.TemplateResponse("owner_form.html", {"request": request, "owner": owner})


@app.post("/owners/{id}", response_class=HTMLResponse)
async def update_owner_detail(request: Request, id: int, form_data: Owner, ):
    owners[find_owner(id)] = form_data
    return templates.TemplateResponse("owners.html", {"request": request, "owners": owners})


@app.get("/pets/new_row", response_class=HTMLResponse)
async def new_pet_detail(request: Request):

    return templates.TemplateResponse("pet_new_row.html", {"request": request,"tmp_id": uuid.uuid1() })
