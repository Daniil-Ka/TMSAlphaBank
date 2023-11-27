import uvicorn

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_htmx import htmx, htmx_init, HXRequest
from keras.src.layers import TextVectorization
from pydantic import BaseModel
from starlette.responses import JSONResponse

from model import Model

app = FastAPI()

# настройка для выдачи статичных файлов
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='static/templates')
htmx_init(templates=templates)

model = Model()
model.load()


class InputModel(BaseModel):
    text: str


@app.get('/', response_class=HTMLResponse)
@htmx("index", "index")
async def index(request: Request):
    return templates.TemplateResponse('index.jinja2', {'request': request})


@app.post('/compute-render')
@htmx('result')
async def compute_render(request: HXRequest):
    text = None
    if request.hx_request:
        form_data = await request.form()
        text = jsonable_encoder(form_data)
    if not text:
        raise Exception('text must not null')

    translated_sentence = model.translate_sentence(text['text'])
    return templates.TemplateResponse("result.jinja2", {"request": request, "result": translated_sentence})


@app.post('/compute', response_class=JSONResponse)
async def compute(input_model: InputModel):
    text = input_model.text
    return {'result': model.predict(text)}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)
