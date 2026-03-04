# Automated API Testing Framework

A **production-style Python automation testing framework** that validates REST APIs from [JSONPlaceholder](https://jsonplaceholder.typicode.com), supports regression testing, and runs automatically in a GitHub Actions CI/CD pipeline.

---

## 🗂️ Project Structure

```
api-test-automation/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── reports/                    # HTML test reports (auto-generated)
├── scripts/
│   └── run_tests.sh            # Bash test runner
├── tests/
│   ├── test_posts.py           # Tests for /posts endpoint
│   ├── test_users.py           # Tests for /users endpoint
│   └── test_comments.py        # Tests for /comments endpoint
├── utils/
│   ├── __init__.py
│   └── api_client.py           # Centralised HTTP client module
├── conftest.py                 # Shared pytest fixtures
├── requirements.txt
└── README.md
```

---

## 🛠️ Tools & Technologies

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Test framework | pytest |
| HTTP client | requests |
| Reporting | pytest-html |
| CI/CD | GitHub Actions |
| Script runner | Bash |

---

## ⚙️ Installation

**Prerequisites:** Python 3.9+, pip, Git

```bash
# 1. Clone the repository
git clone https://github.com/fawaz-devs/api-test-automation.git
cd api-test-automation

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Running Tests Locally

### Option A — pytest directly

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_posts.py -v

# Run tests matching a keyword
pytest tests/ -v -k "users"

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html -v
```

### Option B — Bash script (Linux / macOS / WSL)

```bash
chmod +x scripts/run_tests.sh
bash scripts/run_tests.sh

# Pass extra pytest arguments
bash scripts/run_tests.sh -k "comments"
```

The HTML report is saved to **`reports/report.html`** and can be opened in any browser.

---

## 🧪 Test Cases

A total of **35 tests** across three test files:

| File | Category | Count |
|---|---|---|
| `test_posts.py` | Functional, Negative, Edge Cases | 13 |
| `test_users.py` | Functional, Negative, Edge Cases | 11 |
| `test_comments.py` | Functional, Negative, Edge Cases | 11 |

### Validations performed

- ✅ HTTP status code (200, 201, 404)
- ✅ Response JSON structure (required fields present)
- ✅ Expected data field values
- ✅ Response time under 3-second threshold
- ✅ Non-empty response body
- ✅ Content-Type header
- ✅ Email format validation (regex)
- ✅ Query-parameter filtering (`?postId=`)

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on every **push** and **pull request** to `main`, `master`, or `develop`.

### Pipeline steps

```
1. Checkout repository
2. Set up Python 3.11 (with pip cache)
3. Install dependencies (pip install -r requirements.txt)
4. Run pytest test suite
5. Upload HTML report as a downloadable CI artifact
```

> The HTML report is always uploaded — even on test failures — so you can inspect what went wrong.

### Viewing the report in GitHub Actions

1. Navigate to **Actions → your workflow run**
2. Scroll to the **Artifacts** section
3. Download `html-test-report`

---

## 📁 Key Files Explained

| File | Purpose |
|---|---|
| `utils/api_client.py` | Reusable HTTP client (`get_request`, `post_request`) with logging and base URL |
| `conftest.py` | Shared fixtures: `response_time_threshold`, `api_base_url` |
| `scripts/run_tests.sh` | Shell wrapper around pytest for local execution |
| `.github/workflows/ci.yml` | GitHub Actions pipeline definition |

---

## 📊 Example Commands

```bash
# Run all tests
pytest tests/

# Run and generate HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run only negative tests
pytest tests/ -v -k "negative or 404"

# Run with verbose output and short traceback
pytest tests/ -v --tb=short
```

---

## 📝 Notes

- The API under test (`jsonplaceholder.typicode.com`) is a free, read-only mock REST API.  `POST` requests return a simulated response (status `201`) without persisting data, which is the expected behaviour.
- Response time threshold is set to **3 seconds** in `conftest.py` and can be adjusted without touching test files.
