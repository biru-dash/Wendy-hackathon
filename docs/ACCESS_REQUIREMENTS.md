# Access Requirements for Multi-Agent System

This document outlines all the access, permissions, and configurations needed to run the Marketing Orchestrator multi-agent system.

## 1. Google Cloud Platform (GCP) Access

### Required Services
- **Vertex AI**: For running LLM agents (Gemini models)
- **BigQuery**: For storing and querying customer data

### Required Permissions

#### Project Access
- **Project ID**: `483447458116`
- **Project Region**: `us-central1` (or your preferred region)
- You need to be a **member** of the GCP project with appropriate roles

#### IAM Roles Required
The service account or user account needs these roles:

**Minimum Required Roles:**
```
roles/bigquery.dataViewer    # Read data from BigQuery
roles/bigquery.jobUser       # Run queries in BigQuery
roles/aiplatform.user        # Use Vertex AI APIs
```

**Recommended (if you need to create/load data):**
```
roles/bigquery.dataEditor    # Write data to BigQuery
roles/bigquery.admin         # Create datasets and tables
```

### Authentication Methods

#### Option 1: Application Default Credentials (Recommended)
```bash
gcloud auth application-default login
```
This sets up local authentication for development.

#### Option 2: Service Account (For Production)
1. Create a service account in GCP Console
2. Download the JSON key file
3. Set environment variable:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="path\to\service-account-key.json"
   ```

#### Option 3: gcloud CLI Authentication
```bash
gcloud auth login
gcloud config set project 483447458116
```

## 2. Vertex AI API Access

### Enable APIs
Ensure these APIs are enabled in your GCP project:
- **Vertex AI API**
- **Vertex AI Gemini API**

Enable via console:
```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

### Required Models
The system uses these Gemini models:
- `gemini-2.5-pro` (default for complex tasks)
- `gemini-2.5-flash` (default for fast/simple tasks)

**Note**: Ensure these models are available in your region (us-central1).

## 3. BigQuery Access

### Required Dataset
- **Dataset ID**: `wendys_hackathon_data`
- **Location**: `US` (or your configured location)

### Required Tables
The system expects these tables to exist:
- `crm_data` - CRM and loyalty customer visit data
- `redemption_logs` - Redemption logs and offer history
- `feedback_data` - Customer feedback, reviews, and sentiment data
- `customer_segments` - (Optional) For saving synthesized insights

### Creating Tables (If Needed)
You can create these using the data loader:
```bash
cd customer_insights/data
python bigquery_loader.py
```

### Data Access
- **Read Access**: Needed by `BehavioralAnalysisAgent` and `SentimentAnalysisAgent`
- **Write Access**: Needed by `ProfileSynthesizerAgent` (if using BigQuery save tools)

## 4. Google Search API Access

### Used By
- `MarketTrendsAnalystAgent` - For finding market trends and URLs
- `CompetitorIntelligenceAgent` - For researching competitors

### Access Method
The system uses **Google Search tool from ADK**, which uses:
- Built-in Google Search capabilities via ADK
- May require Google Search API access depending on usage

**Note**: ADK's `google_search` tool may have rate limits. For production, you may need:
- Google Custom Search API (requires API key)
- Or use ADK's built-in search (if included in your ADK plan)

## 5. Environment Configuration

### Required Environment Variables

Each agent directory needs a `.env` file:

**Location**: `[agent_directory]/.env`

**Contents**:
```env
GOOGLE_GENAI_USE_VERTEXAI="TRUE"
GOOGLE_CLOUD_PROJECT="483447458116"
GOOGLE_CLOUD_LOCATION="us-central1"
```

**Agents with .env files:**
- `customer_insights/.env`
- `competitor_intelligence/.env`
- `offer_design/.env`
- `marketing_orchestrator/.env`

### Optional Environment Variables
```env
GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"  # If using service account
GEN_ADVANCED_MODEL="gemini-2.5-pro"                                # Override default model
GEN_FAST_MODEL="gemini-2.5-flash"                                   # Override fast model
BIGQUERY_DATASET="wendys_hackathon_data"                            # Override dataset
```

