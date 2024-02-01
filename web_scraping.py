#Installing and importing necessary libraries
import pandas as pd
import warnings
import requests
from bs4 import BeautifulSoup
warnings.simplefilter('ignore')

#Retrieving the HTML page of a website by bypassing authorization
url='https://www.imdb.com/list/ls089279403/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
html_code=requests.get(url,headers=headers)

#Parsing the HTML content using BeautifulSoup
html_text=BeautifulSoup(html_code.text,'lxml')

#Create a new dataframe to store the data
result=pd.DataFrame(columns=['Song','Sound track','Description'])

#List 100 Best Songs of All Time
list_of_songs=html_text.find_all('div', class_='lister-item mode-detail')
for i in range(100):
  #Getting description of song
  description=list_of_songs[i].find('div',class_='list-description').find('p').text
  #Getting title and sound track of the song
  songtitle=list_of_songs[i].find('h3','lister-item-header').find('a').text
  soundtrack=list_of_songs[i].find('p',class_='text-muted text-small').find('a').text
  result=result.append({'Song':songtitle,'Sound track':soundtrack,'Description':description},ignore_index=True,)

#Performing the data cleaning to the dataframe
result['Song']=result['Song'].str.strip()
result['Sound track']=result['Sound track'].str.strip()
result['Description']=result['Description'].str.strip()

for x,y in zip(range(100),result['Description']):
  result.loc[x,'Description']=y.replace(str(x+1)+'. ','')

#Writing the dataframe to csv
result.to_csv('result.csv',index=False)

result.head(10)
