import os
import sys
import re
import json
import vertexai
import vertexai.generative_models as genai



def gemini_describe_image(user_id, message_id):
    GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
    vertexai.init(project=GCP_PROJECT_ID, location="us-central1")
    gsc_image_path = "gs://vertex_ai_search_data_9999/LINEUSER/test/image/001.jpg"
    print(gsc_image_path)

    image_file = genai.Part.from_uri(
        gsc_image_path,
        mime_type="image/jpg",
    )
    # https://github.com/google-gemini/generative-ai-python/blob/e9b0cdefb66bb4efa8bccef4809b7c8bd7d578b2/samples/controlled_generation.py#L147-L160
    text_prompt = """จงอธิบายรูปภาพนี้ว่าสินค้าอะไร
            ยกตัวอย่าง: {"explaination":"รูปที่คุณส่งมาเป็นรูปของน้ำดื่ม ยี้ห้อสิงห์ น้ำแร่ธรรมชาติ", "product_description":"น้ำดื่มสิงห์"}
            Use this JSON schema:
            Language = ภาษาไทย
            Recipe = {'explaination': str, 'product_description': str]}
            Return: Recipe
            """

    model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content([image_file, text_prompt])

    pattern = r"(json)\s*(\{.*?\})\s*"
    match = re.search(pattern, response.text, re.DOTALL)
    if match:
        data_dict = json.loads(match.group(2))
    else:
        data_dict = None

    return data_dict


if __name__ == "__main__":
    outer_lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.append(outer_lib_path)
    from commons.manage_secret import load_secrets
    load_secrets("vertex_ai_secret.yml")
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sa.json"
    response = gemini_describe_image("test", "001")
    print(response)
