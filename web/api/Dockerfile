FROM python:3.10
WORKDIR /app
COPY web/api/requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
WORKDIR /
COPY common common
WORKDIR /app
COPY web/api/site-requirements.txt site-requirements.txt
RUN ["pip", "install", "-r", "site-requirements.txt"]

COPY web/api/*.py .
CMD ["python","-m","uvicorn","main:app","--host","0.0.0.0","--port","80"]