## 6. Python Dependencies

### Required Packages
Install via:
```bash
pip install -r requirements.txt  # If exists
```

Or manually install:
```bash
pip install google-cloud-bigquery
pip install google-cloud-aiplatform
pip install pandas
pip install pyarrow
pip install google-adk  # Google Agent Development Kit
```

See `customer_insights/data/requirements.txt` for data-related dependencies.

## 7. Network Access

### Required Outbound Access
- **HTTPS to Google Cloud APIs**: For Vertex AI and BigQuery
- **HTTPS to google.com**: For Google Search functionality
- **Port 443**: Standard HTTPS port

### Firewall/Proxy Considerations
If behind corporate firewall:
- Whitelist `*.googleapis.com`
- Whitelist `*.google.com`
- Allow outbound HTTPS connections

## 8. Local Development Setup

### Prerequisites
- **Python 3.8+**: Required for ADK and dependencies
- **Virtual Environment**: Recommended isolation
- **PowerShell or Bash**: For running commands

### Setup Steps
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Install dependencies
pip install google-cloud-bigquery google-cloud-aiplatform pandas pyarrow google-adk

# 4. Authenticate with GCP
gcloud auth application-default login

# 5. Verify access
gcloud config get-value project  # Should show 483447458116
```

## 9. Verification Checklist

Run these checks to verify all access:

### ✅ GCP Access
```bash
gcloud auth list                    # Should show your account
gcloud config get-value project     # Should show 483447458116
gcloud projects describe 483447458116  # Should show project details
```

### ✅ Vertex AI Access
```python
from google.cloud import aiplatform
aiplatform.init(project="483447458116", location="us-central1")
# Should not throw errors
```

### ✅ BigQuery Access
```python
from google.cloud import bigquery
client = bigquery.Client(project="483447458116")
datasets = list(client.list_datasets())
# Should list wendys_hackathon_data
```

### ✅ ADK Access
```bash
adk --version  # Should show ADK version
adk web src  # Should start web server (then select "marketing_orchestrator" from dropdown)
```

## 10. Troubleshooting Access Issues

### "Missing key inputs argument" Error
- **Cause**: Not using Vertex AI, trying to use Google AI Studio API
- **Fix**: Ensure `.env` file exists with `GOOGLE_GENAI_USE_VERTEXAI="TRUE"`

### "Permission denied" for BigQuery
- **Fix**: Add `roles/bigquery.dataViewer` and `roles/bigquery.jobUser` to your account

### "Project not found" Error
- **Fix**: Verify project ID `483447458116` is correct and you have access

### "Model not available" Error
- **Fix**: Check if Gemini models are available in your region (us-central1)
- **Alternative**: Change `GOOGLE_CLOUD_LOCATION` in `.env` files

### "Dataset not found" Error
- **Fix**: Create dataset using `customer_insights/data/bigquery_loader.py`
- Or verify dataset ID `wendys_hackathon_data` exists

## 11. Production Considerations

### For Production Deployment:
1. **Use Service Accounts** (not user credentials)
2. **Enable Audit Logging** for BigQuery and Vertex AI
3. **Set up Budget Alerts** in GCP Console
4. **Configure VPC** if using VPC-native services
5. **Enable API Quotas** to prevent unexpected charges
6. **Use IAM Conditions** for fine-grained access control

### Cost Considerations:
- **Vertex AI**: Pay-per-use for API calls
- **BigQuery**: Pay per query and storage
- **Google Search**: May have rate limits or costs depending on API used

## 12. Summary

**Minimum Requirements:**
1. ✅ GCP project access (`483447458116`)
2. ✅ Vertex AI API enabled
3. ✅ BigQuery dataset access (`wendys_hackathon_data`)
4. ✅ Application Default Credentials set up (`gcloud auth application-default login`)
5. ✅ `.env` files in each agent directory
6. ✅ Python dependencies installed
7. ✅ ADK installed and configured

**Recommended:**
- Service account for production
- Budget alerts configured
- Audit logging enabled

Once all requirements are met, you can run:
```bash
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
adk web src
# Then select "marketing_orchestrator" from the dropdown in the web interface
```

