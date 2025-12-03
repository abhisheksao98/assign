# Deployment Guide

This guide covers deploying the Mobile Shopping Chat Agent to various platforms.

## Prerequisites

- A Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))
- A GitHub account (for most deployment platforms)
- Your code pushed to a GitHub repository

## Platform-Specific Instructions

### Render.com (Recommended - Easiest)

1. **Sign up** at [render.com](https://render.com) (free tier available)

2. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository and branch

3. **Configure the service**:
   - **Name**: mobile-shopping-agent (or any name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variable**:
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key

5. **Deploy**: Click "Create Web Service"

6. **Access**: Your app will be available at `https://your-app-name.onrender.com`

**Note**: Free tier on Render spins down after inactivity. First request may take 30-60 seconds.

### Railway.app

1. **Sign up** at [railway.app](https://railway.app)

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variable**:
   - Go to "Variables" tab
   - Add `GEMINI_API_KEY` with your API key value

4. **Deploy**: Railway auto-detects Python and deploys automatically

5. **Access**: Railway provides a URL like `https://your-app.up.railway.app`

### Vercel (Serverless)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Add Environment Variable**:
   - Go to Vercel dashboard
   - Select your project
   - Go to Settings → Environment Variables
   - Add `GEMINI_API_KEY`

5. **Redeploy**: Changes take effect after redeployment

**Note**: Vercel uses serverless functions. The `vercel.json` file is already configured.

### Heroku

1. **Install Heroku CLI** and login

2. **Create app**:
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variable**:
   ```bash
   heroku config:set GEMINI_API_KEY=your_key_here
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

### PythonAnywhere

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload files** via Files tab

3. **Create web app**:
   - Go to Web tab
   - Click "Add a new web app"
   - Choose Flask (we'll modify it)
   - Point to your `main.py`

4. **Set environment variable** in Web app configuration

5. **Reload** the web app

## Environment Variables

All platforms require the `GEMINI_API_KEY` environment variable:

```
GEMINI_API_KEY=your_actual_api_key_here
```

## Post-Deployment Checklist

- [ ] Test the health endpoint: `https://your-app.com/api/health`
- [ ] Test a chat query: "Best phone under 30000"
- [ ] Verify static files load (CSS, JS)
- [ ] Test adversarial prompts (should be handled gracefully)
- [ ] Check mobile responsiveness

## Troubleshooting

### App won't start
- Check logs for errors
- Verify `GEMINI_API_KEY` is set correctly
- Ensure all dependencies are in `requirements.txt`

### Static files not loading
- Verify `static/` directory is included in deployment
- Check file paths in HTML (should start with `/static/`)

### Database errors
- SQLite database is created automatically
- On some platforms, you may need to use a persistent volume
- Consider migrating to PostgreSQL for production

### API rate limits
- Free Gemini API has rate limits
- Implement caching for production
- Consider upgrading API tier

## Production Considerations

1. **Database**: Migrate from SQLite to PostgreSQL for production
2. **Caching**: Add Redis for response caching
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Monitoring**: Add logging and error tracking (Sentry, etc.)
5. **SSL**: Ensure HTTPS is enabled
6. **Environment**: Use separate API keys for dev/staging/prod

## Cost Estimates

- **Render Free Tier**: Free (with limitations)
- **Railway Free Tier**: $5/month credit
- **Vercel Free Tier**: Free (generous limits)
- **Google Gemini API**: Free tier available, pay-as-you-go after

Most deployments can run entirely on free tiers for development/testing.

