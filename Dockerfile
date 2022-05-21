FROM python

WORKDIR /merelyasite

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python3 app.py
