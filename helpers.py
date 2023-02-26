import json, os

def getCurrentStore():
    # get current data in file
    store = {}
    d = {}
    if (os.stat('posts/jobs.json').st_size != 0):
        with open('posts/jobs.json', 'r') as f:
            store = json.load(f)
        
        for obj in store['postings']:
            d.update({obj['company'] + " " + obj['role']: 1})
    else:
        store = {'postings': []}
    
    return d, store