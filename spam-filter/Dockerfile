FROM python:3.10
COPY .. .
RUN mkdir /files
ENV PYTHONPATH "${PYTHONPATH}:/osd"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt