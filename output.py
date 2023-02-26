from helpers import getCurrentStore
import csv, re

def doOutputFile(companyFilter, roleFilter):
    _, store = getCurrentStore()
    if (store['postings'] != []):
        postings = []

        # filter
        for post in store['postings']:
            if re.search(companyFilter, post['company'], re.IGNORECASE)\
                and re.search(roleFilter, post['role'], re.IGNORECASE):
                postings.append(post)

        # write csv
        with open('Internships.csv', 'w') as f:
            writer = csv.DictWriter(f, delimiter=',', fieldnames=list(postings[0].keys()))
            writer.writeheader()
            writer.writerows(postings)