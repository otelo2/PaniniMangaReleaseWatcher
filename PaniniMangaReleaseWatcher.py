#!/usr/bin/env python
import re
import json
import urllib.request
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from gmailSecrets import gmailSender, gmailPassword

def getMangasToWatchFromFile():
    """ Reads the mangas.json file to get the mangas to track.
    """
    with open('mangas.json') as json_file:
        data = json.load(json_file)
        for manga in data['mangas']:
            print('Name: ' + manga['name'])
            print('Items: ' + str(manga['items']))
        return data

def getWebsiteContents(mangaName):
    """ Gets the search website for the manga.
    """
    try:
        urlMangaName = mangaName.replace(" ", "+")
        with urllib.request.urlopen(f'https://tiendapanini.com.mx/catalogsearch/result/?q={urlMangaName}') as f:
            html = f.read().decode('utf-8')
            return html
    except urllib.error.URLError as e:
        print(e.reason)
        
def extractMangaInformationFromHTML(websiteContent):
    pattern = r'<div class="product details product-item-details "[^>]*>.*?product-image-container'

    # Extract the desired section using the pattern
    match = re.search(pattern, websiteContent, re.DOTALL)

    if match:
        extracted_section = match.group()
        return extracted_section
    else:
        print("No match found.")
        return None

def getAmountOfItems(websiteContent):
    """ Matches a regex against the search website to find the current items that were returned for the search.
    """
    # Regex: <span class="toolbar-number">(\d+)</span>
    regex = r"<span class=\"toolbar-number\">(\d+)</span>"
    match = re.search(regex, websiteContent)
    
    if match:
        print("Match found: " + match.group(1))
        return match.group(1)
    else :
        print("No match")
        return None

def thereIsNewRelease(amountOfPreviousItems, amountOfCurrentItems):
    """ Compares if the current items in the website is grater than the previous number of items.
    """
    if int(amountOfCurrentItems) > int(amountOfPreviousItems):
        print("New release!")
        return True
    else:
        print(f"No new release")
        return False

def sendEmail(mangaName, amountOfPreviousItems, amountOfCurrentItems, recipient):
    """ Sends an email if there is a new release for the manga.
    """
    subject = f"Nuevo lanzamiento de: {mangaName}"
    body = f"Se detectó un nuevo lanzamiento de: {mangaName}.\n\n" \
           f"Había {amountOfPreviousItems} artículos y ahora hay {amountOfCurrentItems} artículos.\n\n" \
           f"Link: https://tiendapanini.com.mx/catalogsearch/result/?q={mangaName.replace(' ', '+')}"
    sender = gmailSender
    recipients = [recipient, gmailSender]
    password = gmailPassword
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipients, msg.as_string())
    print("Email sent!")
    
def sendEmailWithHTML(mangaName, amountOfPreviousItems, amountOfCurrentItems, HTML):
    """ Sends an email if there is a new release for the manga.
    """
    subject = f"Nuevo lanzamiento de: {mangaName}"
    body = f"Se detectó un nuevo lanzamiento de: {mangaName}.\n\n" \
           f"Había {amountOfPreviousItems} artículos y ahora hay {amountOfCurrentItems} artículos.\n\n" \
           f"Link: https://tiendapanini.com.mx/catalogsearch/result/?q={mangaName.replace(' ', '+')}"
    sender = gmailSender
    recipients = ["hello+tests@antoniosolismz.com", gmailSender]
    password = gmailPassword
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    
    text_part = MIMEText(body, 'plain')
    msg.attach(text_part)
    
    html_part = MIMEText(HTML, 'html')
    msg.attach(html_part)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recipients, msg.as_string())
    print("Email sent!")
    
def updateMangasJSON(mangasJSON):
    with open('mangas.json', 'w') as outfile:
        json.dump(mangasJSON, outfile)


def main(recipient):
    mangasJSON = getMangasToWatchFromFile()
    for manga in mangasJSON['mangas']:
        print(f"Checking {manga['name']}...")
        print("Getting website contents...")
        html = getWebsiteContents(manga['name'])
        print("Getting amount of items...")
        currentItemsAmount = getAmountOfItems(html)
        if thereIsNewRelease(manga['items'], currentItemsAmount):
            print("Sending email...")
            #mangaInfoHTML = extractMangaInformationFromHTML(html)
            sendEmail(manga['name'], manga['items'], currentItemsAmount, recipient)
            manga['items'] = int(currentItemsAmount)
        else:
            print(f"No new release for {manga['name']}")
    
    updateMangasJSON(mangasJSON)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Program to watch the new releases of Panini Manga. Emails the recipient if there is a new release.')
    parser.add_argument('emailRecipient', type=str, help='Email to send the notification to')
    args = parser.parse_args()
    recipient = args.emailRecipient

    main(recipient)
