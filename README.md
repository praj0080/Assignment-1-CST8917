<!-- 

Repo:
https://github.com/degu0055/25S_CST8917_Assignment_1

Query: 
https://portal.azure.com/#@AlgonquinLivecom.onmicrosoft.com/resource/subscriptions/cdb9bdf3-e7ee-43e9-8f6c-ba7327868df1/resourceGroups/CST8917-rg/providers/Microsoft.Sql/servers/cst8917sql134/databases/cst8917db/connectionStrings
SELECT * FROM ImageMetadata;
TRUNCATE TABLE ImageMetadata;



Container:
https://portal.azure.com/#view/Microsoft_Azure_Storage/ContainerMenuBlade/~/overview/storageAccountId/%2Fsubscriptions%2Fcdb9bdf3-e7ee-43e9-8f6c-ba7327868df1%2FresourceGroups%2FCST8917-rg%2Fproviders%2FMicrosoft.Storage%2FstorageAccounts%2Fcst8917storagexxx/path/images-input/etag/%220x8DDBF8945DA7D4D%22/defaultId//publicAccessVal/None

ChatGPT:
https://chatgpt.com/c/686f7383-b690-8001-b753-8d933822e2b6


user:
sqladminuser

Password:
StrongP@ssword123!

-->

# CST8917 Assignment 1: Durable Workflow for Image Metadata Processing

## Summary

This project implements a **serverless image metadata processing pipeline** using **Azure Durable Functions (Python)**.

- When a new image (.jpg, .png, or .gif) is uploaded to the Azure Blob Storage container `images-input`, a **blob-triggered Durable Function** starts.
- The **orchestrator function** calls two activity functions:
  - `extract_metadata`: extracts file name, size (KB), width, height, and format from the image.
  - `store_metadata`: saves this metadata into an Azure SQL Database.
- The pipeline is deployed on Azure, fully automated, and tested.

## Source Code

See `function_app.py` in the repo for full source code with documentation.

## Local Settings

Use `local.settings.json` with your Azure Storage and SQL connection strings configured.

## Azure CLI Commands Used

- Create Resource Group:
  ```bash
  az group create --name cst8917-rg --location canadacentral
  ```

- Create Storage Account:
  ```bash
  az storage account create --name cst8917storagexxx --resource-group cst8917-rg --location canadacentral --sku Standard_LRS
  ```

- Create Blob Container:
  ```bash
  az storage container create --name images-input --account-name cst8917storagexxx
  ```

- Create Azure SQL Server:
  ```bash
  az sql server create --name cst8917sql134 --resource-group cst8917-rg --location canadacentral --admin-user sqladminuser --admin-password StrongP@ssword123!
  ```

- Create SQL Database:
  ```bash
  az sql db create --resource-group cst8917-rg --server cst8917sql134 --name cst8917db --service-objective S0
  ```

- Configure firewall to allow Azure services:
  ```bash
  az sql server firewall-rule create --resource-group cst8917-rg --server cst8917sql134 --name AllowAzureIPs --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0
  ```

## How to Use

1. Upload images (`.jpg`, `.png`, `.gif`) to the `images-input` container.
2. The Durable Function pipeline will automatically trigger.
3. Metadata will be extracted and saved to the Azure SQL Database table `ImageMetadata`.
4. Verify data in the database.
5. Record a demo video (max 5 minutes) showing the process.


