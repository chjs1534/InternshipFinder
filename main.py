from scraper import doWebScrape
from output import doOutputFile

if __name__ == "__main__":
    # set options for output
    while True:
        action = input("Enter 1 to search all, 2 to search by company, 3 to search by role:\n")
        if action in ['1', '2', '3']:
            break

    companyFilter = '.*'
    roleFilter = '.*'
    if action == '2':
        companyFilter = input("Enter company:\n")
    elif action == '3':
        roleFilter = input("Enter role:\n")
    
    doWebScrape()
    doOutputFile(companyFilter, roleFilter)
