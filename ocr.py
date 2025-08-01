import time
import sys
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Configuration directement dans le code
AZURE_OCR_ENDPOINT = "https://ocr-main.cognitiveservices.azure.com/"
AZURE_OCR_KEY = "9YvfQeXOHJoI4al7dKKvEGBHma1LiQnew6P4k93t21K90Bjr3or5JQQJ99BFAC5T7U2XJ3w3AAAFACOGqTP6"

def lire_texte_azure(image_path):

    def clean_and_resize_image(input_path, max_size=4000):
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            width, height = img.size
            if max(width, height) > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int(max_size * height / width)
                else:
                    new_height = max_size
                    new_width = int(max_size * width / height)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            cleaned_path = "temp/temp_cleaned.jpg"
            img.save(cleaned_path, format="JPEG", quality=90)
            return cleaned_path

    try:
        cleaned_path = clean_and_resize_image(image_path)
        with open(cleaned_path, "rb") as image_stream:
            client = ComputerVisionClient(AZURE_OCR_ENDPOINT, CognitiveServicesCredentials(AZURE_OCR_KEY))
            read_op = client.read_in_stream(image_stream, raw=True)
            operation_id = read_op.headers["Operation-Location"].split("/")[-1]

            while True:
                result = client.get_read_result(operation_id)
                if result.status.lower() not in ['notstarted', 'running']:
                    break
                time.sleep(1)

            if result.status.lower() == 'succeeded':
                text = "\n".join(
                    line.text
                    for page in result.analyze_result.read_results
                    for line in page.lines
                )
                return text.strip()
            else:
                return "Échec de l'OCR Azure."
    except Exception as e:
        return f"Erreur Azure OCR : {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Veuillez fournir le chemin de l'image.")
    else:
        chemin = sys.argv[1]
        print(lire_texte_azure(chemin))
