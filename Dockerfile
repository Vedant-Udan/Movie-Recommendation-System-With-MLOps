FROM python:3.10-bullseye


WORKDIR /app

COPY deployment/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5003 5000

RUN export PYTHONPATH="$PYTHONPATH:$(pwd)/"

CMD ["sh", "-c", "python src/model.py && python deployment/app.py"]