# Deployment Guide

This guide covers deployment options for the RCT Design Activity Streamlit app.

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud (Recommended)](#streamlit-cloud-recommended)
3. [Docker Deployment](#docker-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Azure Deployment](#azure-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv or conda)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/ajolex/rct-design-activity.git
cd rct-design-activity

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python app/utils/sample_data_gen.py

# Run the app
streamlit run app/main.py
```

The app will open at `http://localhost:8501`.

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=False
ADMIN_PASSWORD=your_secure_password_here
DATA_PATH=./data
```

---

## Streamlit Cloud (Recommended)

### Advantages
- Free tier available (up to 3 apps)
- Automatic deployments from GitHub
- Built-in SSL/HTTPS
- Easy sharing via public URL
- No infrastructure management

### Setup Steps

1. **Push to GitHub**
   - Ensure code is committed and pushed to a GitHub repository
   - Repository should be public

2. **Create Streamlit Cloud Account**
   - Go to https://share.streamlit.io/
   - Sign up with GitHub

3. **Deploy App**
   - Click "New app"
   - Select repository, branch, and main file path (`app/main.py`)
   - Click "Deploy"

4. **Configure Secrets** (if needed)
   - In Streamlit Cloud app settings, go to "Secrets"
   - Add environment variables:
     ```
     ADMIN_PASSWORD = "your_secure_password"
     DEBUG = "false"
     ```

5. **Access Your App**
   - Streamlit provides a public URL: `https://your-username-rct-design-activity.streamlit.app`

### Auto-Deploy on Push
- Any push to the configured branch automatically triggers a redeploy
- Takes ~2-3 minutes

### Sharing Workshop
- Share the public URL with participants
- No login required (unless you add authentication)
- Works on all devices

---

## Docker Deployment

### Prerequisites
- Docker (https://www.docker.com/get-started)
- Docker Compose (included with Docker Desktop)

### Local Docker Development

```bash
# Build image
docker build -t rct-design-activity:latest .

# Run container
docker run -p 8501:8501 \
  -e DEBUG=false \
  -e ADMIN_PASSWORD=mypassword \
  rct-design-activity:latest

# Access at http://localhost:8501
```

### Docker Compose (for local multi-container setup)

```bash
docker-compose up
```

Creates containers for:
- Main Streamlit app
- Optional: PostgreSQL for team submissions storage
- Optional: Redis for caching

### Push to Docker Hub

```bash
# Tag image
docker tag rct-design-activity:latest yourusername/rct-design-activity:latest

# Push to registry
docker push yourusername/rct-design-activity:latest
```

### Run from Docker Hub

```bash
docker run -p 8501:8501 yourusername/rct-design-activity:latest
```

---

## AWS Deployment

### Option 1: AWS App Runner (Easiest)

1. **Create Docker Image** (see Docker section)
2. **Push to Amazon ECR**
   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
   docker tag rct-design-activity YOUR_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/rct-design-activity
   docker push YOUR_ACCOUNT_ID.dkr.ecx.REGION.amazonaws.com/rct-design-activity
   ```
3. **Create App Runner Service**
   - AWS Console → App Runner → Create service
   - Select ECR image
   - Configure: Port 8501, CPU/Memory as needed
   - Deploy

### Option 2: ECS Fargate

1. Create ECS cluster
2. Define task definition with Dockerfile
3. Create service with load balancer
4. Configure auto-scaling

See AWS ECS documentation for detailed steps.

### Option 3: EC2 with Nginx

1. Launch EC2 instance (Ubuntu 20.04+)
2. SSH into instance
3. Install Docker and pull image
4. Configure Nginx reverse proxy
5. Use Certbot for SSL

---

## Azure Deployment

### Azure Container Instances (ACI)

1. **Create Azure Container Registry (ACR)**
   ```bash
   az acr create --resource-group myRG --name myRegistry --sku Basic
   ```

2. **Push Image to ACR**
   ```bash
   az acr build --registry myRegistry --image rct-design-activity:latest .
   ```

3. **Deploy to ACI**
   ```bash
   az container create \
     --resource-group myRG \
     --name rct-app \
     --image myRegistry.azurecr.io/rct-design-activity:latest \
     --cpu 1 --memory 1 \
     --port 8501 \
     --registry-login-server myRegistry.azurecr.io \
     --registry-username <username> \
     --registry-password <password>
   ```

### Azure App Service

1. Create App Service Plan
2. Create Web App
3. Configure continuous deployment from GitHub
4. Deploy from `app/main.py`

---

## GCP Deployment

### Cloud Run (Serverless)

1. **Build and Push to Artifact Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/rct-design-activity
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy rct-design-activity \
     --image gcr.io/PROJECT_ID/rct-design-activity \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## Performance Optimization

### For Large Workshop Groups

1. **Enable Caching**
   - Already configured in `.streamlit/config.toml`
   - Caches data generation and program card loading

2. **Use CDN for Static Assets**
   - Serve images from CloudFront (AWS) or Cloudflare

3. **Database for Submissions** (Optional)
   - Store team submissions in PostgreSQL
   - Reduce memory usage
   - Enable data persistence

4. **Load Balancing**
   - For 100+ concurrent users, use load balancer
   - AWS ALB or Azure Load Balancer

---

## Security Considerations

### For Public Workshop

1. **No Authentication (Default)**
   - App is open to everyone
   - Suitable for in-person workshops

2. **With Authentication** (Optional)
   - Use `streamlit-authenticator` package
   - Restrict to registered participants
   - Requires login with username/password or OAuth

### Environment Variables to Secure
- `ADMIN_PASSWORD` – Use Streamlit Secrets (Cloud) or environment variables
- Database credentials – Never commit to Git
- API keys – Store in Secrets manager (AWS Secrets Manager, Azure Key Vault, etc.)

### HTTPS & SSL
- Streamlit Cloud: Automatic
- Docker/Self-hosted: Use Nginx or Apache as reverse proxy with Let's Encrypt

---

## Monitoring & Logging

### Streamlit Cloud
- Built-in app analytics
- View usage stats in dashboard

### Self-Hosted
- Configure logging to CloudWatch (AWS), Application Insights (Azure), or Stackdriver (GCP)
- Example log rotation in Docker container

### Health Checks
- Add `/health` endpoint for load balancer health checks
- Monitor error rates and response times

---

## Backup & Recovery

### Session State
- By default, stored in browser memory
- Doesn't persist across refreshes
- Implement database backup if persistence needed

### Generated Reports
- Store in S3, Azure Blob, or GCS
- Set up automated backups
- Retention policy (e.g., keep for 30 days)

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:** Ensure all dependencies in `requirements.txt` are installed
```bash
pip install -r requirements.txt
```

### Issue: Streamlit app stuck or slow
**Solutions:**
- Increase Streamlit timeout: Edit `.streamlit/config.toml`
- Reduce number of parallel operations
- Use `@st.cache_data` for expensive computations

### Issue: Can't connect to deployed app
**Solutions:**
- Check firewall rules allow port 8501
- Verify app is running: `docker logs <container_id>`
- Check error logs in cloud platform dashboard

### Issue: PDF export fails
**Solution:** Install system dependencies for WeasyPrint:
```bash
# Ubuntu/Debian
apt-get install libffi-dev libcairo2-dev libpango1.0-dev

# macOS
brew install cairo
```

### Issue: Large workshop group → slow app
**Solutions:**
- Deploy multiple instances behind load balancer
- Reduce sample data size
- Cache program card loading
- Pre-generate reports server-side

---

## Scaling for Large Workshops

For 100+ concurrent participants:

1. **Load Balancer Setup**
   - AWS: Application Load Balancer (ALB)
   - Azure: Azure Load Balancer
   - GCP: Cloud Load Balancing

2. **Multiple App Instances**
   - Deploy 3-5 Streamlit app replicas
   - Share session state via database
   - Use Redis for caching

3. **Database Backend**
   - PostgreSQL for team submissions
   - Store design plans in database
   - Enable progress recovery

4. **CDN for Assets**
   - Host images and stylesheets on CDN
   - Reduces server load

Example Kubernetes deployment included in `/scripts` folder.

---

## Support

For deployment issues:
- Check Streamlit documentation: https://docs.streamlit.io
- Open GitHub issue: https://github.com/ajolex/rct-design-activity/issues
- Contact: support@example.com

---

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] `requirements.txt` updated with all dependencies
- [ ] Sample data generated and in `data/sample_data/`
- [ ] `.env` file created with sensitive variables
- [ ] `README.md` updated with app-specific info
- [ ] Deployment platform chosen (Streamlit Cloud recommended)
- [ ] App deployed and tested in target environment
- [ ] URL shared with workshop participants
- [ ] Admin password configured (if applicable)
- [ ] Performance tested with expected participant count
