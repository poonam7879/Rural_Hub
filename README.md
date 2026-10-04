# Rural Hub

Rural Hub is a digital platform connecting rural users, scrap dealers, and local service providers. It facilitates transparent scrap bidding, local service booking, and a cashless barter exchange.

## Features
- **Scrap Bidding**: List scrap, accept bids from verified dealers.
- **Service Booking**: Find and book local services (tractor repair, plumbing, etc.).
- **Barter Marketplace**: Exchange goods and services directly with neighbors.
- **Role-based Dashboards**: Custom views for users, dealers, service providers, and admins.

## Tech Stack
- **Backend**: Python Flask, SQLAlchemy
- **Database**: PostgreSQL
- **Frontend**: HTML5, Vanilla CSS, Jinja2
- **Image Storage**: Cloudinary (Vercel-compatible)
- **Deployment**: Vercel

---

## Local Development Setup

1. **Clone the repository** and navigate to the project directory:
   ```bash
   cd rural_hub
   ```

2. **Create a virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   Copy the `.env.example` file to a new file named `.env` and fill in the values:
   ```bash
   cp .env.example .env
   ```
   **Required Variables**:
   - `SECRET_KEY`: A strong random string.
   - `DATABASE_URL`: Your local or remote PostgreSQL database URL. (e.g. `postgresql://user:password@localhost/rural_hub`)
   - `CLOUDINARY_URL`: Your Cloudinary API URL (required for image uploads).

4. **Initialize the Database**:
   Run the Flask-Migrate commands to create the tables.
   ```bash
   flask --app run.py db init
   flask --app run.py db migrate -m "Initial migration"
   flask --app run.py db upgrade
   ```

5. **Run the Application**:
   ```bash
   python run.py
   ```
   The app will be accessible at `http://127.0.0.1:5000/`.

---

## Vercel Deployment Guide

This project is specifically architected to be 100% compatible with Vercel's serverless environment.

### Deployment Checklist

- [x] **No Local SQLite**: Uses PostgreSQL via `DATABASE_URL`.
- [x] **No Local File Storage**: Uses Cloudinary for persistent image uploads via `CLOUDINARY_URL`.
- [x] **No Hardcoded Secrets**: Uses Environment Variables.
- [x] **Serverless Entry Point**: `run.py` is configured in `vercel.json` to expose the Flask app to the `@vercel/python` builder.
- [x] **requirements.txt**: Contains all production dependencies (`psycopg2-binary`, `Flask`, etc.).

### Steps to Deploy on Vercel

1. **Push your code to GitHub**.
2. **Create a new project** on Vercel and import your repository.
3. **Configure Environment Variables** in the Vercel dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL` (From Supabase, Neon, or another managed Postgres provider. Make sure it uses `postgresql://`).
   - `CLOUDINARY_URL`
4. **Build and Deploy**: Vercel will automatically read `vercel.json` and build the Python runtime.
5. **Run Migrations in Production**:
   Since Vercel is serverless, you cannot easily run `flask db upgrade` from the Vercel dashboard. 
   **Solution**: Run the upgrade command locally, but point your local `.env` to the production `DATABASE_URL`.
   ```bash
   set DATABASE_URL="your-production-database-url"
   flask --app run.py db upgrade
   ```
   *Note: If your database requires SSL, you may need to append `?sslmode=require` to the URL.*

6. Your application is now live!
