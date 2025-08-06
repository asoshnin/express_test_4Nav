# AI Navigator Profiler Backend

A production-ready Azure Functions backend for the AI Navigator Profiler, a psychometric assessment tool that identifies user archetypes for AI navigation work.

## 🚀 Complete API Implementation

### Core Assessment Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/assessment` | POST | Start new assessment with unique nickname | ✅ Working |
| `/api/assessment/{sessionId}/question` | GET | Get next question pair | ✅ Working |
| `/api/assessment/{sessionId}/answer` | POST | Submit answer and track progress | ✅ Working |
| `/api/assessment/{sessionId}/report` | GET | Generate personalized AI report | ✅ Working |

### User Experience Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/assessment/{sessionId}/status` | GET | Get session progress and status | ✅ Working |
| `/api/assessment/{sessionId}/report/download` | GET | Download Markdown report | ✅ Working |
| `/api/assessment/{sessionId}/contact` | POST | Submit contact information | ✅ Working |

### Administrative Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/admin/assessments` | GET | Admin dashboard for all sessions | ✅ Working |
| `/api/analytics` | GET | System metrics and usage statistics | ✅ Working |
| `/api/health` | GET | Health check for monitoring | ✅ Working |
| `/api/admin/sessions/cleanup` | DELETE | Clean up old sessions (admin) | ✅ Working |
| `/api/admin/sessions/{sessionId}/reset` | POST | Reset session for testing | ✅ Working |

## 🏗️ Architecture

- **Azure Functions v4** with Python 3.11+
- **Azure Cosmos DB** for session storage
- **Azure OpenAI Service** for AI-powered features
  - GPT-3.5-turbo for nickname generation
  - GPT-4 for report generation
- **Production-ready** with comprehensive error handling

## 📊 Features

### Assessment Engine
- 40 pre-generated question pairs from psychometric framework
- 11 core constructs measured across 3 archetypes
- Real-time progress tracking and session management
- Comprehensive analytics and reporting

### Admin Management
- Session cleanup for old/abandoned sessions
- Session reset for development/testing
- Detailed analytics with period-based filtering
- Admin dashboard with pagination and filtering
- Real-time progress tracking and validation
- Unique nickname generation with collision detection

### Analytics & Monitoring
- Session completion rates and performance metrics
- Archetype distribution analysis
- Daily activity tracking
- Report generation and viewing statistics
- Period-based filtering (24h, 7d, 30d, all)

### User Experience
- Session status and progress tracking
- Downloadable Markdown reports
- Contact form integration
- Health monitoring for production

## 🎯 Psychometric Framework

The assessment measures 11 core constructs across 3 primary archetypes:

### Archetypes
1. **The Critical Interrogator** - Analytical thinking and systematic problem-solving
2. **The Human-Centric Strategist** - Emotional intelligence and ethical decision-making  
3. **The Curious Experimenter** - Adaptability and hands-on learning

### Constructs
- Analytical Thinking
- Systematic Problem-Solving
- Evidence-Based Decision Making
- Emotional Intelligence
- Ethical Reasoning
- Collaborative Leadership
- Adaptability
- Experimental Mindset
- Risk Tolerance
- Innovation Orientation
- Learning Agility

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/asoshnin/express_test_4Nav.git
   cd express_test_4Nav
   ```

2. **Set up environment variables** in `local.settings.json`
   ```json
   {
     "IsEncrypted": false,
     "Values": {
       "COSMOS_ENDPOINT": "your-cosmos-endpoint",
       "COSMOS_KEY": "your-cosmos-key",
       "AZURE_OPENAI_ENDPOINT": "your-openai-endpoint",
       "AZURE_OPENAI_KEY": "your-openai-key"
     }
   }
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the function app**
   ```bash
   func start
   ```

## 📝 API Documentation

### Start Assessment
```bash
curl -X POST "http://localhost:7071/api/assessment"
```
**Response:**
```json
{
  "sessionId": "uuid",
  "nickname": "Aqua-Badger-88"
}
```

### Get Question
```bash
curl -X GET "http://localhost:7071/api/assessment/{sessionId}/question"
```
**Response:**
```json
{
  "questionNumber": 1,
  "totalQuestions": 40,
  "statements": {
    "A": {"id": "A", "text": "Statement A"},
    "B": {"id": "B", "text": "Statement B"}
  }
}
```

### Submit Answer
```bash
curl -X POST "http://localhost:7071/api/assessment/{sessionId}/answer" \
  -H "Content-Type: application/json" \
  -d '{"questionNumber": 1, "chosenStatementId": "A"}'
```

### Generate Report
```bash
curl -X GET "http://localhost:7071/api/assessment/{sessionId}/report"
```

### Session Status
```bash
curl -X GET "http://localhost:7071/api/assessment/{sessionId}/status"
```

### Analytics
```bash
curl -X GET "http://localhost:7071/api/analytics?period=7d"
```

## 🔧 Development

### Project Structure
```
express_assessor_4Navigators/
├── start_assessment/          # Assessment initiation
├── get_question/             # Question serving
├── submit_answer/            # Answer processing
├── generate_report/          # AI report generation
├── download_report/          # Report download
├── session_status/           # Progress tracking
├── contact/                  # Contact form
├── admin/                    # Admin dashboard
├── analytics/                # System metrics
├── health/                   # Health monitoring
├── function_app.py           # Main function registration
├── requirements.txt          # Dependencies
└── local.settings.json       # Environment variables
```

### Testing
- All endpoints tested and working
- Comprehensive error handling
- Production-ready status codes
- Session validation and security

## 📈 Production Ready

✅ **Complete API Implementation** - All 10 endpoints working  
✅ **Azure Integration** - Cosmos DB and OpenAI connected  
✅ **Error Handling** - Comprehensive validation and error responses  
✅ **Monitoring** - Health checks and analytics  
✅ **Documentation** - Complete API documentation  
✅ **Testing** - All endpoints tested and validated  

## 🎉 Status: PRODUCTION READY

The AI Navigator Profiler backend is now complete and ready for:
- Frontend integration
- Production deployment
- User testing
- Scaling and monitoring

**Repository:** https://github.com/asoshnin/express_test_4Nav.git 