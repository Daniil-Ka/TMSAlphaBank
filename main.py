from typing import Any, Dict

import uvicorn
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, parse_obj_as
from fastapi import FastAPI, Request, Form, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_htmx import htmx, htmx_init, HXRequest
from pydantic.dataclasses import dataclass

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='static/templates')
htmx_init(templates=templates)


@dataclass
class InputModel(BaseModel):
    text: str


@app.get('/', response_class=HTMLResponse)
@htmx("index", "index")
async def index(request: Request):
    return templates.TemplateResponse('index.jinja2', {'request': request})


@app.post('/compute-render')
@htmx('result')
async def compute_render(request: HXRequest):
    if request.hx_request:
        form_data = await request.form()
        text: str = jsonable_encoder(form_data)

    input_model: InputModel = InputModel.__pydantic_validator__.validate_python(text)
    return {'result': input_model.text}


@app.post('/compute', response_class=JSONResponse)
async def compute(input_model: InputModel):
    return {'result': input_model.text}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)
