FROM python

WORKDIR /merelyasite

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . /merelyasite

CMD ["python", "app.py"]

