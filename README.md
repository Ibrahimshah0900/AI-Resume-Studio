# 📄 AI Resume Studio

> An intelligent, AI-powered resume builder, analyzer, and ATS optimizer built with Python and Streamlit.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Ibrahimshah0900/AI-Resume-Studio.svg)](https://github.com/Ibrahimshah0900/AI-Resume-Studio/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Ibrahimshah0900/AI-Resume-Studio.svg)](https://github.com/Ibrahimshah0900/AI-Resume-Studio/network/members)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ibrahimshah0900-ai-resume-studio.streamlit.app)

---

## 🚀 Live Demo

**Try the app now:** [AI Resume Studio](https://ibrahimshah0900-ai-resume-studio.streamlit.app)

---

## ✨ Features

- 📝 **Resume Builder** - Drag-and-drop section reordering, live preview, pre-fill sample data, section toggle switches, auto-save with unsaved changes warning
- 📊 **ATS Analysis** - Comprehensive ATS compatibility scoring, keyword and skill extraction, readability and formatting analysis, actionable improvement recommendations
- 🎯 **Job Matching** - TF-IDF similarity scoring, skill match analysis, keyword highlighting, "Click to Add" missing skills
- ✨ **Resume Improvement** - Bullet point analysis, action verb detection, metric extraction, AI-powered enhancement suggestions
- 🎨 **Templates** - ATS Minimal, Modern Professional, AI/Tech Professional, Classic Professional, Student/Graduate
- 📥 **Export Options** - PDF (print-ready), DOCX (editable Word documents)
- 💾 **Multi-Resume Management** - Save multiple drafts, load/copy/delete drafts, auto-save, version history tracking
- 🛡️ **Additional Features** - OCR support for scanned resumes, resume parsing (PDF, DOCX, Images), skill extraction, keyword extraction, resume completion tracking, Computer Vision quality analysis

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit, HTML/CSS
- **Backend:** Python 3.9+, Pydantic
- **NLP & ML:** spaCy, NLTK, Scikit-learn, Sentence Transformers
- **Computer Vision & OCR:** OpenCV, Tesseract OCR, EasyOCR, Pillow
- **Document Processing:** PyMuPDF, python-docx, ReportLab, WeasyPrint
- **Database:** SQLite, JSON
- **Deployment:** Streamlit Cloud, Docker, GitHub Actions

---

## 📦 Installation

### Local Installation

```bash
git clone https://github.com/Ibrahimshah0900/AI-Resume-Studio.git
cd AI-Resume-Studio
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py


Docker Installation
docker build -t ai-resume-studio .
docker run -p 8501:8501 ai-resume-studio

Docker Compose
docker-compose up --build



📁 Project Structure

AI-Resume-Studio/
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── Dockerfile                  # Docker config
├── docker-compose.yml          # Docker Compose
├── .gitignore                  # Git ignore
├── LICENSE                     # MIT License
├── README.md                   # Documentation
├── CONTRIBUTING.md             # Contributing guide
├── CODE_OF_CONDUCT.md          # Code of conduct
├── components/                 # UI components
│   ├── dashboard.py
│   ├── resume_builder.py
│   ├── job_match.py
│   ├── resume_improvement.py
│   ├── resume_templates.py
│   └── resume_export.py
├── utils/                      # Core utilities
│   ├── data_models.py
│   ├── completion_engine.py
│   ├── resume_builder_core.py
│   ├── resume_parser.py
│   ├── ocr_parser.py
│   ├── text_cleaner.py
│   ├── section_detector.py
│   ├── skill_extractor.py
│   ├── keyword_extractor.py
│   ├── ats_analyzer.py
│   ├── job_matcher.py
│   ├── resume_improver.py
│   ├── cv_analyzer.py
│   ├── template_engine.py
│   ├── template_renderer.py
│   ├── pdf_generator.py
│   ├── repository.py
│   ├── app_state.py
│   ├── resume_manager.py
│   └── config.py
├── assets/                     # Static assets
│   ├── styles/
│   └── templates/
├── data/                       # Data storage
│   ├── sample_resumes/
│   └── resume_drafts/
├── tests/                      # Test files
└── .github/                    # GitHub config
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── ci.yml



🚀 Usage Guide
Create a Resume - Open the app, click "⚡ Pre-fill Sample Data" for a demo, or fill in your information manually. Use the live preview to see changes in real-time. Save your resume as a draft.

Analyze Your Resume - Go to "📊 Resume Analysis", paste a job description (optional), click "🔍 Analyze Resume", view your ATS score and recommendations.

Match with Job Descriptions - Go to "🎯 Job Match", paste a job description, click "🎯 Run Job Match", see matching score and missing skills.

Improve Your Resume - Go to "✨ Resume Improvement", click "✨ Analyze for Improvements", view suggestions for weak bullets and missing metrics.

Export Your Resume - Go to "📥 Export", select a template, choose PDF or DOCX, generate and download.



🔧 Configuration
Create a .env file:
RESUME_DB_PATH=data/resumes.db
AUTO_SAVE_ENABLED=true
AUTO_SAVE_INTERVAL_SECONDS=30
DEFAULT_TEMPLATE=ats_minimal
SEMANTIC_MODEL_NAME=all-MiniLM-L6-v2
APP_NAME=AI Resume Studio
APP_VERSION=1.0.0
DEBUG=False

🤝 Contributing
We welcome contributions! Please see CONTRIBUTING.md for detail
# Fork the repository, then:
git clone https://github.com/YOUR_USERNAME/AI-Resume-Studio.git
cd AI-Resume-Studio
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
# Create a Pull Request



📄 License
This project is licensed under the MIT License - see the LICENSE file for details.



🙏 Acknowledgments
Built with Streamlit

NLP powered by spaCy and Sentence Transformers

PDF processing with PyMuPDF

OCR from Tesseract

📬 Contact
Ibrahim Shah

GitHub: @Ibrahimshah0900

Live App: AI Resume Studio

⭐ Show Your Support
If you like this project, please ⭐ star the repository!

Made with ❤️ by Ibrahim Shah


