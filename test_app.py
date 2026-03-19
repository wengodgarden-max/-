from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/test")
async def test():
    return {"test": "success"}
