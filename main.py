import numpy as np
import uvicorn
from fastapi.encoders import jsonable_encoder
from keras.src.layers import TextVectorization
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_htmx import htmx, htmx_init, HXRequest
import tensorflow as tf
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from typing import Optional

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='static/templates')
htmx_init(templates=templates)


class InputModel(BaseModel):
    text: str


@app.get('/', response_class=HTMLResponse)
@htmx("index", "index")
async def index(request: Request):
    return templates.TemplateResponse('index.jinja2', {'request': request})


def translate_sentence(sentence, model, vectorizer):
    sequence = vectorizer([sentence]).numpy()
    predicted_sequence = model.predict(sequence)
    predicted_sentence = ' '.join([vectorizer.get_vocabulary()[i] for i in np.argmax(predicted_sequence, axis=2)[0]])
    return predicted_sentence


@app.post('/compute-render')
@htmx('result')
async def compute_render(request: HXRequest):
    if request.hx_request:
        form_data = await request.form()
        text: str = jsonable_encoder(form_data)
    text = 'Ленинский суд'

    data = [
        "The sky is blue.",
        "Grass is green.",
        "Hunter2 is my password.",
    ]

    model = tf.keras.models.load_model("my_model")
    print(model.predict(text))
    vectorizer = TextVectorization(output_mode='int')
    # vectorizer.adapt(text)
    translated_sentence = translate_sentence(text, model, vectorizer)

    return templates.TemplateResponse("result.html", {"request": request, "result": predicted_sentence})
    # new_model = tf.keras.models.load_model('my_model')
    # result = new_model.predict(text)
    # return {'result': new_model}


@app.post('/compute', response_class=JSONResponse)
async def compute(input_model: InputModel):
    text = input_model.text
    new_model = tf.keras.models.load_model('my_model')
    return {'result': new_model}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)
