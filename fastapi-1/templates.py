from fastapi import FastAPI,Request

import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
StaticFiles(directory="static")

templates = Jinja2Templates(directory="templates")

datos = {"0": "Python", "1": "Java", "2": "PHP", "3": "JavaScript", "4": "C++"} # variable global para el almacenamiento de datos

@app.get("/")
def raiz(request:Request):
    sin_codificar = json.dumps(datos) # convierte código python (diccionario) a JSON serializado
    json_datos = json.loads(sin_codificar) # convierte código JSON a código Python
    return templates.TemplateResponse("inicio.html",{"request":request,"datos":json_datos})


@app.post("/agregar")
async def agregar(request:Request):
    formdata = await request.form() # dato del formulario HTML

    id = len(datos) # longitud de la dictionary de datos para crear un nuevo ID
    datos[str(id)] = formdata["nuevoDato"]

    return RedirectResponse("/",303) # redirecciona a la página índice

@app.get("/eliminar/{id}")
async def eliminar(request:Request,id:str):
    del datos[id]
    return RedirectResponse("/",303)