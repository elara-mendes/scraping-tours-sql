import requests, selectorlib
import smtplib, ssl, os
import time
import sqlite3


YOUR_EMAIL = "elaradomingos@gmail.com"
APP_PASSWORD = os.getenv("GMAIL_PASSWORD")


URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class Event:
    def scrape(self, url):
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value

class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def store(self, extracted_text):
        row = extracted_text.split(",")
        new_row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", new_row)
        self.connection.commit()

    def read_file(self, extracted_text):
        row = extracted_text.split(",")
        new_row = [item.strip() for item in row]
        band, city, date = new_row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND date=? AND city=?", (band, date, city))
        rows = cursor.fetchall()
        print(rows)
        return rows

class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        user_name = YOUR_EMAIL
        password = APP_PASSWORD
        receiver = YOUR_EMAIL

        context = ssl.create_default_context()

        message = f"Subject: New Event\n\n{message}"

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user_name, password)
            server.sendmail(user_name, receiver, message.encode("utf-8"))

        print("Email sent!")

if __name__ == '__main__':
    event = Event()
    while True:
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)

        database = Database(db_path='data.db')
        email = Email()
        if extracted != "No upcoming tours":
            line = database.read_file(extracted)
            if not line:
                database.store(extracted)
                email.send(extracted)
        print(extracted)
        time.sleep(2)