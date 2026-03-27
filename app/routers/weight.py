from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
# from app.main import templates, weight

router = APIRouter(prefix="/weight")

weight = ["mg", "gram", 'kg', 'ounce', 'pound']
templates = Jinja2Templates("app/templates")

@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": weight})

@router.get("/{final_number}")
async def root(request: Request, final_number: str = None):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": weight, "final_number": final_number})