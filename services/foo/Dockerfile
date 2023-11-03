FROM python
WORKDIR /code
ENV FLASK_APP=foo.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && pip3 uninstall urllib3 -y  \
    && pip3 install --no-cache-dir -U urllib3
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
