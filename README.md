# CST8917 Assignment 1 – Durable Workflow for Image Metadata Processing

## 🔍 Overview

This project shows a **serverless image metadata process pipeline** with **Azure Durable Functions in Python**. The app has the functionality to automatically derive metadata out of the uploaded images in the Azure Blob Storage and save them in **Azure SQL Database**.

> 💡 **Use Case**: A content moderation team would also like to log metadata of images uploaded by the users in order to keep track of their formats and sizes.

---

## 🧠 Features

- ✅ Blob Trigger: Processing initiated by uploading of image automatically.
- ✅ Orchestration: Employs Durable Functions in an attempt to regulate the extraction and storage of metadata.
- ✅ Activity Functions:
  - Extract image metadata from image files with Pillow.
  - Stores metadata in Azure SQL Database.
- ✅ Azure End-to-End Deployment.

---

## 🧱 Architecture

```text
           +------------------+
           |  Azure Blob      |
           |  Storage (Input) |
           +--------+---------+
                    |
                    v
       [Blob Trigger Function]
                    |
                    v
       [Durable Orchestrator]
            |           |
     [Extract]       [Store]
     [Metadata]     [Metadata]
            |           |
            +-----------+
                    |
                    v
         [Azure SQL Database]
```

---

## 🛠️ Technologies Used

- Python 3.9
- Azure Functions (Durable)
- Azure Blob Storage
- Azure SQL Database
- Pillow (PIL)
- pymssql (SQL driver)

---

## 🚀 Setup Instructions (Local)

### 1. Clone the Repository

```bash
git clone https://github.com/praj0080/Assignment-1-CST8917.git
cd Assignment-1-CST8917
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add Connection Settings

Create a `local.settings.json` file:

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=cst8917storage123;AccountKey=EAbAqRqn5r46430WkuflToWyYLeKmEP0koLBE8w+iF+wLrZTe0AnxeeDiQe1jd6pJ2LYkLyEb4xg+AStwpuSUw==;EndpointSuffix=core.windows.net",
    "SQL_CONNECTION_STRING": "Server=tcp:cst8917sql134.database.windows.net,1433;Initial Catalog=cst8917db;Persist Security Info=False;User ID=sqladminuser;Password=StrongP@ssword123!;MultipleActiveResultSets=False;Encrypt=true;TrustServerCertificate=False;Connection Timeout=30;"
  }
}
```

### 4. Start the Function App

```bash
func start
```

---

## 🧪 Image Metadata Captured

- **FileName**: Original blob name
- **FileSizeKB**: Size in kilobytes
- **Width**: Image width in pixels
- **Height**: Image height in pixels
- **Format**: Image format (JPEG, PNG, etc.)

---

## 📦 Deployment to Azure

1. Create the following resources:
   - Azure Storage Account
   - Azure SQL Database
   - Azure Function App (Linux, Python 3.9)

2. Deploy using Azure CLI:

```bash
func azure functionapp publish image-metadata-func
```

3. Upload test images (`.jpg`, `.png`, `.gif`) to your Blob container (e.g., `images-input`).

4. Use Azure Data Studio to check that stored metadata in SQL.

---

## 🎥 YouTube Demo

🔗 [Watch the Demo Video](https://youtu.be/your-demo-link-here)

---

## 📁 Project Structure

```bash
Assignment-1-CST8917/
│
├── function_app.py           # Durable workflow with orchestrator and activities
├── requirements.txt          # Dependencies
├── host.json                 # Azure Functions host configuration
├── local.settings.json       # Local environment config (excluded in GitHub)
└── README.md                 # You're here!
```

---
