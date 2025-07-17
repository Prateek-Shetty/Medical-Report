import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import mimetypes

def extract_text(file_bytes: bytes, filename: str) -> str:
    try:
        ext = mimetypes.guess_type(filename)[0]

        if ext == "application/pdf":
            pdf = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = ""
            for page in pdf:
                page_text = page.get_text()
                if page_text.strip():
                    full_text += page_text
                else:
                    # fallback to OCR for image-based pages
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    full_text += pytesseract.image_to_string(img)
            return full_text.strip()

        elif ext and ext.startswith("image/"):
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
            return text.strip()

        else:
            return "Unsupported file type"

    except Exception as e:
        print(f"❌ Error in extract_text: {e}")
        return "Error during text extraction"
