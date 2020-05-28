import csv
import pprint
from googleapiclient.discovery import build
import pandas
from datetime import datetime

# TODO: inputs = startDate, endDate, keyword,
country = "Sudan"
#keyword = '"' + myKey + '" "' + country + '"'
startDate = '20190601'
endDate = '20190630'
# You can get the devKey by making a new project and creating a dev key
# from here: https://developers.google.com/custom-search/v1/overview
devKey = "AIzaSyBv7h7rEy4VUGEgTnP5HUXC8uLIeNTyP-o"
# cx is coming from making a customized search engine in google that only searches through specific website.
# currently set to search: BBC, Reuters, Aljazeera, Associate Press
# from: https://cse.google.com/cse/all
myCX = '005401467750615370446:5prav4f1lln'

keywords = ["camp"
,"civilians"
,"test"
,"demonstration",
"test"
]



# Creating date strings for the csv file
ShutDates = [d.strftime('%Y%m%d') for d in pandas.date_range(startDate, endDate)]
keywordHit=[0] * len(ShutDates)

#writing date strings in the first column of the csv file
#with open(fileName+'.csv', 'w') as csvfile:
#    filewriter = csv.writer(csvfile, delimiter=',',
                            #quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #for row in ShutDates:
        #pprint.pprint([row])
    #    filewriter.writerow([row])

def main():

    for k in range(len(keywords)):
        fileName = country + keywords[k] + datetime.now().strftime('%Y%m%d%H%M%S')
        myKey =  '"' + keywords[k] + '" "' + country + '"'
        for i in range(len(ShutDates)-1):
           # i=1
            keywordHit[i] = getTotalGoogleSearchResult(myKey, ShutDates[i], ShutDates[i+1])
            #pprint.pprint(keywordHit[i])
        # writing date strings in the first column of the csv file
        with open(fileName + '.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #
            for j in range(len(ShutDates)-1):
                #while True:
                 #   if (keywordHit[i]!=0 and keywordHit[i]!=None):
                        pprint.pprint([ShutDates[j], keywordHit[j]])
                        filewriter.writerow([ShutDates[j], keywordHit[j]])
                           # break

# YYMMDD
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
  #pprint.pprint(res)

  if (res['searchInformation']['totalResults']) != '0':
      pprint.pprint(res['items'][0]['formattedUrl'])
  #pprint.pprint(res['searchInformation']['totalResults'])
  return res['searchInformation']['totalResults']

if __name__ == '__main__':
  main()


