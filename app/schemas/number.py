from typing import Literal
from pydantic import BaseModel


class Number(BaseModel):
    number: int
    convert_from: Literal["mm", "cm"]
    convert_to: Literal["mm", "cm"]