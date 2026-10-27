# Shree Krishna OTT — Starter Repository

Starter source for a licensed-content OTT app + Telegram bot + basic web admin API.

## Included
- `backend/`: FastAPI API, SQLAlchemy models, SQLite for local development
- `bot/`: Telegram bot using aiogram 3
- `admin/`: tiny web admin page for checking API health (starter)
- `android_app/`: Flutter starter with black/red Shree Krishna branding and bottom navigation
- `.env.example`: configuration template

This is a development starter, **not a deployed or production-ready OTT service**. It does not include a payment gateway, DRM, real offline download manager, full content ingestion pipeline, or production authentication yet. Use only videos you own or have permission to stream.

## 1. Requirements
- Python 3.11+
- Flutter SDK (for Android app)
- A Telegram bot token from BotFather (optional for bot testing)

## 2. Run the backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

The starter uses SQLite locally. For production, configure PostgreSQL and add migrations, authentication, backups, rate limits and monitoring.

## 3. Run the Telegram bot
In the project root, install:
```bash
pip install -r bot/requirements.txt
```
Set `TELEGRAM_BOT_TOKEN` in `.env`, then:
```bash
python -m bot.main
```
The bot uses `BACKEND_URL` (default `http://127.0.0.1:8000`). If the bot runs on another host, set this to the reachable API URL.

## 4. Run the Flutter app
```bash
cd android_app
flutter pub get
flutter run
```
This is a UI scaffold. To use real content, connect the API and integrate a compatible player such as `video_player` with licensed HLS/DASH streams. Do not put secret API keys or bot tokens in the app.

## 5. GitHub
1. Create a new **private** GitHub repository named `shree-krishna-ott`.
2. Extract this ZIP and upload the folder contents, or use:
```bash
git init
git add .
git commit -m "Initial Shree Krishna OTT starter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shree-krishna-ott.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your GitHub username. Do not commit `.env` or secrets.

## Current API routes
- `GET /health`
- `GET /api/content?kind=movie&language=Hindi`
- `POST /api/content` (starter create route; add admin authentication before public deployment)

## Important before public launch
- Add secure admin authentication/roles and protect write routes.
- Use PostgreSQL and database migrations.
- Implement a real payment provider and verify payments server-side.
- Implement secure stream authorization, signed URLs/DRM where required.
- Add privacy policy, content rights checks, abuse prevention and backups.
