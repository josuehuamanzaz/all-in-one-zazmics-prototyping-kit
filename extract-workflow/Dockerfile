FROM python:3.11-slim

RUN pip install psycopg2-binary

RUN pip install python-dotenv

RUN pip install streamlit

WORKDIR /workspace/extract-workflow

CMD ["streamlit", "run", "temp.py"]