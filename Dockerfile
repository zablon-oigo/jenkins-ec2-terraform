FROM python:3.10-slim-bullseye

WORKDIR /sns

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

COPY ./requirements.txt  .
RUN pip install -r requirements.txt
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /sns/entrypoint.sh
RUN chmod +x /sns/entrypoint.sh
COPY . .
ENTRYPOINT ["/sns/entrypoint.sh"]