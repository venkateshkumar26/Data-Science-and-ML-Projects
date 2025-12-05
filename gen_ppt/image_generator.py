import os
import time
from typing import List, Dict
import torch
from diffusers import AutoPipelineForText2Image

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Loading SD-Turbo (small model)...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sd-turbo",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

def generate_images(image_prompts: List[str]) -> Dict[int, str]:
    run_id = str(int(time.time()))
    output_dir = os.path.join("images", run_id)
    os.makedirs(output_dir, exist_ok=True)

    results = {}

    images = pipe(
        image_prompts,
        num_inference_steps=4,    # Turbo = 4 steps
        guidance_scale=0.0        # Turbo requires CFG=0
    ).images

    for i, img in enumerate(images):
        filename = os.path.join(output_dir, f"slide_{i}.png")
        img.save(filename)
        results[i] = filename

    return results
