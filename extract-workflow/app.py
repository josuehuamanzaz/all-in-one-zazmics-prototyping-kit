import streamlit as st
import psycopg2
import json
import os
from dotenv import load_dotenv
from io import BytesIO

# Cargar variables del entorno (.env)
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Conexión única (puedes manejarla con cache si quieres)
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# ------------------------
# Función que convierte una fila a JSON
# ------------------------
def row_to_custom_json(table, row_id, id_column="id"):
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table} WHERE {id_column} = %s", (row_id,))
        row = cur.fetchone()
        if not row:
            return None

        colnames = [desc[0] for desc in cur.description]
        result = {}

        for col, val in zip(colnames, row):
            if val is None:
                result[col] = None
            elif isinstance(val, bool):
                result[col] = val
            elif isinstance(val, (int, float)):
                result[col] = val
            elif isinstance(val, dict):
                result[col] = val
            elif isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    result[col] = parsed
                except Exception:
                    result[col] = val
            else:
                result[col] = str(val)

        return result

# ------------------------
# Función para obtener lista de entidades
# ------------------------
def get_workflow_entities():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM workflow_entity ORDER BY name")
        rows = cur.fetchall()
        return rows

# ------------------------
# STREAMLIT APP
# ------------------------
st.title("Exportador de Workflow Entity a JSON")

# Obtener entidades
entities = get_workflow_entities()

if not entities:
    st.warning("No se encontraron entidades.")
    st.stop()

# Crear diccionario para selección
name_to_id = {name: entity_id for entity_id, name in entities}
selected_name = st.selectbox("Selecciona un workflow:", list(name_to_id.keys()))

if selected_name:
    selected_id = name_to_id[selected_name]

    if st.button("Convertir y Descargar JSON"):
        json_data = row_to_custom_json("workflow_entity", selected_id)

        if json_data:
            # Mostrar en Streamlit
            st.success("✅ JSON generado correctamente")
            st.json(json_data)

            # Guardar en BytesIO para descarga
            json_bytes = BytesIO()
            json.dump(json_data, json_bytes, indent=2, ensure_ascii=False)
            json_bytes.seek(0)

            filename = f"{selected_id}.json"

            # Botón para descargar
            st.download_button(
                label="📥 Descargar JSON",
                data=json_bytes,
                file_name=filename,
                mime="application/json"
            )
        else:
            st.error("No se encontró el registro.")
