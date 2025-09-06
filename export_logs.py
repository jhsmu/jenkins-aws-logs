import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone
import re

# 🔹 Cargar .env si existe (para pruebas locales)
if os.path.exists(".env"):
    load_dotenv()

# 🔹 Variables de entorno
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
LOG_GROUP = os.getenv("LOG_GROUP")

# 🔹 Validación
if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, LOG_GROUP]):
    raise SystemExit("❌ Falta alguna variable obligatoria: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, LOG_GROUP")

# 🔹 Cliente CloudWatch Logs
logs = boto3.client(
    "logs",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 🔹 Obtener stream más reciente
streams = logs.describe_log_streams(
    logGroupName=LOG_GROUP,
    orderBy="LastEventTime",
    descending=True,
    limit=1
)

if not streams.get("logStreams"):
    print("⚠️ No se encontraron streams en el Log Group")
    exit()

latest_stream = streams["logStreams"][0]["logStreamName"]
print(f"📌 Último stream: {latest_stream}")

# 🔹 Descargar logs
events = []
next_token = None

while True:
    params = {
        "logGroupName": LOG_GROUP,
        "logStreamName": latest_stream,
        "limit": 100
    }
    if next_token:
        params["nextToken"] = next_token

    response = logs.get_log_events(**params)

    for event in response.get("events", []):
        events.append({
            "timestamp": datetime.fromtimestamp(event["timestamp"]/1000, tz=timezone.utc),
            "message": event["message"]
        })

    next_token = response.get("nextForwardToken")
    if not next_token or next_token == params.get("nextToken"):
        break

# 🔹 Exportar todos los logs a CSV
df = pd.DataFrame(events)
df.to_csv("logs_export.csv", index=False)
print(f"✅ Exportados {len(events)} logs a logs_export.csv")

# 🔹 Detectar errores y problemas
error_keywords = ["error", "failed", "exception", "no se pudo", "fallida", "denegado"]
problematic_logs = []

fintech_pattern = re.compile(r"fintechId[: ]*([a-z0-9\-]+)", re.IGNORECASE)

for e in events:
    msg_lower = e["message"].lower()
    if any(k in msg_lower for k in error_keywords):
        fintech_match = fintech_pattern.search(e["message"])
        fintech_id = fintech_match.group(1) if fintech_match else "N/A"
        problematic_logs.append({
            "timestamp": e["timestamp"],
            "fintechId": fintech_id,
            "message": e["message"]
        })

# 🔹 Resumen de problemas
if problematic_logs:
    df_errors = pd.DataFrame(problematic_logs)
    df_errors.to_csv("logs_problems_summary.csv", index=False)
    print(f"⚠️ Se encontraron {len(problematic_logs)} logs problemáticos. Resumen exportado a logs_problems_summary.csv")
    print(df_errors.head(10).to_string(index=False))
else:
    print("✅ No se detectaron errores o problemas en los logs")
