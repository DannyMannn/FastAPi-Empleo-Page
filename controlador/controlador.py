import sys
sys.path.append("..")
from fastapi import FastAPI, HTTPException, Request
from modelo import connection as conexion
from modelo import Empleo
from modelo import EmpleoRequestModel, EmpleoResponseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Crear Aplicación
app = FastAPI(title="Empleos Pagina Web", description="Pagina Web de Empleos", version="1.0.0")

# Para levantar el servidor: uvicorn main:app --reload, o el nombre de tu archivo si no es main.

templates = Jinja2Templates (directory="../templates")

# que debe hacer el servidor antes de iniciar
@app.on_event('startup')
def startup():
    if conexion.is_closed():
        conexion.connect()
    conexion.create_tables([Empleo])

@app.on_event('shutdown')
def shutdown():
    if not conexion.is_closed:
        conexion.close()

@app.get('/')
async def index():
    return "Index de la pagina web"

# normalmente FastAPI responde con JSON, pero con
# response_class = HTMLResponse le decimos a la API
# que retorne HTML
@app.get('/empleos', response_class = HTMLResponse)
async def empleos(request: Request):
    empleos = Empleo.select()

    context = { 'request': request, 'empleos':empleos }
    return templates.TemplateResponse("index.html", context)

@app.post('/createEmpleo')
# si un cliente quiere realizar una petición a esta url obligatoriamente
# debe enviar los valores para crear un usuario con los valores de EmpleoRequestModel
async def createEmpleo(empleoRequest: EmpleoRequestModel):
    empleo = Empleo.create(
        pagoMensual = empleoRequest.pagoMensual,
        descripcion = empleoRequest.descripcion
    )
    return empleoRequest

@app.get('/getEmpleo/{empleoId}')
async def getEmpleo(empleoId):
    empleo = Empleo.select().where(Empleo.id == empleoId).first()
    print(empleo)

    if empleo:
        return EmpleoResponseModel(id = empleo.id, pagoMensual = empleo.pagoMensual, descripcion = empleo.descripcion)
    else:
        HTTPException(404, "User not found")