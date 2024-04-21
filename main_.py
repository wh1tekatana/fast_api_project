import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()


@app.get("/")
async def p_index():
    return {"FIO": "Каплунов Александр Артемович"}


@app.get("/users", response_class=HTMLResponse)
async def p_users():
    output = "<h3> Phone Number:+7923*****94 </h3>"
    return output

@app.get("/tools", response_class=HTMLResponse)
async def p_tools():
    output = "<h2> <center> Python Junior <br> Designer <br> Artist </center></h2>"
    return output

if __name__ == "__main__":
    uvicorn.run(app = "main:app",host="127.0.0.1",port=500)