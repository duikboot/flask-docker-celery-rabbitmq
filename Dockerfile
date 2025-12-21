FROM python:3.13.9-bookworm


RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /flask-deploy

WORKDIR /flask-deploy

RUN pipenv install --system --skip-lock

RUN pip install gunicorn[gevent]
# RUN pip install flower

EXPOSE 8888

CMD [ "python",  "app.py" ]
