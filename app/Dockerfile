FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install fastapi uvicorn pysqlite3 pydantic asyncio SQLAlchemy psycopg2 pandas
COPY . /app/app



CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port", "8000"]