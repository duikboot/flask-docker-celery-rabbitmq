FROM python:3.7.2

RUN pip install pipenv

ADD . /flask-deploy

WORKDIR /flask-deploy

RUN pipenv install --system --skip-lock

RUN pip install gunicorn[gevent]
RUN pip install flower

EXPOSE 8000

# CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:8000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info

CMD python app.py
