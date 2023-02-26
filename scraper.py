from bs4 import BeautifulSoup
import time, json, re
from helpers import getCurrentStore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def filterInternships(role):
    return re.search("intern", role, re.IGNORECASE)

def postingObj(jobPosting):
    # create posting
    companyElement = jobPosting.find('h4', class_='base-search-card__subtitle')
    roleElement = jobPosting.find('h3', class_='base-search-card__title')
    locationElement = jobPosting.find('span', class_='job-search-card__location')
    postingLinkElement = jobPosting.div
    
    if not companyElement or not roleElement or not locationElement or\
        not filterInternships(roleElement.text):
        return None

    posting = {
        "company" : companyElement.a.text.strip(),
        "role" : roleElement.text.strip(),
        "location" : locationElement.text.strip(),
        "postingLink" : postingLinkElement.a['href']
    }

    return posting

def saveJSONObjects(soup):
    # save as json object to file
    jobSearchList = soup.find('ul', class_='jobs-search__results-list')
    jobPostings = jobSearchList.find_all('li')

    d, store = getCurrentStore()

    for jobPosting in jobPostings:
        posting = postingObj(jobPosting)
        if not posting:
            continue
        
        key = posting['company'] + " " + posting['role']
        if not key in d:
            store['postings'].append(posting)

        with open('posts/jobs.json', 'w') as f:
            f.write(json.dumps(store, indent=4))

def scroll():
    browser = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'))
    browser.get('https://au.linkedin.com/jobs/search?keywords=Computer%20Science&location=Sydney%2C%20New%20South%20Wales%2C%20Australia&geoId=104769905&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')
    
    # scroll
    prevHeight = browser.execute_script('return document.body.scrollHeight')
    while True:
        browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(1)
        currHeight = browser.execute_script('return document.body.scrollHeight')
        if currHeight == prevHeight:
            # scroll end
            break
        prevHeight = currHeight

    # press 'see more jobs button'
    for _ in range(20):
        time.sleep(1)
        try:
            seeMore = browser.find_element(By.CLASS_NAME, 'infinite-scroller__show-more-button')
            seeMore.click()
        except:
            break

    return browser

def doWebScrape():
    browser = scroll()
    soup = BeautifulSoup(browser.page_source, 'lxml')
    saveJSONObjects(soup)
    browser.close()