from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel # Para definir esquemas y reglas para los modelos
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid # Crea un objeto uuid que es una cadena de caracteres aleatorios. uuid genera una ID único.
import uvicorn

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
StaticFiles(directory="static")

templates = Jinja2Templates (directory="templates")

# Arreglo global que guarda diccionarios (cada diccionario representa un objeto de la BD)
empleos = []

# Post model
class Empleo(BaseModel):
    id: Optional[str]
    puesto: str
    empresa: str
    pagoMensual: str
    created_at: datetime =  datetime.now()
    published_at: Optional[datetime] 
    published: Optional[bool] = False

@app.get('/')
def read_root():
    return {"welcome": "Welcome to my API"}

@app.get('/empleos', response_class = HTMLResponse)
async def getEmpleos(request: Request):

    context = { 'request': request, 'empleos':empleos }
    return templates.TemplateResponse("empleos.html", context)

@app.post('/empleos')
async def save_empleos(post: Empleo):
    # formdata = await request.form() # dato del formulario HTML
    # empleo = {}
    # empleo["puesto"] = formdata["puesto"]
    # empleo["pagoMensual"] = formdata["pagoMensual"]
    # empleo["empresa"] = formdata["empresa"]
    # empleo["id"] = str(uuid())
    # empleos.append(empleo)
    #return RedirectResponse("/empleos",303) # redirecciona a la página índice
    
    post.id = str(uuid())
    empleos.append(post.dict())
    return empleos[-1]

@app.get('/empleos/{empleo_id}')
def get_empleo(empleo_id: str):
    for empleo in empleos:
        if empleo["id"] == empleo_id:
            return empleo
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete('/borrarEmpleo/{empleo_id}')
def delete_empleo(empleo_id: str):
    for index, post in enumerate(empleos):
        if post["id"] == empleo_id:
            empleos.pop(index)
            return {"message": "Empleo has been deleted succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put('/empleos/{empleo_id}')
def update_empleo(empleo_id: str, updatedEmpleo: Empleo):
    for index, post in enumerate(empleos):
        if post["id"] == empleo_id:
            empleos[index]["puesto"]= updatedEmpleo.dict()["puesto"]
            empleos[index]["pagoMensual"]= updatedEmpleo.dict()["pagoMensual"]
            empleos[index]["empresa"]= updatedEmpleo.dict()["empresa"]
            return {"message": "Empleo has been updated succesfully"}
    raise HTTPException(status_code=404, detail="Item not found")