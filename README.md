
# DocuFlow – Document Approval Workflow (Phase 1)

DocuFlow is a document approval workflow system built using **Django** and **FastAPI**.  
This project demonstrates a real-world approval flow where a user can create documents, submit them for approval, and an approver can approve or reject them.

---

## 🚀 Features

### ✅ Django (UI + Core Backend)
- User authentication (Login / Logout)
- Document creation
- Document listing dashboard
- Document detail view
- Approval status tracking (Draft / Submitted / Approved / Rejected)
- Audit logs for document actions

### ⚡ FastAPI (Workflow Engine)
- Assigns approver automatically
- Handles workflow actions:
  - Submit
  - Approve
  - Reject
- Maintains workflow rules separately from Django

---

## 🛠️ Tech Stack

- **Frontend UI**: Django Templates (Phase 1)
- **Backend**: Django (Python)
- **Workflow Engine**: FastAPI (Python)
- **Database**: SQLite
- **Authentication**: Django session-based login

---

## 📁 Project Structure

```txt
DocuFlow/
│
├── phase1_django/         # Django project (UI + document system)
├── phase1_fastapi/        # FastAPI workflow engine
├── requirements.txt
├── fixtures.json          # sample data
├── pytest.ini
└── DocuFlow_Submission.zip


⸻

✅ Setup Instructions

1️⃣ Create & Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies

pip install -r requirements.txt


⸻

▶️ Run Django Server

cd phase1_django
python manage.py migrate
python manage.py runserver

Django will run at:

http://127.0.0.1:8000/


⸻

▶️ Run FastAPI Workflow Server

Open a new terminal:

cd phase1_fastapi
uvicorn main:app --reload --port 8001

FastAPI will run at:

http://127.0.0.1:8001/


⸻

🔑 Sample Users (If fixtures loaded)

Submitter User
	•	Username: submitter
	•	Password: submitter123

Approver User
	•	Username: approver
	•	Password: approver123

⸻

🧪 Load Sample Data (Optional)

From phase1_django/ folder:

python manage.py loaddata ../fixtures.json


⸻

📌 Workflow
	1.	Submitter logs in
	2.	Creates a document (Draft)
	3.	Clicks Submit
	4.	FastAPI assigns an approver
	5.	Approver logs in and Approves/Rejects
	6.	Status updates in Django dashboard
	7.	Audit logs record every action

⸻

✅ Notes
	•	This is Phase 1 implementation.
	•	Django templates are used for UI in this phase.
	•	FastAPI is used only for workflow engine logic.

⸻

👨‍💻 Author

Omprakash Ghorpade
GitHub: https://github.com/Omprakash6353

