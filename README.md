# The Python Sage 🐍

[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The Python Sage is an interactive, AI-powered tutor designed to help users master Python concepts. Leveraging Google's Gemini Pro model, this application transforms the official Python tutorial documentation into dynamic quizzes, code challenges, and in-depth reviews. It features a unique voice-activated follow-up system, allowing users to ask questions and get instant clarification via audio.

## Key Features

-   **Multiple Learning Modes:** Choose from three distinct modes:
    -   **Complete Section Review:** Get a detailed, point-by-point explanation of every concept in a topic, complete with definitions and code examples.
    -   **Concept-by-Concept Code Challenges:** Generate a series of targeted coding exercises for each concept within a topic.
    -   **1 Comprehensive Code Challenge:** Tackle a single, multi-step capstone problem that integrates multiple concepts from the selected topic.
-   **Adjustable Difficulty:** Tailor the content to your skill level, from "Infant" for absolute beginners to "PHD" for seasoned experts.
-   **Voice-Activated Follow-ups:** After generating a quiz, use the built-in audio recorder to ask clarifying questions about the material. The AI will provide a concise, context-aware answer.
-   **Comprehensive Content:** Covers a wide range of topics sourced directly from the official Python 3 tutorial documentation.
-   **Secure and Private:** Your Google API key is processed exclusively in-session and is never stored or logged.
-   **Slick, Responsive UI:** A clean, two-column layout with a sticky follow-up column for a seamless desktop experience. The UI intelligently adapts, hiding advanced features until an API key is provided.

## Visual Demo

Here is a look at the application in action, showcasing the main interface after a quiz has been generated.
[![Python Sage Demo Thumbnail](https://raw.githubusercontent.com/DawsonSallee/PythonForge_App/main/demo_thumbnail.png)](https://raw.githubusercontent.com/DawsonSallee/PythonForge_App/main/python_sage_demo.mp4)


## Project Structure

The repository is organized to be simple and maintainable:

```
.
├── .gitignore               # Ensures sensitive files and artifacts are not committed.
├── app.py                   # The main Streamlit application script.
├── audio_follow_up.py       # A modular component for the audio recorder and follow-up logic.
├── python_sage_demo.mp4     # The video file used for the welcome screen demo.
├── python_tutorial_library.json # A JSON file containing the pre-processed Python tutorial content.
└── requirements.txt         # A list of all necessary Python packages for the project.
```

---

## 🚀 Setup and Installation

Follow these steps to get The Python Sage running on your local machine.

### Prerequisites

-   [Python](https://www.python.org/downloads/) (version 3.9 or higher)
-   [Git](https://git-scm.com/downloads/) for cloning the repository

### 1. Clone the Repository

Open your terminal or command prompt and run the following command:

```bash
git clone <your-repository-url>
cd <repository-folder-name>
```

### 2. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv .venv
.venv\Scripts\activate

# For macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install all the required packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Get Your Google API Key

This application requires a Google API key to interact with the Gemini model.

1.  Go to the [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Sign in with your Google account.
3.  Click on the **"Create API key in new project"** button.
4.  Copy the generated key. You will paste this into the application's sidebar.

## ▶️ Running the Application

Once the setup is complete, run the following command in your terminal from the project's root directory:

```bash
streamlit run app.py
```

Your web browser should automatically open with the application running.

---

## 📖 How to Use the App

1.  **Enter Your API Key:** On the left sidebar, paste your Google API Key into the designated input field. The main application interface will appear.
2.  **Select a Topic:** Choose a Python topic you want to learn about from the "Choose a topic" dropdown menu.
3.  **Select a Quiz Mode:** Use the radio buttons to select your preferred learning mode (e.g., "Complete Section Review").
4.  **Select a Difficulty:** Adjust the slider to match your current knowledge level.
5.  **Generate Quiz:** Click the "✨ Generate My Quiz!" button. The main content area will populate with the AI-generated material.
6.  **Ask a Follow-up Question:**
    -   In the right-hand column, click the microphone icon in the "Ask a Follow-up" section.
    -   Record your question about the content on the left.
    -   Stop the recording. The app will process your audio and display a text-based answer from the AI below the recorder.

## 🛠️ Architectural Deep Dive

### State Management (`st.session_state`)

The application relies heavily on Streamlit's `st.session_state` to maintain persistence across user interactions and re-runs:
-   `st.session_state.api_key`: Stores the user-provided API key.
-   `st.session_state.chat_session`: Holds the active `genai.GenerativeModel.start_chat()` instance, allowing for contextual follow-up questions.
-   `st.session_state.last_quiz_response`: Caches the most recently generated quiz content.
-   `st.session_state.follow_up_response`: Stores the AI's answer to an audio follow-up question.
-   `st.session_state.quiz_count`: A counter used to create unique keys for the audio recorder widget, forcing it to reset when a new quiz is generated.

### Conditional UI Layout

The application uses a clever trick to hide the `follow_up_col` until an API key is provided. The `st.columns()` definition is wrapped in an `if/else` block:

```python
if api_key:
    # When the key exists, create a balanced two-column layout
    main_col, follow_up_col = st.columns([1.25, 1])
else:
    # When no key exists, create an extremely unbalanced layout
    # This visually "hides" the follow_up_col by making it too narrow to see
    main_col, follow_up_col = st.columns([100, 1])
```
This ensures the `with follow_up_col:` block never causes an error, while providing a clean welcome screen for new users.

### Prompt Engineering

The core logic resides in the `PROMPT_TEMPLATES` dictionary in `app.py`. Each key corresponds to a quiz mode and holds a detailed, structured prompt. These prompts instruct the Gemini model on its persona, task, constraints, and, most importantly, the **MANDATORY OUTPUT STRUCTURE**. This strict formatting ensures the AI's output is consistent and can be reliably rendered in the UI.

## 🔒 Security

Security and user privacy are top priorities.
-   **API Key Handling:** Your Google API key is **never stored** by the application. It is only held in the server's memory for the duration of your session and is immediately discarded when you close the browser tab. The input field is of `type="password"` to mask it from shoulder-surfers.
-   **No Prompt Injection Risk:** The application's prompts are constructed from trusted, hard-coded templates and predefined user selections (dropdowns, sliders). Raw user text is not formatted into the prompts, mitigating the risk of prompt injection attacks.
-   **Secure Configuration:** The `.gitignore` file is configured to explicitly ignore sensitive files, including virtual environments (`.venv`), environment variable files (`.env`), and Streamlit's secret management file (`.streamlit/secrets.toml`), preventing accidental credential exposure.

## 🤝 How to Contribute

Contributions are welcome! If you have ideas for new features, find a bug, or want to improve the documentation, please feel free to:
1.  Open an issue to discuss the change.
2.  Fork the repository.
3.  Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
4.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5.  Push to the branch (`git push origin feature/AmazingFeature`).
6.  Open a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🙏 Acknowledgments

-   The tutorial content is based on the official [Python 3 Documentation](https://docs.python.org/3/tutorial/index.html).
-   Built with the amazing [Streamlit](https://streamlit.io/) framework.
-   Powered by [Google's Gemini API](https://ai.google.dev/).
