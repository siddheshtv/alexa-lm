from fastapi import FastAPI
from routers.database import dbops
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

app.include_router(dbops.router, prefix="/api")

@app.get("/")
async def checker():
    return {"message": "Server Running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
