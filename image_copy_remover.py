from PIL import Image
import imagehash
from pathlib import Path

def find_duplicates(path):
    path = Path(path)
    hashes = {}

    for img in path.glob("*.png"):
        try:
            hash = imagehash.phash(Image.open(img))
            if hash in hashes:
                print(f"Duplikat: {img.name} ≈ {hashes[hash].name}")
                img.unlink()  
            else:
                hashes[hash] = img
        except Exception as e:
            print(f"Fehler bei {img.name}: {e}")

find_duplicates("C:/Users/kevin/Downloads/png")