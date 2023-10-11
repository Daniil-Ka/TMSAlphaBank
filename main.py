from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx, htmx_init

from cases import Cases

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='static/templates')
htmx_init(templates=templates)


@app.get('/', response_class=HTMLResponse)
@htmx("index", "index")
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post('/compute')
async def compute(text=Form()):
    return {
        Cases.Nominative: 'text',
        Cases.Genitive: 'text',
        Cases.Dative: 'text',
        Cases.Accusative: 'text',
        Cases.Instrumental: 'text',
        Cases.Prepositional: 'text'
    }
