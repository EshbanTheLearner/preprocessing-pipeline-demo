from chalice import Chalice
import boto3

app = Chalice(app_name='pipeline-trigger')

client = boto3.client("datapipeline")

# The pipeline you want to activate
PIPELINE_ID = "df-xxxxxxxxxxxxxxxxxxxx"

@app.on_s3_event(bucket='automated-data-pipeline', events=['s3:ObjectCreated:*'], prefix="preprocess/", suffix=".csv")
def activate_pipeline(event):
    app.log.debug(f"Received event for bucket: {event.bucket}, key: {event.key}")
    try:
        response = client.activate_pipeline(
            pipelineId=PIPELINE_ID,
            parameterValues=[
                {
                    "id": "myS3DataPath",
                    "stringValue": f"s3://{event.bucket}/{event.key}"
                }
            ]
        )
        app.log.debug(response)
    except Exception as e:
        app.log.critical(e)