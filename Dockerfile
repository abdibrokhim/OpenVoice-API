FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./OpenVoice/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /OpenVoice/requirements.txt

COPY ./OpenVoice /app