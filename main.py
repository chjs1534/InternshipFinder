from bs4 import BeautifulSoup
import requests

source = requests.get('https://au.linkedin.com/jobs/search?keywords=Computer%20Science&location=Sydney%2C%20New%20South%20Wales%2C%20Australia&geoId=104769905&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')
soup = BeautifulSoup(source.text, 'lxml')

jobSearchList = soup.find('ul', class_='jobs-search__results-list')
jobPostings = jobSearchList.find_all('li')

for jobPosting in jobPostings:
    company = jobPosting.find('h4', class_='base-search-card__subtitle').a.text
    role = jobPosting.find('h3', class_='base-search-card__title').text
    location = jobPosting.find('span', class_='job-search-card__location').text
    postingLink = jobPosting.div.a['href']

    # child = requests.get(postingLink)
    # furtherInfoPage = BeautifulSoup(child.text, 'lxml')
    # description = furtherInfoPage.find('div', 
    #     class_='show-more-less-html__markup').text

    with open('posts/jobs.txt', 'w') as f:
        f.write(f'company: {company.strip()}')
        f.write(f'role: {role.strip()}')
        f.write(f'location: {location.strip()}')
        f.write(f'postingLink: {postingLink}')


