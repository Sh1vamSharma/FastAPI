from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session  
from .database import engine, get_db 
from .routers import post, user, auth, vote
from .config import settings

# to create all of the models in main
# when we have alembic we don't need this command to create tables in database
# models.Base.metadata.create_all(bind=engine)

# initiating FastAPI instance.
app = FastAPI()

# list of website/origins which can talk to our API use origins = ["*"] to allow all public domains
# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_posts(db: Session=Depends(get_db)):
    return {"status" : "Welcome to Shivam's first API."}

# Getting the routed path operation from the other files
app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)


  





