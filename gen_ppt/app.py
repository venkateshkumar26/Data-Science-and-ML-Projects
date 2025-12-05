from fastapi import FastAPI
from fastapi.responses import FileResponse
from gen_ppt.clients import openai_client
from gen_ppt.pipeline import run_pipeline

app = FastAPI()

@app.get("/generate")
def generate_ppt(title: str):
    ppt_path = run_pipeline(title,openai_client)
    return FileResponse(ppt_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation")
