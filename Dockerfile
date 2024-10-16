FROM python:3.6
RUN mkdir /usr/src/app/
COPY ./api/ /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python", "app.py"]