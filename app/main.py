from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import issue, citizen, auth, decisionmaker, focus
from .config import settings

#building tables of DB
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins= ["*"]

app.add_middleware(
    CORSMiddleware, #function runs before each request
    allow_origins=origins, #list of domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(issue.router)
app.include_router(citizen.router)
app.include_router(decisionmaker.router)
app.include_router(focus.router)
app.include_router(auth.router)

@app.get("/") 
def home(): 
    return{"Message": "Thanks for using the app!"}


