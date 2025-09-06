import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone

# Cargar variables de entorno
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = 'us-east-1'
LOG_GROUP = 'LeancoreInfraStackProd-LeancorePortfolioReporterTaskleancoreportfolioreporterLogGroupD62FBEF1-V5zAjptjzyox'

# Cliente de CloudWatch Logs
print("Cliente de Cloudwath")
logs = boto3.client(
    "logs",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# 👉 Obtener el stream más reciente
print("Obteniendo stream mas recientes")
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

# Obtener logs de ese stream
print("Obteniendo Logs")
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

# Exportar a CSV
print("Exportando CSV")
df = pd.DataFrame(events)
df.to_csv("logs_export.csv", index=False)

print(f"✅ Exportados {len(events)} logs del stream más reciente a logs_export.csv")

