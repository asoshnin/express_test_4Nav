# **Product & Technical Specification: The Dynamic AI Navigator Profiler (MVP)**

**Project:** Dynamic AI Navigator Profiler **Version:** 1.3 (MVP) **Date:** August 6, 2025 **Owner:** Product & Engineering **Status:** Final, Ready for Development

### **1.0 Product Vision & Goals**

#### ***1.1 Vision Statement***

To create an intelligent, developmental assessment that empowers individuals and organizations to identify and cultivate the core traits of a successful AI Navigator, moving beyond static quizzes to provide deep, personalized insights through an **anonymous-first**, AI-powered experience.

#### ***1.2 Business Goals***

* **For Organizations:** Provide a scalable, scientifically-grounded tool to identify high-potential candidates for AI-centric roles, reducing hiring risk and improving talent strategy.  
* **For Individuals:** Offer a developmental, anonymous experience that provides actionable feedback, helping users understand their cognitive strengths with the option to download their results for personal use.  
* **For the Author:** Enable consented, non-automated follow-up contact with interested users to foster a community and gather qualitative feedback for future research.

#### ***1.3 Key Features (Epics)***

1. **Seamless & Anonymous Assessment Experience:** A fluid, engaging user journey that prioritizes anonymity with AI-generated nicknames.  
2. **Pre-Generated Question Assessment:** A robust backend that serves a fixed, psychometrically balanced set of questions for the MVP.  
3. **Personalized, Downloadable Reporting:** A rich, dynamically generated report that users can view once and download for their records.  
4. **Administrator Oversight:** A secure, simple interface for system administrators to view high-level results.

---

### **2.0 System Architecture (Cost-Optimized)**

The system is built on a **serverless-first** architecture to ensure near-zero fixed costs, with spending directly proportional to usage. For the MVP, the LLM is used only for nickname and final report generation.

**Architecture Diagram:**

```
[User's Browser] <--> [Azure Static Web Apps (React Frontend - Free Tier)]
      |
      | (HTTPS API Calls)
      v
[Azure Functions App (Python - Consumption Plan)] <-------------------------+
      |                                                                       |
      |--> [Azure Cosmos DB (Serverless Mode)] (Stores Session Data)           |
      |--> [Azure Blob Storage] (Stores Knowledge Base)                       |
      |--> [Azure OpenAI Service] (Tiered Models: GPT-3.5 & GPT-4)            |
      |--> [Azure Application Insights] (Logging & Monitoring)                |
      |                                                                       |
[Admin's Browser] <--> [Azure Static Web Apps (Admin UI - Free Tier)] --(Authenticated Call)-->+
```

#### ***2.1 Frontend***

* **Framework:** **React (Vite)** for a fast, modern single-page application (SPA).  
* **Hosting:** **Azure Static Web Apps (Free Tier)**. Both the main application and the admin UI will be deployed on the free tier, which includes SSL, global distribution, and CI/CD at no recurring cost.

#### ***2.2 Backend***

* **Platform:** **Azure Functions (Consumption Plan)**. This is a pure pay-per-execution model, meaning there is no cost when the application is idle.  
* **Language:** **Python 3.11+** is chosen for its robust AI and data handling libraries.  
* **Core Logic:** The backend's core logic for assessment is simplified for the MVP. It will fetch the next **pre-generated question pair** from the Knowledge Base in a fixed sequence for each user.

#### ***2.3 Data & AI Services***

* **Database:** **Azure Cosmos DB (Serverless Mode)**. This is a critical cost-saving choice. We are billed purely for the database operations and storage consumed, with **no minimum monthly fee**.  
* **Knowledge Base Storage:** **Azure Blob Storage**. Storing the knowledge base document will incur negligible costs.  
* **AI Service:** **Azure OpenAI Service (Pay-as-you-go)**. To control variable costs, we will use a **tiered-model strategy**:  
  * **Nickname Generation:** A faster, cheaper model (**GPT-3.5-Turbo**) will be used for this simple task.  
  * **Report Generation:** The more powerful **GPT-4** model will be reserved for generating the high-quality final report.

---

### **3.0 Data Models**

Data will be structured as JSON documents in a **Serverless** Azure Cosmos DB container.

#### ***3.1 `AssessmentSession` (Container: `sessions`)***

