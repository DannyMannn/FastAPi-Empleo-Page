from pydantic import BaseModel
from typing import Optional # para tener parámetros opcionales

class EmpleoRequestModel(BaseModel):
    pagoMensual: str
    descripcion: str
    # lastname: Optional[str] = None

class EmpleoResponseModel(EmpleoRequestModel):
    id: int