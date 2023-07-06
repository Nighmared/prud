FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN ["pip","install","-r", "requirements.txt"]
COPY main.py main.py
COPY prud prud

CMD ["python","main.py"]