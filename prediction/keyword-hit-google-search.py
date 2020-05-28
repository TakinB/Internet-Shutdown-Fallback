import csv
import pprint
from googleapiclient.discovery import build
import pandas
from datetime import datetime

# TODO: inputs = startDate, endDate, keyword,
country = "Sudan"
#keyword = '"' + myKey + '" "' + country + '"'
startDate = '20190603'
endDate = '20190604'
# You can get the devKey by making a new project and creating a dev key
# from here: https://developers.google.com/custom-search/v1/overview
devKey = "AIzaSyBv7h7rEy4VUGEgTnP5HUXC8uLIeNTyP-o"
# cx is coming from making a customized search engine in google that only searches through specific website.
# currently set to search: BBC, Reuters, Aljazeera, Associate Press
# from: https://cse.google.com/cse/all
myCX = '005401467750615370446:5prav4f1lln'

myKey = '"Sudan" "attack"'

def main():
    keywordHit = getTotalGoogleSearchResult(myKey, startDate, endDate)
    pprint.pprint(keywordHit)


def getTotalGoogleSearchResult(myKey, startDate, endDate):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey=devKey)

  res = service.cse().list(
      q= myKey,
      cx= myCX,
      sort='date:r:' + str(startDate) +':' + str(endDate),
    ).execute()
  pprint.pprint(res)

  return res['searchInformation']['totalResults']

if __name__ == '__main__':
  main()


