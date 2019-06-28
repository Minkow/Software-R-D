FROM python:3.7

ADD ./Software-R-D /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python", "/code/KBMS.py"]
