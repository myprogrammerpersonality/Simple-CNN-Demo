from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum
import torchvision
from torchvision.models.detection import fasterrcnn_mobilenet_v3_large_320_fpn
import torch
from PIL import Image
import cv2
import io
import numpy as np
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Set TORCH_HOME to the same directory as in the Dockerfile
os.environ["TORCH_HOME"] = "/var/task/torch_cache"
model = fasterrcnn_mobilenet_v3_large_320_fpn(pretrained=True)
model.eval()

def predict(img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    tensor = torch.unsqueeze(torchvision.transforms.functional.to_tensor(img), 0)
    with torch.no_grad():
        prediction = model(tensor)
    return prediction

@app.get("/", response_class=HTMLResponse)
async def chatbot_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.post("/uploadfile/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Unable to decode image")

        prediction = predict(img)
        
        for box, score in zip(prediction[0]['boxes'], prediction[0]['scores']):
            if score > 0.5:
                cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)

        _, img_byte_arr = cv2.imencode('.png', img)
        
        return templates.TemplateResponse("base.html", {"request": request, "image": img_byte_arr.tobytes()})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ping")
def read_root():
    return {"Hello": "World"}

lambda_handler = Mangum(app)
