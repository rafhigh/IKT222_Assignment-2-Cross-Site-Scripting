FROM python:3.10-slim
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/rafhigh/IKT222_Assignment-2-Cross-Site-Scripting.git
WORKDIR /IKT222_Assignment-2-Cross-Site-Scripting
RUN pip install Flask && pip install Jinja2==2.11.3 && pip install itsdangerous==2.0.1 && pip install Flask-WTF && pip install Flask-SQLAlchemy && pip install Flask-Login && pip install Flask-Migrate
EXPOSE 5000
CMD ["python", "app.py"]
