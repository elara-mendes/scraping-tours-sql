import requests, selectorlib
import smtplib, ssl, os
import time


YOUR_EMAIL = "elaradomingos@gmail.com"
APP_PASSWORD = os.getenv("GMAIL_PASSWORD")

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def store(extracted_text):
    with open("extract.txt", "a") as file:
        file.write(extracted_text + "\n")

def read_file(extracted_text):
    with open("extract.txt", "r") as file:
        return file.read()

def email_send(message):
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
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        content = read_file(extracted)
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                email_send(extracted)
        print(extracted)
        time.sleep(2)