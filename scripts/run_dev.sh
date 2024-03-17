echo "Running: uvicorn main:app --reload --port=8000 ..."
cd src
uvicorn main:app --reload --port=8000
