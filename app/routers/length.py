from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
# from app.main import templates, length

router = APIRouter(prefix="/length")

templates = Jinja2Templates("app/templates")
length = ["mm", "cm", 'dm', 'm', 'km', 'inch', 'foot', 'yard', 'mile']

@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": length})

@router.get("/{final_number}")
async def root(request: Request, final_number: str = None):
    return templates.TemplateResponse(name="index.html", request=request, context={"values": length, "final_number": final_number})