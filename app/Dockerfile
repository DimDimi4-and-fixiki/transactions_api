FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install fastapi uvicorn pysqlite3 pydantic asyncio SQLAlchemy psycopg2 pandas GitPython
COPY . /app/app
COPY logging_tools /app/app/logging_tools
COPY utilities /app/app/utilities


CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port", "8000"]