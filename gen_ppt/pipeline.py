from gen_ppt.llm_outline import outline_ppt
from gen_ppt.image_generator import generate_images
from gen_ppt.ppt_builder import create_ppt

def run_pipeline(title:str,openai_client) -> str:
    outline=outline_ppt(openai_client,title)
    image_prompts=[slide.get("image_prompt","") for slide in outline.get("slides",[])]
    image_paths=generate_images(image_prompts)
    ppt_path=create_ppt(outline,image_paths)
    return ppt_path
