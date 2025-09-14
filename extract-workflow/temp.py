import psycopg2
import json
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

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


if __name__ == "__main__":
    table_name = "workflow_entity"
    row_id = "zmKa4DIERHOzVXqn"  # 👈 string porque es character varying
    output = row_to_custom_json(table_name, row_id)

    if output:
        filename = f"{row_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"✅ Fila guardada en {filename}")
    else:
        print("Fila no encontrada")
