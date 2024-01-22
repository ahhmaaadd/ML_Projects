import time
from email.message import EmailMessage
import sqlite3
import requests  # requests library takes source code of website and stores it in python as a string
import selectorlib
import os
import smtplib, ssl

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("events.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    """Extract the exact information from the Soruce Code"""
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tour"]
    return value


def send_email():
    host = "smtp.gmail.com"
    port = 465

    email_message = EmailMessage()
    email_message["Subject"] = "New Event"
    email_message.set_content("Hey, we just found a new event!")


    username = "muhammadahmed181@gmail.com"
    password = "%%%"
    reciever = "muhammadahmed181@gmail.com"

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, reciever, email_message.as_string())
    print("Email was sent")


def store(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()



def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows




if __name__ == "__main__":
    while True:
        scrapped = scrape(URL)
        extracted = extract(scrapped)
        print(extracted)


        if extracted != "No upcoming tours":
            row = read(extracted)
            if not row:
                store(extracted)
                send_email()
        time.sleep(2)
