# This is a simple Amazon price tracker, it uses webscraping to keep track of the price of a product in a given Amazon
# URL and alerts you when the price has dropped below your chosen threshold

import requests
from bs4 import BeautifulSoup
import smtplib
import os

Gmail_User = os.environ["My_Email"]
Gmail_Pass = os.environ["My_Pass"]
Receiver_Email = os.environ["Receiver_Email"]
Threshold_Price = int(input("What price would you consider buying the product at?: "))


# Paste the Amazon URL of the product you want to watch below
URL = "https://www.amazon.com/XFX-Speedster-MERC310-Graphics-RX-79XMERCB9/dp/B0BNLSW23M/ref=sr_1_2?crid=3ITL2NO2WBI7I&keywords=radeon+7900+xtx&qid=1674071161&sprefix=radeon+7900+xtx%2Caps%2C120&sr=8-2"

# Paste your headers below. You can find your headers here by pasting this link into your browser; http://myhttpheader.com/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


response = requests.get(url=URL, headers=HEADERS)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

price = int(soup.find("span", class_="a-price-whole").getText().replace(",", "").replace(".", ""))
print(price)
product = soup.find('span', id='productTitle').getText()
print(product)

if price < Threshold_Price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=Gmail_User, password=Gmail_Pass)
        connection.sendmail(
            from_addr=Gmail_User,
            to_addrs=Receiver_Email,
            msg=f"Subject: Price Drop On {product}!!!\n\n The {product}'s price has dropped below ${Threshold_Price},"
                f"consider buying it now."
        )
