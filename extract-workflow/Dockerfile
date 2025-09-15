FROM python:3.11-slim

RUN pip install psycopg2-binary

RUN pip install python-dotenv

RUN pip install streamlit

CMD ["streamlit", "run", "/workspace/extract-workflow/app.py"]