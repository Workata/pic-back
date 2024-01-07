FROM python:3.12.1-alpine3.19

# * install needed libs
COPY requirements/base.txt requirements/base.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements/base.txt

COPY ./src ./src
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
