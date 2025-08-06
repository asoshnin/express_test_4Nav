# AI Navigator Profiler - Azure Functions Backend

This is the backend implementation for the AI Navigator Profiler, built using Azure Functions with Python.

## Project Structure

```
express_assessor_4Navigators/
├── DevDocs/                          # Core documentation
│   ├── Knowledge Base_ The Dynamic AI Navigator Profiler.md
│   ├── Product & Technical Specification_ The Dynamic AI Navigator Profiler.md
│   └── Project Setup Guide_ AI Navigator Profiler MVP.md
├── start_assessment/                 # Start Assessment API
│   ├── function.json                # Function configuration
│   └── __init__.py                  # Function implementation
├── function_app.py                   # Main function app entry point
├── host.json                        # Host configuration
├── requirements.txt                  # Python dependencies
└── local.settings.json              # Local development settings
```

## API Endpoints

### POST /api/assessment
Creates a new assessment session with a unique nickname.

**Request:** No body required

**Response (201 Created):**
```json
{
  "sessionId": "uuid-string",
  "nickname": "Crimson-Llama-42"
}
```

## Setup Requirements

### Environment Variables
The following environment variables must be configured:

- `COSMOS_ENDPOINT`: Azure Cosmos DB endpoint URL
- `COSMOS_KEY`: Azure Cosmos DB access key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI service endpoint
- `AZURE_OPENAI_KEY`: Azure OpenAI API key

### Azure Resources Required

1. **Azure Cosmos DB (Serverless Mode)**
   - Database: `navigator_profiler`
   - Container: `sessions`
   - Partition Key: `/id`

2. **Azure OpenAI Service**
   - Model: `gpt-35-turbo` (for nickname generation)

3. **Azure Functions App**
   - Runtime: Python 3.11+
   - Plan: Consumption

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables in `local.settings.json`:
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "FUNCTIONS_WORKER_RUNTIME": "python",
       "AzureWebJobsStorage": "UseDevelopmentStorage=true",
       "COSMOS_ENDPOINT": "your-cosmos-endpoint",
       "COSMOS_KEY": "your-cosmos-key",
       "AZURE_OPENAI_ENDPOINT": "your-openai-endpoint",
       "AZURE_OPENAI_KEY": "your-openai-key"
     }
   }
   ```

3. Run the function app:
   ```bash
   func start
   ```

## Testing

The function can be tested using curl or any HTTP client:

```bash
curl -X POST http://localhost:7071/api/assessment
```

Expected response:
```json
{
  "sessionId": "12345678-1234-1234-1234-123456789abc",
  "nickname": "Crimson-Llama-42"
}
```

## Implementation Details

### Nickname Generation
- Uses Azure OpenAI GPT-3.5-turbo model
- Format: `[Color]-[Animal]-[Number]` (e.g., "Crimson-Llama-42")
- Validates uniqueness against existing sessions in Cosmos DB
- Retries up to 10 times if duplicates are found

### Session Document Schema
```json
{
  "id": "session-uuid",
  "nickname": "Crimson-Llama-42",
  "contactEmail": null,
  "status": "InProgress",
  "createdAt": "2025-08-06T12:00:00Z",
  "completedAt": null,
  "reportFirstViewedAt": null,
  "answers": [],
  "result": null
}
```

## Error Handling

- Returns 201 Created on successful session creation
- Returns 500 Internal Server Error for any exceptions
- Logs all errors for debugging
- Validates nickname format before saving
- Handles Azure service connection failures gracefully 