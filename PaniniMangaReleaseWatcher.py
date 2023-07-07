import json

def getMangasToWatchFromFile():
    """ Reads the mangas.json file to get the mangas to track.
    """
    with open('mangas.json') as json_file:
        data = json.load(json_file)
        for manga in data['mangas']:
            print('Name: ' + manga['name'])
            print('Items: ' + str(manga['items']))
        return data

def getWebsiteContents(mangaName):
    """ Gets the search website for the manga.
    """
    return 0

def getAmountOfItems(websiteContent):
    """ Matches a regex against the search website to find the current items that were returned for the search.
    """
    # Regex: <span class="toolbar-number">(\d+)</span>

    return 0

def checkIfNewRelease(amountOfItems):
    """ Compares if the current items in the website is grater than the previous number of items.
    """
    return 0

def sendEmail():
    """ Sends an email if there is a new release for the manga.
    """
    return 0

def main():
    getMangasToWatchFromFile()

if __name__ == "__main__":
    main()
