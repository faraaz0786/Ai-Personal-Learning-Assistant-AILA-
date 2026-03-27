# AILA Deployment Guide (Vercel)

This project is configured for seamless full-stack deployment on Vercel as a monorepo.

## Prerequisites
- GitHub Account
- Vercel Account
- Supabase Project (Postgres)
- Groq API Key (or OpenAI/X.AI)

## Deployment Steps

1. **GitHub Push**
   ```bash
   git add .
   git commit -m "Configure Vercel deployment"
   git push origin main
   ```

2. **Vercel Setup**
   - Connect your GitHub repository to a new Vercel project.
   - Vercel will automatically detect the `vercel.json` configuration.

3. **Environment Variables**
   Add the following variables in **Settings > Environment Variables**:
   - `DATABASE_URL`: Your Supabase connection string.
   - `GROQ_API_KEY`: Your Groq API key.
   - `SECRET_KEY`: A secure random string for session handling.

4. **Build & Deploy**
   - Vercel will build the React frontend and deploy the FastAPI backend as Serverless Functions.
   - Verify health at `https://your-project.vercel.app/api/v1/health`.

## Customizing Backend Port (Local)
For local development, the backend is configured to run on port `8003` to avoid common conflicts. See `.env.example` for details.
