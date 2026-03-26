from fastapi import FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .schemas.number import Number

app = FastAPI()
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates("app/templates")

length = ["mm", "cm", 'dm', 'm', 'km', 'inch', 'foot', 'yard', 'mile']
weight = ["mg", "gram", 'kg', 'ounce', 'pound']
temperature = ['Celsius', 'Fahrenheit', 'Kelvin']


@app.get("/length")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": length})

@app.get("/weight/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": weight})

@app.get("/weight/{final_number}")
async def root(request: Request, final_number: str = None):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": weight, "final_number": final_number})

@app.get("/temperature/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": temperature})

@app.get("/length/{final_number}")
async def root(request: Request, final_number: str = None):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": length, "final_number": final_number})

@app.get("/temperature/{final_number}")
async def root(request: Request, final_number: str = None):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": temperature, "final_number": final_number})

@app.post("/postdata")
async def number_postdata(number = Form(), convert_to=Form(), convert_from=Form()):
    return RedirectResponse(url=f"/{convert_length(float(number), convert_to=convert_to, convert_from=convert_from)}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/")
async def number(number: Number):
    return {"your number is": convert_length(number)}


def convert_length(numb: int,
    convert_from, convert_to) -> str:
    if convert_from in length:
        path = "length"
        converter = {'mm': 0.001, 'cm': 0.01, 'dm': 0.1, 'm': 1, 'km': 1000, 'inch': 39.3701, 'foot': 3.28084, 'yard': 1.09361, 'mile': 0.000621371}
    elif convert_from in weight:
        path = "weight"
        converter = {"mg": 1000, "gram": 1, 'kg': 0.001, 'ounce': 0.035274, 'pound': 0.00220462}
    else:
        path = "temperature"
        converter = {'Celsius': 1, 'Fahrenheit': 1, 'Kelvin': 1}
    return f"{path}/{numb*(converter[convert_from]/converter[convert_to])}{convert_to}"