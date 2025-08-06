# **Project Setup Guide: AI Navigator Profiler MVP**

This guide will walk you through creating the local project structure, setting up a Python virtual environment, initializing an Azure Functions project, and preparing the initial prompt for your AI coding assistant, Cursor.ai.

#### ***Prerequisites***

Before you begin, ensure you have the following installed on your Windows machine:

1. **Python** (version 3.9 or higher).  
2. **Visual Studio Code** and/or the **Cursor.ai** application.  
3. **Azure Functions Core Tools** (`npm install -g azure-functions-core-tools@4`).  
4. **Git** for version control.  
5. An **Azure subscription** (you'll need this for deployment later, not for the initial setup).

---

### **Phase 1: Local Environment Setup**

**Step 1: Open Your Terminal**

* Open a modern terminal like **Windows Terminal** or PowerShell. Avoid the old Command Prompt if possible.

**Step 2: Create Project Directories**

* Run the following commands to create the main project folder and the `DevDocs` subfolder, then navigate into the project directory.

```
# Navigate to your playground directory
cd D:\Users\asosh\playground\azure-func

# Create the main project folder and the DevDocs subfolder
mkdir express_assessor_4Navigators
cd express_assessor_4Navigators
mkdir DevDocs
```

**Step 3: Populate the `DevDocs` Folder**

* Manually save the two documents we finalized into the `DevDocs` folder:  
    
  1. `Knowledge Base The Dynamic AI Navigator Profiler (MVP).md`  
  2. `Product & Technical Specification The Dynamic AI Navigator Profiler (MVP).md`


  *This is the most critical step for enabling Cursor to understand our project's context.*

**Step 4: Create and Activate Python Virtual Environment**

* A virtual environment keeps your project's dependencies isolated. From inside the `express_assessor_4Navigators` folder, run:

```
# Create the virtual environment in a folder named .venv
python -m venv .venv

# Activate the virtual environment
.\.venv\Scripts\activate
```

* You will know it's active when you see `(.venv)` at the beginning of your command prompt line.

---

### **Phase 2: Project Initialization**

**Step 5: Initialize the Azure Functions Project**

* While the virtual environment is active, initialize the folder as a Python-based Azure Functions project.

```
# Initialize the current folder (.) as a Python function app
func init . --python
```

* This command creates essential files like `host.json`, `local.settings.json`, and `requirements.txt`.

**Step 6: Create a `.gitignore` File**

* It's a best practice to prevent committing unnecessary files to your GitHub repository. Create a file named `.gitignore` in the root of your project folder (`express_assessor_4Navigators`) and add the following content:

```
# Python
__pycache__/
*.py[cod]
*$py.class

# Environment
.venv/
.env

# Azure Functions
local.settings.json
.funcignore

# IDE
.vscode/
```

**Step 7: Initial Git Setup (Recommended)**

* Initialize your local repository and make your first commit.

```
git init
git add .
git commit -m "Initial project setup with environment and spec docs"
```

* You can later link this to your `asoshnin` GitHub account by creating a new repository on GitHub and following the instructions to push an existing repository.

---

### **Phase 3: AI-Assisted Development with Cursor.ai**

**Step 8: Open the Project in Cursor**

* From your terminal (still in the project root directory), type:

```
cursor .
```

* This will open the entire project folder in Cursor. Make sure the files in `DevDocs` are visible in the file explorer.

**Step 9: Your Initial Prompt for Cursor.ai**

* Open a new chat with Cursor (`Ctrl+L` or by clicking the chat icon) and provide it with the following comprehensive prompt. This prompt gives it the context and the first actionable task.

---

#### ***(Copy and paste the following into the Cursor chat)***

Hello Cursor. You are my expert AI coding assistant. We are about to start building a new web application called the **AI Navigator Profiler**.

**\#\# My Goal** My goal is to build the backend for this application using Python on Azure Functions, following a specific set of requirements.

**\#\# Core Documentation (Your 'Single Source of Truth')** Before we write any code, please familiarize yourself with the two documents located in the `DevDocs` folder:

1. **`Knowledge Base... (MVP).md`**: This contains the project's core philosophy, the psychometric framework, the pre-generated question pairs, and the final prompt for the report-generation AI.  
2. **`Product & Technical Specification... (MVP).md`**: This contains the user stories, a detailed data model for our Cosmos DB `AssessmentSession`, and the full API specification.

These documents are our complete blueprint. Please reference them for all subsequent tasks.

**\#\# Our First Task: Create the 'Start Assessment' API** Let's start by building the first API endpoint as defined in the technical specification: `POST /api/assessment`.

Please create a new Azure Function for me named `start_assessment`. This function must accomplish the following, based on our spec documents:

* It must be an **HTTP Trigger** that responds to `POST` requests on the route `/api/assessment`.  
* It needs to generate a unique, human-readable nickname (e.g., "Aqua-Badger-88"). For this, it should make a call to the **Azure OpenAI Service** using a light and fast model like `gpt-3.5-turbo`.  
* **Crucially**, it must check for nickname uniqueness by querying our **Azure Cosmos DB** database to ensure the generated name doesn't already exist. It should loop until a unique name is found.  
* It must create a new session document in the `sessions` container in Cosmos DB. The document schema should match the `AssessmentSession` data model in the technical spec (including fields like `id`, `nickname`, `status: "InProgress"`, and `createdAt`).  
* Finally, it must return a `201 Created` JSON response containing the new `sessionId` and the unique `nickname`.

Please generate the necessary files (`function.json` and `__init__.py`) inside a new folder named `start_assessment`.  
