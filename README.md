# Hospital

# Backend 

## to set up the virtual environment

python -m venv venv    [Only once to setup the virtual environment ]

source venv/Scripts/activate [activate for each terminal ]

uvicorn main:app --reload [To run the dev server]

## Libraries

pip install fastapi
pip install "uvicorn[standard]"
pip install motor
pip install pydantic
pip install python-dotenv
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install requests
pip install aiofiles
pip install EOL
pip install "pydantic[email]"
pip install PyMuPDF
pip install python-multipart
pip install openai
pip install google-generativeai


## For requirements.txt

pip freeze > requirements.txt


## To run the dev server

uvicorn main:app --reload




# Frontend

