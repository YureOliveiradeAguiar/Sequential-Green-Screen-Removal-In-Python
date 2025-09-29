import os
from PIL import Image

# === Configuration ===
input_folder = "images"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

green_rgb = (0, 255, 0)
tolerance = 128  # Range of similarity to green
resize_to = (1080, 1080)  # <-- Set your desired (width, height)

# === Helper: Color similarity ===
def is_similar_color(color1, color2, tol):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return abs(r1 - r2) < tol and abs(g1 - g2) < tol and abs(b1 - b2) < tol

# === Process Images ===
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        image_path = os.path.join(input_folder, filename)
        image = Image.open(image_path).convert("RGBA")
        pixels = image.getdata()

        new_pixels = []
        for pixel in pixels:
            r, g, b, a = pixel
            if is_similar_color((r, g, b), green_rgb, tolerance):
                new_pixels.append((r, g, b, 0))
            else:
                new_pixels.append((r, g, b, a))

        image.putdata(new_pixels)
        
        # Resize image
        image = image.resize(resize_to, Image.Resampling.LANCZOS)

        out_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
        image.save(out_path, "PNG")
        print(f"Processed and resized: {filename}")

print("All done.")
