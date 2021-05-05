import os  # for clearing screen
import random  # holds up spork
import re  
import sys  
import time  
import requests  # for the http requests
import wikipedia  # the free encyclopedia
from bs4 import BeautifulSoup 
from badarticles import badArticles

cls = lambda: os.system('cls')
cls()

# Building the bunny
faces = ['^.^','>.>','<.<','o.o','o.O','@.@','u.u','*.*','v.v','O.O','-.-','^v^'] 
def printRabbit(i):
    print(f' (\_/)\n ({faces[i]})\n (___)!')
def create_face_num():
    return random.randint(0, (len(faces)) - 1)
faceNum = create_face_num()
rabbitHoles = 0

def suspense(message):
    for i in range(1,4):
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(message + ('.' * i))
        time.sleep(1)
    print('\n')


# Main Wikipedia article
response = requests.get(url='https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages')
soup = BeautifulSoup(response.content, 'html.parser')
mostViewedTable = soup.find('tbody') # the table of most viewed articles has no id >:( but luckily it is the only element with a <tbody> tag

mostViewedLinks = []
for link in mostViewedTable.find_all('a'):
    if (link.get('href'))[6:] in badArticles:
        continue
    mostViewedLinks.append('http://en.wikipedia.org' + link.get('href'))

def introScreen():
    printRabbit(0)
    input('This is the Wikipedia rabbit\nHe likes to go down rabbit holes to find Wikipedia articles\nYour goal is to guide him down the proper holes to his destination\nHe will start on a random article\nPress enter to begin')
    cls()

# creating the start and end page
def startingArticles():
    goalLink = random.choice(mostViewedLinks)
    a = requests.get(url=goalLink) 
    goalSoup = BeautifulSoup(a.content, 'html.parser')
    goalTitle = goalSoup.find(class_ = 'firstHeading').text 

    startingLink = "https://en.wikipedia.org/wiki/Special:Random" 
    b = requests.get(url=startingLink) 
    startingSoup = BeautifulSoup(b.content, 'html.parser')
    startingTitle = startingSoup.find(class_ = 'firstHeading').text

    return {'goalTitle': goalTitle, 'startingTitle': startingTitle}
articleInfo = startingArticles()

def articleOptions(article_title):
    linksList = wikipedia.page(article_title).links
    random.shuffle(linksList)
    if len(linksList) <= 10:
        for x in range(len(linksList)):
            print( str(x+1) + ': ' + linksList[x])
    else:        
        for x in range(0, 10):
            print( str(x+1) + ': ' + linksList[x])
    return linksList

def gameStats(schroedinger='alive', current='current article'):
    cls()
    print(f'Rabbit holes entered: {rabbitHoles}    Current article: {current}    Goal article: {articleInfo["goalTitle"]}')
    if schroedinger == 'dead':
        printRabbit(-1)
    else: 
        printRabbit(faceNum)

def userInput():
    global rabbitHoles
    choice = input('\nEnter article number then press Enter\n')
    rabbitHoles += 1
    choice = int(choice) - 1
    return choice

def startGame():
    introScreen()
    suspense('The article you want to reach is')
    print(articleInfo["goalTitle"])
    print(wikipedia.summary(articleInfo["goalTitle"], sentences=1) + '\n')
    suspense('The article you are starting with is')
    print(articleInfo['startingTitle'])
    print(wikipedia.summary(articleInfo['startingTitle'], sentences=1))
    input('Press enter to continue')
    cls()
    gameStats('alive', articleInfo['startingTitle'])
    suspense('Your options are')
    linksList = articleOptions(articleInfo['startingTitle'])
    choice = userInput()
    currentTitle = linksList[choice]
    cls()
    return currentTitle

currentTitle = startGame()
while currentTitle != articleInfo['goalTitle']: 
    cls()
    gameStats('alive', currentTitle)
    suspense('Your options are')
    linksList = articleOptions(currentTitle)
    choice = userInput()
    currentTitle = linksList[choice]