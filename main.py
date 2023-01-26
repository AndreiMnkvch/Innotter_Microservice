from fastapi import FastAPI
from consumer import consume


app = FastAPI()


@app.get("/")
async def root():
    return {"Works": "Fine"} 
    
app.on_event("startup")
consume()
