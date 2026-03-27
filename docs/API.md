# AILA API Documentation (v1)

The Scholarly AI Workspace (AILA) exposes a REST API built with FastAPI and hosted as Serverless Functions on Vercel.

## Core Endpoints

### Health Check
- **GET** `/api/v1/health`
- **Response**: `{"status": "ok"}`
- **Purpose**: Verify backend availability.

### Scholarly Progress
- **GET** `/api/v1/progress`
- **Response**: Current weighted intelligence stats.
- **Purpose**: Provide real-time learning analytics.

### Intelligence Insights (AI Mentor)
- **GET** `/api/v1/insights`
- **Response**: Context-aware tips from the AI Mentor.
- **Purpose**: Provide dynamic study advice based on recent performance.

### Learning Library
- **GET** `/api/v1/library`
- **Response**: Searchable list of all previous sessions and summaries.
- **Purpose**: Persistent storage of scholarly activity.

### AI Tutor (Learning)
- **POST** `/api/v1/learn`
- **Payload**: `{"text": "topic name"}`
- **Response**: Detailed AI explanation and summary.
- **Purpose**: Core learning engine.

### Learning Quiz
- **POST** `/api/v1/quiz`
- **Payload**: `{"topic": "topic name"}`
- **Response**: Structured quiz data.
- **Purpose**: Knowledge validation.
