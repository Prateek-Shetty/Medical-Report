# Hospital

mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000

pip install fastapi uvicorn pymongo python-dotenv PyMuPDF requests python-multipart
pip freeze > requirements.txt


npm run dev
npm run electron