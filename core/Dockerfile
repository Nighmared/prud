FROM python:3.10
WORKDIR /
COPY common common
WORKDIR /app
COPY core/requirements.txt requirements.txt
RUN ["pip","install","-r", "requirements.txt"]
COPY core/main.py main.py
COPY core/prud prud

CMD ["python","main.py"]