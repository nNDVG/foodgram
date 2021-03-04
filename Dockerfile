FROM python:3.8.5
WORKDIR /code
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x /code/entrypoint.sh
ENTRYPOINT ['/code/entrypoint.sh']