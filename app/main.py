from fastapi import FastAPI, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .schemas.number import Number
from .routers import length, temperature, weight

app = FastAPI()

app.include_router(length.router)
app.include_router(temperature.router)
app.include_router(weight.router)

app.mount('/app/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates("app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": []})


@app.post("/postdata")
async def number_postdata(number = Form(), convert_to=Form(), convert_from=Form()):
    return RedirectResponse(url=f"/{convert_length(float(number), convert_to=convert_to, convert_from=convert_from)}", status_code=status.HTTP_303_SEE_OTHER)

def convert_length(numb: int,
    convert_from, convert_to) -> str:
    if convert_from in length.length:
        path = "length"
        converter = {'mm': 0.001, 'cm': 0.01, 'dm': 0.1, 'm': 1, 'km': 1000, 'inch': 39.3701, 'foot': 3.28084, 'yard': 1.09361, 'mile': 0.000621371}
    elif convert_from in weight.weight:
        path = "weight"
        converter = {"mg": 0.001, "gram": 1, 'kg': 1000, 'ounce': 28.3495, 'pound': 453.592}
    else:
        path = "temperature"
        # (12 °C × 9/5) + 32
        final = numb
        if convert_from == "Celsius" and convert_to == "Fahrenheit":
            final = (numb*9/5)+32
        elif convert_from == "Kelvin" and convert_to == "Fahrenheit":
            # (12 K − 273,15) × 9/5 + 32
            final = (numb - 273.15)*9/5+32
        elif convert_from == "Kelvin" and convert_to == "Celsius":
            # 12 K − 273,15
            final = numb - 273.15
        elif convert_from == "Fahrenheit" and convert_to == "Celsius":
            # (12 °F − 32) × 5/9
            final = (numb-32)*5/9
        elif convert_from == "Fahrenheit" and convert_to == "Kelvin":
            # (12 K − 273,15) × 9/5 + 32
            final = (numb-32)*5/9+273.15
        elif convert_from == "Celsius" and convert_to == "Kelvin":
            # 12 K − 273,15
            final = numb + 273.15
        return f"{path}/{final}"
    return f"{path}/{numb*(converter[convert_from]/converter[convert_to])}{convert_to}"