from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import os
from typing import List, Optional
from schemas import (InputModelCircuitDiode,OutputModelCircuitDiode)
from services.newton_raphson import *

app = FastAPI(
    title="NuMaaS - Numerical Methods as a Software",
    description="the first Numerical Methods as a Software development",
    version="0.0.1"
)

templates_dir=os.path.join(os.path.dirname(__file__),"templates")
templates = Jinja2Templates(directory=templates_dir)

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(
        request=request,name= "home.html"
    )

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
