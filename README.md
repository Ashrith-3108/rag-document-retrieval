📄 Document Retrieval System using RAG

A Django-based Document Retrieval System built using Retrieval-Augmented Generation (RAG) to perform semantic document search and context-aware text generation.
This project demonstrates the integration of NLP, deep learning, and information retrieval techniques in a full-stack application.

⚠️ Note: This project is not deployed. It is designed to run locally for academic, learning, and portfolio purposes.

🚀 Project Overview

Traditional document retrieval systems rely on keyword matching, which often fails to capture semantic meaning.
This project enhances document search by combining:

Dense document retrieval

Transformer-based language models

Context-aware answer generation

Using RAG (Retrieval-Augmented Generation), the system retrieves relevant documents first and then generates accurate responses grounded in those documents.

✨ Key Features

User Registration & Login

Document Upload

Semantic Document Retrieval

Context-Aware Answer Generation

Accuracy-Based Ranking

Document Download

AWS S3 Integration (Demo Only)

🧠 Technology Stack
Backend

Python 3.7+

Django

NLP & AI

Hugging Face Transformers

RAG (facebook/rag-sequence-nq)

Sentence Transformers

FAISS (CPU)

Database

SQLite / MySQL (Local setup)

Cloud (Demo Purpose)

AWS S3 (No credentials committed)

Frontend

HTML

CSS

📁 Project Structure
Document Retrieval System using RAG/
│
├── Rag/                     # Django project settings
├── RagApp/                  # Core application logic
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── screenshots/             # Application screenshots
├── manage.py
├── requirements.txt
├── run.bat
└── README.md

⚙️ Installation & Setup (Local Only)
1️⃣ Prerequisites

Python 3.7.x

pip

MySQL (optional)

2️⃣ Clone the Repository
git clone https://github.com/Ashrith-3108/rag-document-retrieval.git
cd rag-document-retrieval

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Database Setup

Use SQLite (default) OR

Execute SQL commands from:

database.txt

5️⃣ Run the Application
python manage.py runserver


OR (Windows):

run.bat

6️⃣ Open in Browser
http://127.0.0.1:8000/index.html

📸 Application Screenshots

Screenshots are stored in the screenshots/ folder

🏠 Home Page

📝 User Registration

🔐 User Login

☁️ Document Upload

🔎 Document Retrieval

✍️ Text Generation

☁️ AWS S3 Integration (Demo Only)

The project includes AWS S3 integration logic for storing documents.

AWS credentials are NOT included

Credentials are expected via environment variables

This feature is for demonstration only

import boto3

s3 = boto3.client(
    's3',
    region_name='ap-south-1'
)

🔐 Security & GitHub Compliance

✅ No AWS keys committed

✅ No secrets exposed

✅ .gitignore properly configured

✅ GitHub Push Protection passed

📌 Project Status

✔ Fully functional locally

❌ Not deployed

🎓 Ideal for:

Academic submission

Resume projects

GitHub portfolio

👨‍💻 Author

Ashrith
GitHub: https://github.com/Ashrith-3108

🙏 Acknowledgments

Hugging Face for Transformers & RAG

FAISS for fast vector search

Django framework

Open-source NLP community

⭐ If you find this project useful, consider starring the repository!
