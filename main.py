import datetime

from fastapi import FastAPI, Request
from routers import login, post, signup
from db.database import engine
from db.models import Base

app = FastAPI()


@app.get("/")
async def index(request: Request):
    return {
        "Author": "Mikhail C.",
        "docs": f"{request.url._url}docs",
        "github": "https://github.com/konflic/social_api",
        "host": request.client.host,
        "datetime": datetime.datetime.now().strftime("%Y-%b-%d, %A %I:%M:%S"),
    }


try:
    Base.metadata.create_all(bind=engine)
    print("Database connection was successful.\nMetadata crated.")
except Exception as error:
    print(f"Connection to db failed: {error}")

app.include_router(signup.router)
app.include_router(login.router)
app.include_router(post.router)
