# Wendy's AI Agents Hackathon: Marketing Orchestrator

Welcome, participants! This project is a multi-agent system designed to revolutionize marketing at Wendy's by generating novel, data-driven promotional offers. You will be working with a team of AI agents that collaborate to research market trends, analyze customer data, and design compelling new offers.

This guide will walk you through setting up the project, understanding its components, and starting your journey to build the future of fast-food marketing.

## Table of Contents

- [Project Overview](#project-overview)
- [File Structure](#file-structure)
- [Part 1: Quick Start with ADK Web (Recommended)](#part-1-quick-start-with-adk-web-recommended)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Running the System](#running-the-system)
- [Part 2: Using the Streamlit UI (Advanced)](#part-2-using-the-streamlit-ui-advanced)
  - [Overview](#overview)
  - [Setup and Running](#setup-and-running)
- [How the Multi-Agent System Works](#how-the-multi-agent-system-works)
- [Your Mission: What to Modify](#your-mission-what-to-modify)
- [Key Files to Explore](#key-files-to-explore)

---

## Project Overview

The **Marketing Orchestrator** is the root agent that manages a sophisticated workflow. It coordinates three specialized sub-agent teams:

1.  **Market Trends Analyst:** Scans the internet for the latest trends in the fast-food industry, focusing on competitor activities and consumer behavior.
2.  **Customer Insights Agent:** Dives into Wendy's internal (mock) BigQuery database to analyze customer behavior, sentiment, and profile data.
3.  **Competitor Intelligence Agent:** Gathers information on promotions and strategies from Wendy's key competitors.

Once the research is complete, the findings are passed to the **Offer Design Agent**, which synthesizes the information and generates creative, data-backed offer concepts.

---

## File Structure

The repository has been organized to keep the agent source code, documentation, and UI separate.

```
/
├── src/                    # All Python source code for the agents
│   ├── competitor_intelligence/
│   ├── customer_insights/
│   ├── market_trends_analyst/
│   ├── marketing_orchestrator/
│   ├── offer_design/
│   └── utils/
├── ui/                     # Contains the Streamlit user interface
│   └── hackathon_ui.py
├── docs/                   # All non-code documents, guides, and notes
├── scripts/                # Helper scripts for running the project
├── venv/                   # Your local Python virtual environment
└── README.md               # This file
```

---

## Part 1: Quick Start with ADK Web (Recommended)

This is the most stable and straightforward way to run the multi-agent system. It uses Google's built-in Agent Development Kit (ADK) web interface.

### Prerequisites

1.  **Python 3.10+:** Ensure you have a modern version of Python installed.
2.  **Google Cloud Project Access:** You must have access to the `gemini-copilot-testing` project in Google Cloud Platform.
3.  **Google Cloud SDK:** You must have `gcloud` installed and configured.
    - Install it from [here](https://cloud.google.com/sdk/docs/install).
    - After installing, run `gcloud init`.
4.  **Application Default Credentials (ADC):** The agents need to authenticate with Google Cloud services (like Vertex AI).
    - Run the following command in your terminal:
      ```bash
      gcloud auth application-default login
      ```

### Setup Instructions

1.  **Create and Activate a Virtual Environment:**
    - We recommend using `uv` for a fast and reliable experience. If you don't have it, install it with `pip install uv`.
    - From the project root directory, run:
      ```bash
      # Create the virtual environment
      python -m venv venv

      # Activate the environment (on Windows PowerShell)
      .\venv\Scripts\Activate.ps1
      ```

2.  **Install Dependencies:**
    - Use `uv` to install all the required Python packages.
      ```bash
      uv pip install google-adk google-cloud-aiplatform google-cloud-bigquery "uvicorn[standard]" streamlit
      ```

3.  **Configure Environment Variables:**
    - Each agent needs a `.env` file to connect to Google Cloud. **You must create this file in each of the agent directories** inside `src/`.
    - **File Path:** `src/marketing_orchestrator/.env`
    - **File Content:**
      ```
      GOOGLE_GENAI_USE_VERTEXAI="TRUE"
      GOOGLE_CLOUD_PROJECT="483447458116"
      GOOGLE_CLOUD_LOCATION="us-central1"
      ```
    - **Action:** Create the same `.env` file in the following directories:
      - `src/market_trends_analyst/`
      - `src/customer_insights/`
      - `src/competitor_intelligence/`
      - `src/offer_design/`

### Running the System

1.  **Start the ADK Web Server:**
    - Make sure your virtual environment is activated.
    - Run the following command from the project root:
      ```bash
      adk web src/marketing_orchestrator
      ```
    - This will start a local web server, typically at `http://localhost:8000`.

2.  **Interact with the Agent:**
    - Open the provided URL in your browser.
    - In the chat interface, enter your request.
    - **Example Prompt:** `Develop three innovative, app-exclusive offers to increase breakfast traffic among Gen Z customers. Focus on trending flavors and value.`

You will see the agent process your request, and the final offer concepts will be displayed in the UI.

---

## Part 2: Using the Streamlit UI (Advanced)

This project includes a custom Streamlit UI for a more tailored user experience. Please note that this method is currently a work in progress and may have some instability.

### Overview

The Streamlit UI communicates with a backend ADK **API server**. This is different from the `adk web` command, as it exposes the agent as an API rather than a web page.

### Setup and Running

1.  **Complete All Prerequisites and Setup from Part 1.**
    - The virtual environment, dependencies, and `.env` files must be set up correctly first.

2.  **Start the ADK API Server:**
    - In a terminal (with the venv activated), run the following command. We are forcing debug logging to help troubleshoot.
      ```powershell
      $env:ADK_LOG_LEVEL="DEBUG"
      adk api_server src/marketing_orchestrator
      ```
    - This will start the backend server on `http://localhost:8000`.

3.  **Run the Streamlit App:**
    - Open a **second terminal** (and activate the venv).
    - Run the Streamlit app:
      ```powershell
      streamlit run ui/hackathon_ui.py
      ```
    - This will open the Streamlit interface in your browser.

4.  **Interact and Observe:**
    - Use the UI to enter your prompt and click "Generate Offers".
    - Watch the ADK API Server terminal. You should see `DEBUG` logs indicating that the agent run has started.

---

## How the Multi-Agent System Works

This system uses a **Sequential Agent** architecture. The `MarketingOrchestratorAgent` acts as a manager, executing each specialized agent team one by one and passing the results to the next.

1.  **Input:** Your prompt is sent to the `MarketingOrchestratorAgent`.
2.  **Research Phase:**
    - It first invokes the `MarketTrendsAgent` to find relevant articles and trends.
    - The results are passed to the `CustomerInsightsAgent`, which queries the BigQuery database for related customer data.
    - The combined findings are then given to the `CompetitorIntelAgent` for competitive analysis.
3.  **Synthesis Phase:**
    - All research materials are handed over to the `SimplifiedOfferDesignAgent`.
    - This agent's sole purpose is to read the research and generate the final offer concepts in a structured JSON format.
4.  **Output:** The final JSON is sent back to the user interface for display.

---

## Your Mission: What to Modify

Your goal during this hackathon is to improve and experiment with this system. Here are some ideas:

-   **Modify Agent Instructions:** The core logic of each agent is defined in its `instruction.txt` file. Try changing the instructions to alter an agent's behavior, personality, or focus.
-   **Add New Tools:** Create new Python functions and register them as tools for the agents to use. For example, a tool that calculates the potential cost of a promotion.
-   **Change the Agent Architecture:** The main workflow is defined in `src/marketing_orchestrator/agent.py`. Try changing the order of the agents, or even switching to a `ParallelAgent` to have them run at the same time!
-   **Improve the Final Output:** Modify the `SimplifiedOfferDesignAgent` to produce more detailed or differently structured JSON.

## Key Files to Explore

-   **Root Agent Logic:**
    - `src/marketing_orchestrator/agent.py`: Defines the main sequence of agent execution. A great place to change the overall workflow.
-   **Specialist Agent Instructions:**
    - `src/market_trends_analyst/sub_agents/data_collection/instruction.txt`: Controls how the market research agent behaves.
    - `src/customer_insights/sub_agents/behavioral_analysis/instruction.txt`: Defines how the BigQuery database is queried.
-   **Tools:**
    - `src/customer_insights/sub_agents/behavioral_analysis/tools.py`: Contains the Python function that connects to BigQuery. A perfect place to add new data tools.
-   **UI Code:**
    - `ui/hackathon_ui.py`: The Streamlit application. Feel free to customize the user interface.
