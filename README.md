# MatchUp — Football Tournament Tracker
### Software Development & DevOps — Individual Assignment 2

**Author:** Fares Qaddoumi  
**Institution:** IE University  
**Course:** Software Development & DevOps  

---

##  Overview

**MatchUp** is a lightweight football tournament tracker used to manage friendly competitions.  

The application supports:

- Creating and editing teams  
- Recording match results  
- Automatic leaderboard updates  
- User signup and login  
- Health and monitoring endpoints  
- Containerized backend  
- Automated CI/CD pipeline  
- Cloud deployment on Render  
- Prometheus metrics for monitoring  

For Assignment 2, the system was improved with:

- Refactoring and cleanup  
- Pytest test suite with 90%+ coverage  
- CI pipeline running tests, coverage, and Docker builds  
- Docker image for local and cloud deployment  
- Prometheus metrics and health checks  
- Auto‑deployments from `main`  

---

##  Tech Stack

| Component        | Technology              |
|------------------|-------------------------|
| Backend          | Python (Flask)          |
| Database         | SQLite                  |
| Frontend         | HTML, CSS, JavaScript   |
| Testing          | Pytest + Coverage       |
| Continuous Integration | GitHub Actions      |
| Continuous Deployment | Render (Docker‑based) |
| Monitoring       | Prometheus             |
| Version Control  | Git & GitHub           |
| Containerization | Docker                 |

---

##  Project Structure

matchup/
│
├── backend/
│   ├── app.py               # Flask app entrypoint
│   ├── db.py                # Database initialization and helpers
│   ├── auth.py              # Authentication routes
│   ├── teams.py             # Team management routes
│   ├── matches.py           # Match‑related routes
│   ├── leaderboard.py       # Leaderboard logic
│   ├── metrics.py           # Prometheus metrics setup
│   ├── tests/               # Pytest test suite
│   └── __init__.py
│
├── frontend/
│   ├── index.html
│   ├── auth.html
│   ├── teams.html
│   ├── leaderboard.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│
├── Dockerfile               # Backend Docker image definition
├── docker-compose.yml       # (Optional) Local multi‑service setup
├── prometheus.yml           # Local Prometheus configuration
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline (tests + coverage + build)
└── README.md
 
 **Running the Backend Locally**
## 1  . Install Dependencies
From the project root:

bash
**Copy code**
- cd backend
- pip install -r requirements.txt
## 2. Initialize the SQLite Database
bash
**Copy code**
- python -m backend.db
This creates the necessary tables if they don’t already exist.

## 3. Start the Backend Server
bash
**Copy code**
- python -m backend.app
- The backend will run at:

http://127.0.0.1:5000

 **Running the Frontend**
- From the project root:

bash
**Copy code**
- cd frontend
- python -m http.server 5500
Then open:

http://127.0.0.1:5500

in your web browser.

 ## Testing and Coverage
All tests are located inside:

bash
Copy code
- backend/tests/
**Run all tests**
bash
Copy code
- cd backend
- pytest
**Run tests with coverage**
bash
Copy code
- pytest --cov=backend --cov-report=term-missing
**Local coverage: around 90 %**

CI coverage threshold: 70 % (the pipeline fails if below this threshold)

## Generate HTML coverage report
bash
**Copy code**
- pytest --cov=backend --cov-report=html
This will create an htmlcov/ directory containing a browsable coverage report.

**Docker Usage**
Build the image
From the project root:

bash
**Copy code**
- docker build -t matchup-backend .
**Run the container**
bash
Copy code
- docker run -p 5000:5000 matchup-backend
The backend will be available at:

http://localhost:5000

 ## CI/CD Pipeline
 Continuous Integration (GitHub Actions)
File:

bash
Copy code
- .github/workflows/ci.yml
The CI pipeline:

Checks out the repository

Sets up Python

Installs dependencies

Runs tests

Measures coverage

Fails the pipeline if:

Any test fails, or

Coverage is below 70 %

Builds the Docker image

 **Continuous Deployment (Render)**
The app is deployed to Render using the Dockerfile.

Auto‑deploy is enabled only for the main branch.

Every successful push to main triggers a new deploy.

The live production URL is:

https://matchup-7p8i.onrender.com

 **Monitoring and Health Checks**
Health Endpoint
bash
**Copy code**
- /health
Returns a basic JSON status indicating whether the application is up.

**Prometheus Metrics Endpoint**
bash
Copy code
- /metrics_prom
Exports metrics such as:

Total request count

Error count

Request latency (histograms)

Per‑route statistics

**Local Prometheus Setup**
A minimal prometheus.yml is provided in the repository. Example scrape configuration:

**yaml**
**Copy code**
scrape_configs:
  - job_name: "matchup"
    static_configs:
      - targets:
          - "host.docker.internal:5000"
You can run Prometheus locally with:

bash
Copy code
- docker run -p 9090:9090 \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
**Prometheus UI will be available at:**

http://localhost:9090

 **SDLC Model**
This project uses the Incremental Development Model.

Each feature (teams, matches, authentication, leaderboard, monitoring, CI/CD) was:

Designed

Implemented

Tested locally

Integrated into the main codebase

 Advantages of this model for MatchUp: 

Early discovery of bugs

Continuous integration of working increments

Easier rollback and refactoring

Natural alignment with DevOps practices (small, frequent, testable changes)

 **Future Improvements**
Potential next steps for MatchUp:

Add frontend CI (linting, formatting, and basic UI tests)

Integrate Grafana dashboards on top of Prometheus metrics

Migrate from SQLite to PostgreSQL for production use

Add caching (for example, Redis) for leaderboard and heavy queries

Implement rate limiting and stronger input validation

Extend authentication with user roles (e.g., admin, standard user)

Add API documentation (e.g., using Swagger or OpenAPI)




