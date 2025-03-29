FROM python:3-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy login.py and Firebase credentials
COPY ./login.py ./
COPY ./esd-coffeehouse-firebase-adminsdk-fbsvc-8fcd8a05cd.json ./

CMD ["python", "./login.py"]
