packages = [
   "fastapi",
        "uvicorn",
        "python-multipart",
        "openbharatocr",
        "opencv-python-headless",
        "Pillow",
        "numpy",
        "python-dateutil"
]

with open("requirements.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(packages))

print("✅ requirements.txt has been fixed successfully!")