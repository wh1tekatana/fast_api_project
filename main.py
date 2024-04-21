import uvicorn
from fastapi import FastAPI, Response, Path, Query, Body, Header
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
import db
from public.router_users import users_router,classes_router

app = FastAPI()


db.create_tables()
db.populate_classes_table()
db.f_bilder()

app.include_router(users_router)
app.include_router(classes_router)


@app.get("/")
def main():
    return FileResponse("files/index.html")


if __name__ == "__main__":
   uvicorn.run(app,host="127.0.0.1", port=8000)