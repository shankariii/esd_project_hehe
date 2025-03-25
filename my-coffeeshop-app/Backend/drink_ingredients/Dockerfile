FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./drink_ingredients.py .
CMD [ "python", "./drink_ingredients.py" ]