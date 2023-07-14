export API_DB_URL=sqlite:///../../core/polyring.db
source ../../bin/activate
python -m uvicorn main:app --port 8000
