# Using Environment Variables with .env

This project uses `.env` files to manage environment variables for configuration.

## Quick Start

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   # Open with your text editor
   ADMIN_PASSWORD=your-secure-password-here
   DEBUG_MODE=false
   ```

3. **Variables are automatically loaded when the app starts**

## Available Variables

### Facilitator Dashboard

```env
# Password for accessing the facilitator dashboard
# Default: changeme
ADMIN_PASSWORD=your-secure-password-here
```

### Debug Mode

```env
# Enable debug output and logging
# Default: false
DEBUG_MODE=false
```

### Data Paths (Optional)

```env
# Custom paths for data storage
# Default: ./data
DATA_PATH=./data

# Path to sample data files
# Default: ./data/sample_data
SAMPLE_DATA_PATH=./data/sample_data

# Path to program cards
# Default: ./data/program_cards
PROGRAM_CARDS_PATH=./data/program_cards
```

### Deployment

```env
# RCT Field Flow deployment URL
# Default: https://ajolex.github.io/rct_field_flow
RCT_FIELD_FLOW_URL=https://your-deployment-url
```

## File Structure

- **`.env`** - Your local environment variables (not tracked by git)
- **`.env.example`** - Template file showing all available variables (tracked by git)

## Security Notes

⚠️ **Important:**
- The `.env` file is in `.gitignore` - it won't be committed to git
- Never commit passwords or sensitive data
- Always use `.env.example` as a template for team members
- Change `ADMIN_PASSWORD` from the default before production use

## Streamlit Cloud Deployment

For deployment on Streamlit Cloud:

1. Go to your app's **Secrets** section (not Settings)
2. Add your variables in TOML format:

```toml
ADMIN_PASSWORD = "your-secure-password"
DEBUG_MODE = false
```

See [Streamlit Cloud Secrets Documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

## Loading in Code

The `.env` file is automatically loaded by `app/config.py`:

```python
from dotenv import load_dotenv
import os

# Already loaded by config.py!
password = os.getenv("ADMIN_PASSWORD", "changeme")
```

## Troubleshooting

**Variables not loading?**
1. Check that `.env` is in the project root (same level as `app/` folder)
2. Make sure you're running from the project root: `streamlit run app/main.py`
3. Restart the Streamlit app after changing `.env`

**Can't find `.env` file?**
1. Copy the example: `cp .env.example .env`
2. Or create manually with your settings

**Working with team?**
1. Share `.env.example` (not `.env`)
2. Each team member creates their own `.env` from the example
3. This keeps everyone's passwords and configs private
