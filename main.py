from fastapi import FastAPI, UploadFile, File, Form
import openbharatocr
import shutil
import os
import uuid
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "My OCR Service is Running"}

@app.post("/verify")
async def verify_document(
    file: UploadFile = File(...), 
    document_type: str = Form(...) 
):
    # 1. Setup paths
    if not os.path.exists("/tmp"):
        os.makedirs("/tmp")
        
    file_ext = file.filename.split(".")[-1]
    safe_filename = f"{uuid.uuid4()}.{file_ext}"
    temp_file_path = os.path.join("/tmp", safe_filename)
    
    try:
        # 2. Save file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Process based on Document Type
        data = {}
        doc_type_upper = document_type.upper().strip()
        print(f"Processing: {doc_type_upper}")

        if doc_type_upper in ["DL", "DRIVING_LICENSE", "DRIVERS LICENSE"]:
            data = openbharatocr.driving_licence(temp_file_path)
            key_check = 'Driving Licence Number'
            
        elif doc_type_upper == "PAN":
            data = openbharatocr.pan(temp_file_path)
            key_check = 'Pan Number'
            
        elif doc_type_upper == "AADHAAR":
            data = openbharatocr.front_aadhaar(temp_file_path)
            key_check = 'Aadhaar Number'
            
        else:
            return {"valid": False, "error": f"Unsupported type: {document_type}"}

        # 4. Validation
        print(f"Extracted Data: {data}")

        if not data or (key_check and not data.get(key_check)):
            return {
                "valid": False, 
                "message": "Could not read ID Number. Image might be blurry.",
                "extracted_raw": data 
            }

        return {
            "valid": True,
            "document_type": doc_type_upper,
            "data": data,
            "source": "My-OpenBharatOCR"
        }

    except Exception as e:
        return {"valid": False, "error": str(e)}

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)