# Telegram bot
__________________________________________________________________
This is a bot which allows to upload photos with their links to download and uses OpenAI to analyze user's answers.Try the bot :point_right: [try](https://t.me/tour_agency_eon_bot).
## Requirements
__________________________________________________________________
- aiogram==2.25
- openai==1.10.0
- pydantic-settings==2.1.0
- python-dotenv==1.0.1

To install requirements run
```bash
pip install -r requirements.txt
```
## How to start
__________________________________________________________________
Firstly, clone project:
```bash
git clone https://github.com/VitaliiFedin/Telegram_bot.git
```
Create a Virtual Environment
```bash
python -m venv venv
```
Then activate it
```bash
venv/Scripts/activate
```
For Linux
```bash
source venv/bin/activate
```
To start application you need to create .env file with variables (examples in .env.sample). Then run command
```bash
python bot.py
```
## Docker
__________________________________________________________________
To start project in docker run
```bash
docker-compose up --build -d
```
- --build to rebuild image
- -d detach mode
