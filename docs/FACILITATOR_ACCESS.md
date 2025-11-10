# Facilitator Dashboard Access

## How to Access the Facilitator Dashboard

The facilitator dashboard is available as a Streamlit page at:
- **Local:** Navigate to "Facilitator Dashboard" in the sidebar when running the app
- **URL:** `http://localhost:8501/facilitator_dashboard` (when app is running)

## Setting the Password

### Option 1: Using Environment Variable (Recommended for Production)

Set the `ADMIN_PASSWORD` environment variable before running the app:

**Windows (PowerShell):**
```powershell
$env:ADMIN_PASSWORD="your-secure-password"
streamlit run app/main.py
```

**Windows (Command Prompt):**
```cmd
set ADMIN_PASSWORD=your-secure-password
streamlit run app/main.py
```

**Mac/Linux:**
```bash
export ADMIN_PASSWORD="your-secure-password"
streamlit run app/main.py
```

### Option 2: Using .env File (for Development)

Create a `.env` file in the project root:
```
ADMIN_PASSWORD=your-secure-password
```

Then install python-dotenv and load it in your app:
```bash
pip install python-dotenv
```

### Option 3: Streamlit Cloud Secrets

For deployment on Streamlit Cloud:

1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets" section
3. Add:
```toml
ADMIN_PASSWORD = "your-secure-password"
```

### Default Password

If no password is set, the default is: **`changeme`**

⚠️ **Security Warning:** Always change the default password for production use!

## Dashboard Features

The facilitator dashboard includes:

1. **Overview Tab**
   - Workshop timing
   - Program cards reference
   - Session notes area

2. **Coaching Tips Tab**
   - Pre-defined coaching prompts
   - Common challenges and solutions
   - Guidance for stuck teams

3. **Sprint Checklist Tab**
   - Completion checklist for teams
   - Timing guidelines for workshop phases
   - Facilitation tips

## Workshop Timing

Recommended schedule:
- Introduction: 5 min
- Design Sprint (6 steps): 18 min (3 min/step)
- Randomization Practice: 10 min
- Gallery Walk: 10 min
- Report Generation: 5 min
- Debrief: 10 min

**Total: ~60 minutes**
