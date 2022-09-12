from xml.dom.minidom import Element
from bs4 import BeautifulSoup
import requests
from lxml import etree
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException


date = datetime.datetime.now()
driver = webdriver.Firefox(executable_path="/path/to/geckodriver")



month =  str(date.month)
prev_month = str(date.month)
day = str(date.day)
prev_day = str(date.day - 1)
year = str(date.year)



if(date.day == 1):
    if(date.month > 1):
        prev_month = str(date.month - 1)
    else:
        prev_month = "12"
    if(date.month - 1 < 10 and date.month != 1):
        prev_month = "0" + prev_month 

if(date.month < 10):
    month = "0" + month

if(date.day < 10 and date.day != 1):
    day = "0" + day
    prev_day = "0" + prev_day



print(year, month, day, prev_day)

URL = "https://www.sec.gov/edgar/search/#/dateRange=custom&category=custom&startdt="+year+"-"+month+"-"+prev_day+"&enddt="+year+"-"+month+"-"+day+"&forms=D"

driver.get(URL)

# run search
search_bar = driver.find_element("xpath", '//*[@id="search"]')
time.sleep(2)
search_bar.click()
time.sleep(2)

next_button = driver.find_element("xpath", '//*[@id="results-pagination"]/ul/li[12]')

pages = driver.find_elements(By.CLASS_NAME, 'page-item')
for page in pages:
    if page.text == "" or page.text == None:
        pages.remove(page)


print([page.text for page in pages])


def send_results(results):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSdgj2e_3qUZG1iQTj4Vj2PxOKe7-vv1ch-hKJAN3n4wZ3Fjrw/viewform")
    name = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    name.click()
    name.send_keys(results['business_name'])
    
    key_players = driver.find_element("xpath", '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/textarea')
    key_players.click()
    key_players.send_keys(results['names'])

    linkedins = driver.find_element("xpath", '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    linkedins.click()
    linkedins.send_keys(results['linkedins'])

    amount = driver.find_element("xpath", '/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    amount.click()
    amount.send_keys(results['amount'])

    submit = driver.find_element('xpath', "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div")
    submit.click()



   



def scrape_all(page_source):
    # get page source with all entries
    
    with open("source.html", "w") as f:
        f.write(page_source)

    source = open("source.html")

    soup = BeautifulSoup(source, "html.parser")
    
    res_table = soup.find_all("td", {"class": "file-num d-none"})
    for entry in res_table:
        a = entry.find("a", href=True)
        link = a['href']
        driver.get(link)
        time.sleep(1)
        documents_button = driver.find_element("xpath", '//*[@id="documentsbutton"]')
        documents_button.click()
        time.sleep(1)
        primary_doc = driver.find_element("xpath", '//*[@id="formDiv"]/div/table/tbody/tr[2]/td[3]/a')
        primary_doc.click()
        time.sleep(1)
        filing_source = driver.page_source
        with open('filing.html', 'w') as f:
            f.write(filing_source)
        find_filing_details()
    
    source.close()



def find_filing_details():
    results = {}
    filing = open("filing.html")
    filing_soup = BeautifulSoup(filing)

    # make sure company is a corporation
    table = filing_soup.find("table", {"summary": "Table with Multiple boxes"})
    tds = table.find_all("td", {"class": "CheckBox"})
    span = tds[0].find("span")
    if span == None:
        print("not a corporation.")
        return None
    
    # check that type of financing is is equity
    type_table = filing_soup.find("table", {"summary": "Types of Securities Offered"})
    type_tds = type_table.find_all("td", {"class": "CheckBox"})
    type_span = type_tds[0].find("span")
    if type_span == None:
        print("not an equity financing")
        return None
    
    # make sure that financing is not for a merger/acquisition
    merger_table = filing_soup.find("table", {"summary": "Business Combination Transaction"})
    merger_tds = merger_table.find_all("td", {"class": "CheckBox"})
    merger_span = merger_tds[0].find("span")
    if merger_span != None:
        print("financing is for an m&a transaction")
        return None
    
    # check that filing is a new notice 
    filing_type_table = filing_soup.find("table", {"summary": "Type of Filing"})
    filing_type_tds = filing_type_table.find_all("td", {"class": "CheckBox"})
    filing_type_span = filing_type_tds[0].find("span")
    if filing_type_span == None:
        print("not a new notice.")
        return None

    print("this is a valid company!")

    # check that offering is between 100k and 3 million
    amount_table = filing_soup.find("table", {"summary": "Offering and Sales Amounts"})
    amount_tds = amount_table.find("td", {"align": "right"})
    amount = amount_tds.find("span", {"class":"FormData"}).text
    amount = int(amount.replace(",", ""))
    if(amount < 100000):
        print("too low.")
        return None
    elif(amount > 3000000):
        print("too high.")
        return None
    
    results['amount'] = amount

    print(amount)

    # get name of company
    business_table = filing_soup.find("table", {"summary": "Principal Place of Business and Contact Information"})
    business_td = business_table.find("td", {"class": "FormData"})
    business_name = business_td.text

    results['business_name'] = business_name

    print(business_name)
    # find table summary = Principal Place of Business and Contact Information
    # find first td class="FormData"
    

    # get founder/ceo names
    people = filing_soup.find_all("table", {"summary": "Related Persons"})
    names = []
    names_list = ""
    linkedins = []
    linkedins_list = ""
    for table in people:
        trs = table.find_all("tr")
        tds = trs[1].find_all("td", {"class": "FormData"})
        
        names = []

        for td in tds:
            name_part = td.text
            names.insert(0, name_part)
        
        if len(names) == 3:
            full_name = names[2] + " " + names[0] + " " + names[1]

        else:
            full_name = names[0] + " " + names[1]
        
        linkedins.append("https://www.linkedin.com/search/results/all/?keywords="+names[0]+"%20"+names[1]+"&origin=GLOBAL_SEARCH_HEADER&sid=sT8")
        
        names_list += full_name + ", "
        print(full_name)
    
    for linkedin in linkedins:
        linkedins_list += linkedin + ", "
        print(linkedin)

    
    results['names'] = names_list
    results["linkedins"] = linkedins_list

    print(results)

    send_results(results)

    # get year of incorporation

    # get investor names (if applicable) and attempt to find linkedin

sources = []
total_pages = len(pages)-3
for i in range(len(pages)-3):
    
    time.sleep(1)
    page_source = driver.page_source
    
    print("page_source", i)
    sources.append(page_source)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_button.click()    
    except(ElementNotInteractableException):
        break

for page_source in sources:
    scrape_all(page_source)





