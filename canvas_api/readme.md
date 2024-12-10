# DAP Access Guide

This guide provides step-by-step instructions to access and utilize the **DAP API**.

---

## Requirements

You need to have installed the Canvas API, if you do not have it you can get it like this:
```powershell
pip3 install "instructure-dap-client[postgresql]"
```


## 1. Setting Environment Variables

Before you can interact with the DAP API, you need to set up the necessary environment variables. Follow these steps:

### For Windows PowerShell

Run the following commands:

```powershell
$env:DAP_API_URL = "https://api-gateway.instructure.com"
$env:DAP_CLIENT_ID = "us-east-1#9ef4d927-0457-4156-9f37-713734dfe506"
$env:DAP_CLIENT_SECRET = "aXI4mOFDx0v-RFw6iHemq79ioCfMUcnJ7VtFF2aBPuw"
```

### Verifying Environment Variables

To confirm the variables were loaded correctly, use the following commands:

```powershell
echo $env:DAP_API_URL
echo $env:DAP_CLIENT_ID
echo $env:DAP_CLIENT_SECRET
```

> **Warning:** These environment variables must be set each time you create a new PowerShell session. To make this process persistent, consider adding these variables to your system environment settings.

---

## 2. Using Namespaces with DAP

DAP commands require specifying the appropriate namespace. Use the following format:

```bash
dap list --namespace canvas
```

This command will list the available datasets within the `canvas` namespace.

---

## 3. Loading Data from Specific Tables

To retrieve data from a specific table, use the `dap snapshot` command. Here is the general syntax:

```bash
dap snapshot --namespace canvas --table <table_name> --output-dir <path_to_download>
```

### Example

To download data from the `submissions` table:

```bash
dap snapshot --namespace canvas --table submissions --output-dir "C:\Users\diego\Downloads\"
```

This command will:

- Download multiple zip files containing the data.
- Save the files in the specified directory (`C:\Users\diego\Downloads\`).

> **Tip:** Ensure the output directory exists before running the command to avoid errors.

---

### Troubleshooting

- **Missing Environment Variables:** Double-check that the variables are set correctly by echoing them in your terminal.
- **Namespace or Table Not Found:** Ensure the namespace and table name are spelled correctly.
- **Access Errors:** Verify your client ID and secret are valid and that your API URL is correct.

For additional information or support, refer to the official DAP documentation or contact your system administrator.