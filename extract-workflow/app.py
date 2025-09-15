import streamlit as st
import psycopg2
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Single connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# ------------------------
# Function that converts a row to JSON
# ------------------------
def row_to_custom_json(table, row_id, id_column="id"):
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT row_to_json(t)
            FROM (
                SELECT * FROM {table} WHERE {id_column} = %s
            ) t
        """, (row_id,))        

        result = cur.fetchone()
        return result[0] if result else None

# ------------------------
# Function to get list of entities
# ------------------------
def get_workflow_entities():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM workflow_entity ORDER BY name")
        rows = cur.fetchall()
        return rows


def save_all_credentials():
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM credentials_entity")
        rows = cur.fetchall()
        for (cred_id,) in rows:
            json_data = row_to_custom_json("credentials_entity", cred_id)
            if json_data:
                filename = f"/workspace/n8n/demo-data/credentials/{cred_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                st.write(f"Saved credential: {filename}")

# ------------------------
# STREAMLIT APP
# ------------------------
st.title("Generate n8n Workflow JSON from PostgreSQL")

# Obtain entities
entities = get_workflow_entities()

if not entities:
    st.warning("No entities found.")
    st.stop()

# Map names to IDs
name_to_id = {name: entity_id for entity_id, name in entities}
selected_name = st.selectbox("Selecciona un workflow:", list(name_to_id.keys()))

if selected_name:
    selected_id = name_to_id[selected_name]

    if st.button("Convertir y Guardar JSON"):
        json_data = row_to_custom_json("workflow_entity", selected_id)

        save_all_credentials()

        if json_data:

            filename = f"/workspace/n8n/demo-data/workflows/{selected_id}.json"

            # save file to filesystem
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            st.success(f"📁 File saved at: `{filename}`")
        else:
            st.error("No register found.")
