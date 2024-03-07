# app/Dockerfile

# FROM python:3.9-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/streamlit/streamlit-example.git .

# RUN pip3 install -r requirements.txt

# EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


FROM python:3.10

WORKDIR /app

RUN echo "work directory 1" > delete1.txt

COPY frosty_app_mine.py   .
COPY promptsmine.py .
COPY .streamlit/secrets.toml ./.streamlit/secrets.toml

RUN pip3 install streamlit altair pandas openai snowflake-snowpark-python

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "frosty_app_mine.py", "--server.port=8501", "--server.address=0.0.0.0"]