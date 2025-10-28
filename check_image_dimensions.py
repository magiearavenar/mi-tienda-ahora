from PIL import Image
import os

# Check slides dimensions
slides_path = "media/slides/"
if os.path.exists(slides_path):
    for filename in os.listdir(slides_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(slides_path, filename)
            try:
                with Image.open(filepath) as img:
                    width, height = img.size
                    print(f"{filename}: {width}x{height} píxeles")
            except Exception as e:
                print(f"Error con {filename}: {e}")
else:
    print("No se encontró la carpeta media/slides/")