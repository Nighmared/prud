FROM python:3.10
WORKDIR /
RUN mkdir -p common/{ prud-db, confloader }
COPY common/prud-db/pruddb.py common/prud-db/pyproject.toml common/prud-db/
COPY common/confloader/confloader.py common/confloader/pyproject.toml common/confloader/
WORKDIR /app
COPY core/requirements.txt requirements.txt
COPY core/local-requirements.txt local-requirements.txt
RUN ["pip","install","-r", "requirements.txt"]
COPY core/alembic.ini alembic.ini
COPY core/alembic alembic
COPY core/main.py main.py
COPY core/prud prud

CMD ["python","main.py"]