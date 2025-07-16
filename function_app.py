import logging
import os
from datetime import datetime

import azure.functions as func
import azure.durable_functions as df
from azure.storage.blob import BlobServiceClient
from PIL import Image
import io
import pymssql

# Durable Function app instance
my_app = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Blob Storage client setup
blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AzureWebJobsStorage"))

# Blob trigger with corrected path pattern
@my_app.blob_trigger(arg_name="myblob", path="images-input/{name}", connection="AzureWebJobsStorage")
@my_app.durable_client_input(client_name="client")
async def blob_trigger(myblob: func.InputStream, client):
    logging.info(f"Blob trigger processed blob: Name={myblob.name}, Size={myblob.length} bytes")
    blobName = myblob.name.split("/")[-1]
    await client.start_new("orchestrator", client_input=blobName)

# Orchestration function
@my_app.orchestration_trigger(context_name="context")
def orchestrator(context: df.DurableOrchestrationContext):
    blobName = context.get_input()

    retry_options = df.RetryOptions(first_retry_interval_in_milliseconds=5000, max_number_of_attempts=3)

    metadata = yield context.call_activity_with_retry("extract_metadata", retry_options, blobName)
    yield context.call_activity_with_retry("store_metadata", retry_options, metadata)

    return f"Metadata processed and stored for {blobName}"

# Activity function to extract metadata from image
@my_app.activity_trigger(input_name='blobName')
def extract_metadata(blobName):
    logging.info(f"Extracting metadata for {blobName}")
    container_client = blob_service_client.get_container_client("images-input")
    blob_client = container_client.get_blob_client(blobName)
    blob_bytes = blob_client.download_blob().readall()

    with Image.open(io.BytesIO(blob_bytes)) as img:
        metadata = {
            "FileName": blobName,
            "FileSizeKB": round(len(blob_bytes) / 1024, 2),
            "Width": img.width,
            "Height": img.height,
            "Format": img.format
        }
    logging.info(f"Extracted metadata: {metadata}")
    return metadata

# Activity function to store metadata in SQL Server
@my_app.activity_trigger(input_name='metadata')
def store_metadata(metadata):
    logging.info(f"Storing metadata in SQL DB: {metadata}")

    try:
        conn = pymssql.connect(
            server='cst8917sql134.database.windows.net',
            user='sqladminuser',
            password='StrongP@ssword123!',
            database='cst8917db',
            port=1433
        )
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO ImageMetadata (FileName, FileSizeKB, Width, Height, Format)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            metadata["FileName"],
            metadata["FileSizeKB"],
            metadata["Width"],
            metadata["Height"],
            metadata["Format"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Metadata stored successfully with pymssql.")
    except Exception as e:
        logging.error(f"Failed to store metadata with pymssql: {e}", exc_info=True)
        raise

    return "Metadata stored successfully."
