from dotenv import load_dotenv
import os, boto3, pandas as pd
from datetime import datetime, timezone

load_dotenv()

aws_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
log_group = os.getenv("LOG_GROUP")

if not all([aws_key, aws_secret, log_group]):
    raise SystemExit("❌ Variables de entorno faltantes")

logs = boto3.client("logs",
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=region
)

streams = logs.describe_log_streams(
    logGroupName=log_group,
    orderBy="LastEventTime",
    descending=True,
    limit=1
)

if not streams.get("logStreams"):
    print("⚠️ No hay streams en el grupo")
    exit()

stream = streams["logStreams"][0]["logStreamName"]
events = logs.get_log_events(logGroupName=log_group, logStreamName=stream)

rows = [{"timestamp": datetime.fromtimestamp(e["timestamp"]/1000, tz=timezone.utc), "message": e["message"]} for e in events["events"]]

pd.DataFrame(rows).to_csv("logs_export.csv", index=False)
print("✅ Exportados", len(rows), "eventos")
