#!/usr/local/bin/python3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from mylinks import my_links
import time
import random

def get_articile(url):
    try:
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        chrome_options.add_argument("--headless")

        # Create a new instance of the Chrome driver
        browser = webdriver.Chrome(options=chrome_options)


        # Navigate to the page
        browser.get(url)

        # Get HTML source
        html = browser.page_source
        # Close the browser
        browser.quit()

        soup = BeautifulSoup(html, 'html.parser')

       # paragraphs = soup.find_all('p')
       # for paragraph in paragraphs:
       #     print(paragraph.get_text())

        abstract_div = soup.find('div', class_='abstract author')

        # Find the paragraph within this div
        abstract_paragraph = abstract_div.find('p') if abstract_div else None

        # Extract and print the text if the paragraph is found
        #if abstract_paragraph:
        #    print(abstract_paragraph.get_text())
        #else:
        #    print("Abstract paragraph not found")

        # Find the Journal name  within this div
        journal_name_div = soup.find('div', class_='publication-volume')

        journal_name = journal_name_div.find('span') if journal_name_div else None

        # Extract and print the text if the Journal name is found
        #if journal_name:
        #    print(journal_name.get_text())
        #else:
        #    print("Journal name not found")

        if abstract_paragraph and journal_name:
            result = {}
            result[journal_name.get_text()] = abstract_paragraph.get_text()
            return result

    except Exception as e:
        print(e)


def main():
    mydata = []

    # This is just an example but you can fee the func my_articile in a loop
    #url = 'https://www.sciencedirect.com/science/article/pii/S138511019700052X'
    for url in my_links:
        my_articile = get_articile(url)

        # Add / append article only if the data is dict type and not exist in the list
        if isinstance(my_articile, dict):
            if my_articile not in mydata:
                mydata.append(my_articile)
                print(my_articile)
        else:
            print(f"The {my_articile} is not a dictionary.")
        time.sleep(random.randint(300, 600))

    # print all the articles
    for i in mydata:
        print(i)

    with open('result.txt', 'w') as file:
        file.write(mydata)

if __name__ == "__main__":
    main()
