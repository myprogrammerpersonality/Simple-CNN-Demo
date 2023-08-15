from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")  # This line serves static files

templates = Jinja2Templates(directory="templates")  # Specify the directory where your templates are

@app.get("/", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/ping")
def read_root():
    return {"Hello": "World"}

# Create a Mangum instance with the app
lambda_handler = Mangum(app)
