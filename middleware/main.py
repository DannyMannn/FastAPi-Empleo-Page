from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app  = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

@app.middleware("http")
async def verificarUserAgent(request: Request, callNext):
    #callNext pasa al siguiente endpoint
    if request.headers['User-Agent'].find("Mobile") == -1:
        response=await callNext(request)
        return response
    else:
        return JSONResponse(
            content=
            {"message": "no permitimos mobiles" }, status_code=401
            )

@app.get("/")
def main():
    return ("dentro de main")

@app.get("/getInfo")
def main():
    return JSONResponse(content={"hello": "a todos" }, status_code=200)


# async function getData(){
#     const res = await fetch("http://127.0.0.1:8000")
#     const data = await = res.json()

#     if(res.ok)
#         return data
#     else
#         throw new Error(data)

# }

# let promise = getData()