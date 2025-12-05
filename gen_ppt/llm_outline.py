import json 
from typing import List, Dict, Any
import textwrap

def outline_ppt(openai_client, title:str,model:str="gpt-4o-mini") -> Dict[str, Any]:
    prompt = textwrap.dedent(f"""
    You are a slide-outline generator. Given a single project title, return a JSON object with a "slides" array.
    Each slide object must contain:
      - "title": short string (5-7 words)
      - "bullets": 5 points related to the title
      - "image_prompt": a short text prompt for generating an image, or empty string if none.
    Return ONLY valid JSON and nothing else.

    Input title: "{title}"
    """)

    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=1000,
    )
    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        import re
        m = re.search(r'\{.*\}', raw, flags=re.DOTALL)
        if m:
            data = json.loads(m.group(0))
        else:
            raise ValueError(f"Failed to parse JSON: {e}\nRaw response: {raw}")
    
    if "slides" not in data or not isinstance(data["slides"], list):
        raise ValueError("Invalid JSON response: missing 'slides' array")
    return data
