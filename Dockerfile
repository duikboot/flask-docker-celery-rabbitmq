FROM python:3.9

RUN pip install pipenv

ADD . /flask-deploy

WORKDIR /flask-deploy

RUN pipenv install --system --skip-lock

RUN pip install gunicorn[gevent]
# RUN pip install flower

EXPOSE 8000

CMD python app.py