```json
{
  "id": "<session_guid>",
  "nickname": "Aqua-Badger-88",
  "contactEmail": "user@example.com",
  "status": "InProgress | Completed",
  "createdAt": "2025-08-06T12:00:00Z",
  "completedAt": "2025-08-06T12:15:00Z",
  "reportFirstViewedAt": null,
  "answers": [
    {
      "questionNumber": 1,
      "pairId": 1,
      "chosenStatementId": 103,
      "chosenConstruct": "Need for Cognition"
    }
  ],
  "result": {
    "primaryArchetype": "The Critical Interrogator",
    "secondaryArchetype": "The Curious Experimenter",
    "scores": {
      "archetypes": [
        { "name": "The Critical Interrogator", "score": 18.5, "percentile": 88 },
        { "name": "The Curious Experimenter", "score": 15.2, "percentile": 75 },
        { "name": "The Human-Centric Strategist", "score": 11.0, "percentile": 52 }
      ],
      "constructs": [
        { "name": "Need for Cognition", "score": 5, "percentile": 92 }
      ]
    },
    "reportNarrative": "Your profile shows a powerful blend of..."
  }
}
```

---

### **4.0 API Endpoints**

#### ***`POST /api/assessment`***

* **Action:** Initiates a new assessment, generates a unique nickname, and saves the new session.  
* **Response (201 Created):**

```json
{
  "sessionId": "<new_session_guid>",
  "nickname": "Crimson-Llama-42"
}
```

#### ***`GET /api/assessment/{sessionId}/question`***

* **Action:** Fetches the next question pair for the given session.  
* **Backend Logic:** The function identifies the current question number for the session and fetches the corresponding pre-generated pair from the definitive list in the Knowledge Base.  
* **Response (200 OK):**

```json
{
  "questionNumber": 1,
  "totalQuestions": 40,
  "statements": [
    { "id": "A", "text": "I like to analyze a problem from every angle..." },
    { "id": "B", "text": "I find it easy to connect with people..." }
  ]
}
```

#### ***`POST /api/assessment/{sessionId}/answer`***

* **Action:** Submits the user's choice for the current question.  
* **Request Body:**

```json
{
  "questionNumber": 1,
  "chosenStatementId": "A"
}
```

* **Response (204 No Content):** On successful submission.

#### ***`GET /api/assessment/{sessionId}/report`***

* **Action:** Retrieves the final report. This endpoint is designed to be called only once successfully.  
* **Backend Logic:** On the first successful call, the function sets the `reportFirstViewedAt` timestamp. On subsequent calls, it returns a `410 Gone` status.  
* **Response (200 OK):** The full `result` object from the `AssessmentSession` data model.  
* **Response (410 Gone):** If the report has already been viewed.

#### ***`GET /api/assessment/{sessionId}/report/download`***

* **Action:** Provides the user's report as a downloadable Markdown file.  
* **Response (200 OK):**  
  * **Headers:** `Content-Type: text/markdown`, `Content-Disposition: attachment; filename="navigator-report-Crimson-Llama-42.md"`  
  * **Body:** The full report content formatted in Markdown.

#### ***`POST /api/assessment/{sessionId}/contact`***

* **Action:** Allows a user to optionally submit their email after viewing their report.  
* **Request Body:**

```json
{
  "email": "user@example.com"
}
```

* **Response (204 No Content):** On successful submission.

#### ***`GET /api/admin/assessments`***

* **Action:** Retrieves a list of all completed assessments for the admin view.  
* **Security:** This endpoint will be secured directly within the Azure Functions App. Its authorization level will be set to `function`, requiring a secret **Function Key** to be included in the HTTP request header (`x-functions-key`).  
* **Response (200 OK):**

```json
{
  "assessments": [
    {
      "nickname": "Crimson-Llama-42",
      "completedAt": "2025-08-06T12:15:00Z",
      "primaryArchetype": "The Critical Interrogator",
      "archetypeScores": [ /* condensed scores */ ]
    }
  ]
}
```

---

### **5.0 User Stories & Acceptance Criteria**

#### ***Epic 1: Seamless & Anonymous Assessment Experience***

* **User Story 1.1:** As a candidate, I want to be assigned a unique and friendly nickname when I start the test, so I can identify my session easily and anonymously.  
  * **AC 1:** Given I am on the landing page, when I click "Start Assessment", then a new session is created and the API returns a `sessionId` and a `nickname`.  
  * **AC 2:** The nickname must be displayed prominently on the screen throughout the assessment.  
  * **AC 3:** The nickname generated must be composed of 2-3 neutral, non-offensive words and a number, and must not already exist in the database.  
