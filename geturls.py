from bs4 import BeautifulSoup
import requests, time
import pandas as pd
import json

import random

def get_headers():
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    user_agent = random.choice(user_agent_list)

    #Set the headers
    headers = {'User-Agent': user_agent}
    return headers


#brand = input("Enter Technology:  ")
#pages = int(input("Number of pages: "))
brand = "Journal of Marine Systems"
pages = 100
url = "https://scholar.google.com/scholar?start={}&q={}+technology&hl=en&as_sdt=0,5"

data = []
for i in range(0,pages*10+1,10):
    print(url.format(i, brand))
    headers = get_headers()
    print("Going to hit %s" % url.format(i, brand))
    res = requests.get(url.format(i, brand),headers=headers)
    if res.status_code != 200:
        print(res.status_code,res.text)
    else:
        print(res.status_code,res.text)
    main_soup = BeautifulSoup(res.text, "html.parser")
    divs = main_soup.find_all("div", class_="gs_r gs_or gs_scl")
    for div in divs:
        temp = {}
        h3 = div.find("h3", class_="gs_rt")
        temp["Link"] = h3.find("a")["href"]
        temp["Heading"] = h3.find("a").get_text(strip=True)
        temp["Authors"] = div.find("div",class_="gs_a").get_text(strip=True)
        print(temp["Link"])
        try:
            res_link = requests.get(temp["Link"], headers=headers)
            soup_link = BeautifulSoup(res_link.text,"html.parser")
            if "sciencedirect" in temp["Link"]:
                temp["Abstract"] = soup_link.find("div", class_="abstract author").find("div").get_text(strip=True)
            elif "acm" in temp["Link"]:
                temp["Abstract"] = soup_link.find("div", class_="abstractSection abstractInFull").get_text(strip=True)
        except: pass

        if isinstance(temp, dict):
            if temp not in data:
                data.append(temp)
        else:
            print(f"The {temp} is not a dictionary.")
        print(data)
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        time.sleep(random.randint(90, 180))
    time.sleep(random.randint(900, 1200))


pd.DataFrame(data).to_csv("data.csv", index=False)
