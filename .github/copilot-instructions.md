# Copilot Instructions for PoliHacks

## Project Overview
PoliHacks is a multi-component project with a React/Vite frontend (`interviewer/`) and a Python backend (`backend/`). The backend includes machine learning models and OpenCV libraries, while the frontend is a single-page React app.

## Architecture & Key Directories
- **interviewer/**: React app using Vite. Entry: `src/main.jsx`. Main UI logic in `src/components/` and `src/pages/`.
- **backend/**: Python service. Main files: `app.py`, `app_mock.py`. ML models in `physiology/graph/models/`. OpenCV libs in `opencv_libs/`.
- **Integration**: Frontend communicates with backend via HTTP (see backend `curl` and Docker setup).

## Developer Workflows
- **Frontend**:
  - Start dev server: `npm run dev` in `interviewer/`
  - Build: `npm run build`
  - Lint: `npm run lint`
  - Entry: `src/main.jsx`, main page: `src/pages/HomePage.jsx`, camera logic: `src/components/CameraPanel.jsx`
- **Backend**:
  - Run: `python app.py` or use Docker (`docker-compose up` in `backend/`)
  - Requirements: `requirements.txt` in `backend/`
  - Models: TensorFlow Lite files in `physiology/graph/models/`
  - OpenCV: Custom libs in `opencv_libs/` (Linux .so files)

## Patterns & Conventions
- **Frontend**:
  - Uses React functional components and hooks
  - Page routing via `src/pages/`
  - Camera and media logic in `CameraPanel.jsx`
- **Backend**:
  - Main entry: `app.py` (REST API)
  - ML models loaded from `physiology/graph/models/`
  - Custom OpenCV libraries (Linux only)
  - Docker setup for reproducible environment

## Integration Points
- Frontend calls backend endpoints for ML inference
- Backend expects Linux environment for OpenCV .so files
- Use Docker for consistent backend setup

## Examples
- To add a new ML model: place `.tflite` in `backend/physiology/graph/models/` and update `app.py` to load it
- To add a new page: create in `interviewer/src/pages/` and update routing in `main.jsx`

## External Dependencies
- React, Vite, ESLint (frontend)
- Python, TensorFlow Lite, OpenCV (backend)
- Docker (backend deployment)

---
Update this file if you change major workflows, add new integration points, or introduce new conventions.
