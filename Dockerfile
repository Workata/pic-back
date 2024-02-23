FROM python:3.12.2-bookworm

# * install needed libs
COPY requirements/ requirements/
RUN pip install --upgrade pip
RUN pip3 install -r requirements/prod.txt

COPY ./src ./src
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--reload", "--host=0.0.0.0", "--port=8000"]
