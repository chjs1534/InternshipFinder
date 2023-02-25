from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os, csv, json, time, re, sys

def writeToCSV(postings):
    with open('Internships.csv', 'w') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=list(postings[0].keys()))
        writer.writeheader()
        writer.writerows(postings)

def filterInternships(role):
    return re.search("intern", role, re.IGNORECASE)

def postingObj(jobPosting):
    company = jobPosting.find('h4', class_='base-search-card__subtitle').a.text
    role = jobPosting.find('h3', class_='base-search-card__title').text
    
    if not filterInternships(role):
        return None
    
    location = jobPosting.find('span', class_='job-search-card__location').text
    postingLink = jobPosting.div.a['href']

    posting = {
        "company" : company.strip(),
        "role" : role.strip(),
        "location" : location.strip(),
        "postingLink" : postingLink
    }

    return posting

def getCurrentStore():
    store = {}
    d = {}
    if (os.stat('posts/jobs.json').st_size != 0):
        with open('posts/jobs.json', 'r') as f:
            store = json.load(f)
        
        for obj in store['postings']:
            d.update({obj['company'] + obj['role']: 1})
    else:
        store = {'postings': []}
    
    return d, store

def saveJSONObjects(soup):
    jobSearchList = soup.find('ul', class_='jobs-search__results-list')
    jobPostings = jobSearchList.find_all('li')

    d, store = getCurrentStore()

    for jobPosting in jobPostings:
        posting = postingObj(jobPosting)
        if not posting:
            continue
        
        key = posting['company'] + " " +posting['role']
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

def doOutputFile():
    _, store = getCurrentStore()
    if (store['postings'] != []):
        writeToCSV(store['postings'])

if __name__ == "__main__":
    action = input("Enter 1 for scrape data only, 2 for output file only, 3 for both\n")

    if action == '1':
        doWebScrape()
    elif action == '2': 
        doOutputFile()
    elif action == '3':
        doWebScrape()
        doOutputFile()