# Quick Start Guide - Running the Hackathon UI

## The Problem You Had

When you ran `pip install streamlit requests`, you got an error because the `pip` launcher was pointing to a different virtual environment path.

## The Solution

**Always use `python -m pip` instead of `pip` directly** when you have venv path issues.

## Complete Setup & Run Instructions

### Step 1: Activate Virtual Environment

```powershell
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
```

### Step 2: Install Dependencies (If Not Already Done)

```powershell
python -m pip install streamlit requests
```

✅ **This should now work!** (Streamlit is already installed from above)

### Step 3: Run the System

You need **TWO separate terminals/windows** running simultaneously:

#### Option A: Use the Launch Script (Easiest)

```powershell
.\run_hackathon.ps1
```

This automatically opens two windows:
- Window 1: ADK API Server
- Window 2: Streamlit UI

#### Option B: Manual Setup (Two Terminals)

**Terminal 1 - ADK API Server:**
```powershell
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
adk api_server marketing_orchestrator
```

**Terminal 2 - Streamlit UI:**
```powershell
cd C:\Users\birup\Documents\wendy-hack-sprint
.\venv\Scripts\activate
streamlit run hackathon_ui.py
```

### Step 4: Access the UI

- **Streamlit UI**: http://localhost:8501 (opens automatically)
- **ADK API**: http://localhost:8000 (runs in background)

## Troubleshooting Common Issues

### Issue 1: "pip" command fails

**Solution**: Always use `python -m pip` instead:
```powershell
python -m pip install <package>
```

### Issue 2: Virtual environment not activating

**Solution**: Use full path:
```powershell
.\venv\Scripts\Activate.ps1
```

Or if you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Issue 3: ADK server not starting

**Check**:
1. Is port 8000 already in use?
2. Are you in the correct directory?
3. Is the virtual environment activated?

**Test ADK**:
```powershell
adk --version  # Should show version
```

### Issue 4: Streamlit can't connect to ADK

**Symptoms**: "Failed to connect to ADK server" error in UI

**Solutions**:
1. Make sure ADK server is running in Terminal 1
2. Check if ADK is listening: Open http://localhost:8000/health in browser
3. Verify the URL in `hackathon_ui.py` matches your setup

### Issue 5: Module not found errors

**Solution**: Reinstall in virtual environment:
```powershell
.\venv\Scripts\activate
python -m pip install --upgrade streamlit requests
```

## Best Practices

### ✅ DO:
- Always activate venv first: `.\venv\Scripts\activate`
- Use `python -m pip` for installations
- Run ADK server before Streamlit UI
- Keep both terminals open while using the UI

### ❌ DON'T:
- Don't use `pip` directly (use `python -m pip`)
- Don't run Streamlit before ADK server
- Don't close the ADK server terminal while using UI

## Verification Checklist

Before running the UI, verify:

- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] Streamlit installed: `python -m pip show streamlit`
- [ ] Requests installed: `python -m pip show requests`
- [ ] ADK installed: `adk --version`
- [ ] GCP authentication: `gcloud auth application-default login`
- [ ] ADK server can start: `adk api_server marketing_orchestrator` (test in separate terminal)

## Quick Test

Test if everything works:

1. Start ADK server:
   ```powershell
   adk api_server marketing_orchestrator
   ```

2. In a new terminal, start Streamlit:
   ```powershell
   streamlit run hackathon_ui.py
   ```

3. Open http://localhost:8501
4. You should see the Mission Control UI
5. Click "Generate Offers" with default settings
6. Should connect to ADK and run agents

## Need Help?

If you encounter other issues:
1. Check `ACCESS_REQUIREMENTS.md` for GCP setup
2. Check `README_HACKATHON_UI.md` for UI-specific issues
3. Verify all `.env` files exist in agent directories
4. Ensure GCP project access is configured