* **User Story 1.2:** As a candidate, I want to answer a question by choosing one of two statements so that I can express my preferences.  
  * **AC 1:** Given I am on a question screen, when I click on a statement button, then my answer is submitted and I am automatically taken to the next question.  
  * **AC 2:** A progress bar updates to reflect the new question number (e.g., "2 of 40").

#### ***Epic 2: Pre-Generated Question Assessment***

* **User Story 2.1:** As the Product Owner, I want a definitive set of 40 pre-generated question pairs created and stored in the Knowledge Base, so that the assessment served to users is fair, balanced, and consistent for the MVP.  
  * **AC 1:** The final list must contain exactly 40 pairs, identified by `pair_id` from 1 to 40\.  
  * **AC 2:** Each pair must be created by matching two statements from the Item Bank that have a `social_desirability_score` delta of less than 1.5.  
  * **AC 3:** The set of 80 statements used across all 40 pairs must have a balanced representation of all 11 psychometric constructs.

#### ***Epic 3: Personalized, Downloadable Reporting***

* **User Story 3.1:** As a candidate, I want to see my final results immediately after completing the assessment, presented in a visually engaging way.  
  * **AC 1:** Given I have answered the 40th question, when I proceed, then I am shown a report screen.  
  * **AC 2:** The report screen must display my primary archetype clearly and include a visual representation (e.g., Radar Chart) of my scores.  
* **User Story 3.2:** As a candidate, I want to receive personalized feedback that explains what my results mean and how I can develop.  
  * **AC 1:** Given my report is generated, it must contain a dynamically generated narrative explaining my primary (and any strong secondary) archetypes.  
  * **AC 2:** The report must include sections on my "Signature Strengths" and "Potential Blind Spots" based on my archetype profile.  
* **User Story 3.3:** As a candidate, after viewing my results, I want to be able to download my full report as a Markdown file so that I can keep a personal copy.  
  * **AC 1:** Given I am on the report screen, when I click the "Download Report" button, then a `.md` file is downloaded to my device.  
  * **AC 2:** The filename of the downloaded report includes my unique nickname.  
* **User Story 3.4:** As a candidate, I want to be informed that my online report is viewable only once, so I know to save or download it.  
  * **AC 1:** The report screen must contain a clear, visible message stating that the web-based report can only be viewed once.  
  * **AC 2:** If I try to refresh or re-access the report URL after leaving the page, I am shown a message explaining that the report is no longer available.  
* **User Story 3.5:** As a candidate, after viewing my results, I want a clear and optional choice to provide my email address for potential, non-automated contact by the author.  
  * **AC 1:** The report screen contains an optional input field for an email address and a submit button.  
  * **AC 2:** Next to the input field, there must be clear text stating: "By providing your email, you consent to occasional, non-automated contact from the author regarding this profiler. Your email will not be shared."

#### ***Epic 4: Administrator Oversight***

* **User Story 4.1:** As the system administrator, I want to log in to a secure portal to view a list of all completed assessments.  
  * **AC 1:** Access to the admin portal requires authentication.  
  * **AC 2:** The portal displays a list of all assessments, with each entry showing the candidate's `nickname`, test `completionDate`, and their primary archetype and scores.

---

### **6.0 Deployment & Operations (DevOps)**

#### ***6.1 Infrastructure as Code (IaC)***

* All Azure resources (Static Web Apps, Function App, Cosmos DB, Storage, OpenAI Service) will be defined using **Bicep** templates. The templates will explicitly specify the `Serverless` capacity mode for Cosmos DB.

#### ***6.2 CI/CD Pipeline***

* A **GitHub Actions** workflow will be created to automate the build and deployment of the React frontend (to Azure Static Web Apps) and the Python backend (to Azure Functions).

#### ***6.3 Security & Configuration***

* **Endpoint Security:** The admin API (`/api/admin/assessments`) will be secured using a Function Key.  
* **Secrets Management:** All keys and connection strings (Cosmos DB, OpenAI, Function Key) will be stored in **Azure Key Vault** and accessed by the Function App via managed identity.

---

### **7.0 Future Enhancements (Roadmap)**

* **Implement Dynamic LLM Pairing:** For v2.0, replace the pre-generated pairs with the original dynamic, real-time matchmaking engine to increase variety and test security.  
* **Admin Dashboard Enhancements:** Add analytics, data visualization, and norm group management to the admin portal.  
* **Full RAG Implementation:** Transition from loading a single knowledge base file to indexing it in **Azure AI Search** for more sophisticated context retrieval.  
* **ATS/HRIS Integration:** Build integrations to connect the profiler with Applicant Tracking Systems.

