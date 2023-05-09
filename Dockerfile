FROM  python:3.9.16-alpine3.17

LABEL author.name="Uere, Edilson Junior" 
LABEL author.e-mail="ueremizera@gmail.com"
LABEL version="0.0.1"
LABEL description="I need one container with connect on s3 and dele all archives with more X days"

COPY /app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod 644 s3-rotation.py
ENTRYPOINT ["python3"]
CMD ["s3-rotation.py"]