@echo off
echo Starting City News Sentiment Analysis System...
echo Setting environment variables...

:: Set Flask environment variables
set FLASK_APP=city_news_app.py
set FLASK_ENV=development

:: Start the application
echo Starting Flask application...
python -m flask run --host=0.0.0.0 --port=5000

pause 