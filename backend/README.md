# Backend (FastAPI)

Quick start:

```bash
# create virtualenv
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# run the server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Healthcheck: GET http://127.0.0.1:8000/
