FROM python:3.11.0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy
COPY . .
RUN chmod +x microservice_entrypoint.sh
EXPOSE 7000
CMD ./microservice_entrypoint.sh
