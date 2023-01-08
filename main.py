import datetime
import uvicorn

from fastapi import FastAPI, Request
from routers import login, post, signup
from db.database import engine
from db.models import Base
from config.settings import settings

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


app.include_router(signup.router)
app.include_router(login.router)
app.include_router(post.router)

if __name__ == "__main__":

    try:
        Base.metadata.create_all(bind=engine)
        print("Database connection was successful.\nMetadata crated.")
    except Exception as error:
        print(f"Connection to db failed: {error}")

    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
