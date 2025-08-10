# 🚀 Dev Toolbox

An all-in-one, AI-powered dashboard built with [Streamlit](https://streamlit.io/) that unifies DevOps workflows, generative AI tools, and development utilities into a single, interactive interface.

---

## Features

- **AI & Machine Learning:**
  - **Gemini Integration:** Direct chat interface with Google's Gemini API.
  - **AI Tutor:** An interactive assistant to explain complex technical concepts.
  - **LangChain Support:** Tools for building agentic AI workflows.
  - **ML Model Dashboards:** Interactive demos for models like Linear Regression.

- **DevOps & Cloud Automation:**
  - **AWS Automation:** Programmatically manage and launch EC2 instances.
  - **Docker & Kubernetes Menus:** View and manage containers and cluster information from a simple UI.
  - **Git Automation:** Utilities to simplify and automate common Git commands.

- **Web & Scripting Utilities:**
  - **Interactive JavaScript Playground:** Live demos for media capture, speech recognition, and social media sharing.
  - **Web Scraping Tools:** Modules for extracting data from websites like Amazon.
  - **Linux & Python Command Centers:** Execute scripts and commands directly from the dashboard.

- **Modern & Extensible UI:**
  - **Unified Dashboard:** A clean, single-page application experience.
  - **Modular Architecture:** Easily add new tools and features by adding files to the `module/` directory.
  - **User Management:** Includes an admin panel and support for user data.

---

## Getting Started

### Prerequisites

- Python 3.9+
- An active [Google Gemini API Key](https://ai.google.dev/).

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/[YOUR_PROJECT_REPO].git
   cd [YOUR_PROJECT_REPO]

### Usage
1.Launch the application using the command above.
2.Use the sidebar menu to navigate between the different modules (e.g., AI Tutor, AWS Manager, Docker Menu).
3.Each tool is loaded dynamically within the main interface. For browser-based tools in the "JS Playground," functionality will run directly in your browser.

### Project Structure
.
├── app.py                  # Main Streamlit application entry point
├── module/                 # All feature modules
│   ├── ai_tutorm.py
│   ├── aws_automation.py
│   ├── docker_menu.py
│   ├── linear_regression.py
│   ├── amazon_webscrape.py
│   └── ...                 # Other modules
├── requirements.txt        # Python dependencies
├── .env                    # For storing API keys (local only)
└── README.md
### Author
[Riya Sharma]
LinkedIn: [https://www.linkedin.com/in/riya-sharma-638a6b217]
