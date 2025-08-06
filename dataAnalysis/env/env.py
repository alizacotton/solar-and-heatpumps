#your google api key
API_KEY = #FILL IN

#path to your chromedriver
#if you don't have chromedriver downloaded, 
#go to https://googlechromelabs.github.io/chrome-for-testing/ to download
PATH = #FILL IN

#json files containing house information
#use this website: https://console.apify.com/actors/ENK9p4RZHg0iVso52/input?addFromActorId=ENK9p4RZHg0iVso52
#and batch import addresses, download as json
#it helps to get better data if you import addresses in groups no bigger than 300
file1 = #FILL IN
file2 = #FILL IN
file3 = #FILL IN
...

jsonFiles = [file1, file2, file3, ...]

#where you would like your final dataset to be saved
finalFilepath = #FILL IN