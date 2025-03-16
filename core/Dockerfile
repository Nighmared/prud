FROM python:3.12
WORKDIR /
# RUN mkdir -p common/{prud-db/pruddb, confloader }
COPY common common
WORKDIR /app
COPY core/requirements.txt requirements.txt
COPY core/local-requirements.txt local-requirements.txt
RUN ["pip","install","-r", "requirements.txt"]
COPY core/alembic.ini alembic.ini
COPY core/alembic alembic
COPY core/main.py main.py
COPY core/prud prud

CMD ["python","main.py"]
