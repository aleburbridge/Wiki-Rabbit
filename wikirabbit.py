import wikipedia
import os
from bs4 import BeautifulSoup
import random
import requests
import re

cls = lambda: os.system('cls')
cls()

# building the bunny
faces = ['>.>','^.^','o.o','<.<','o.O','@.@','u.u','*.*','v.v','O.O','-.-','^v^','x.x']
def printRabbit(index):
    print(f' (\_/)\n ({faces[index]})\n (___)!')
randomRabbit = lambda: (f' (\_/)\n ({faces[(random.randint(0, (len(faces)) - 3) )]})\n (___)!')

#Title screen
greeting = printRabbit(1), input('This is the Wikipedia rabbit\nHe likes to go down rabbit holes to find Wikipedia articles\nYour goal is to guide him down the proper holes to his destination\nHe will start on a random article\nPress enter to begin')
cls()

# Main Wiki page with list of most viewed pages
response = requests.get(
    url='https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages'
)
soup = BeautifulSoup(response.content, 'html.parser')
mostViewedTable = soup.find('tbody')

mostViewedLinks = [] # generating navigable links from the table
for link in mostViewedTable.find_all('a'):
    mostViewedLinks.append('http://en.wikipedia.org' + link.get('href'))

# Parameters for current game
goalPage = mostViewedLinks[(random.randint(0, len(mostViewedLinks)))]
a = requests.get(goalPage)
goalSoup = BeautifulSoup(a.content, 'html.parser')
goalTitle = goalSoup.find(class_ = "firstHeading").text

randomPage = "https://en.wikipedia.org/wiki/Special:Random"
u = requests.get(randomPage)
randomSoup = BeautifulSoup(u.content, 'html.parser')
randomTitle = randomSoup.find(class_ = "firstHeading").text

linksList = []
def articleOptions():
    global rabbitHoles
    allLinks = randomSoup.find(id='bodyContent').find_all('a', href=re.compile('/wiki/'))
    for item in allLinks:
        linksList.append(item)
    random.shuffle(linksList)


    print('Your choices are')
    if len(linksList) < 5:
        for x in range(1, len(linksList)):
            print( str(x+1) + ': ' + linksList[x]['title'])
    else:
        for x in range(0,5):
            try: 
                print( str(x+1) + ': ' + linksList[x]['title'])
            except TypeError:
                print( str(x+1) + ': ' + linksList[x])
            except KeyError:
                print( str(x+1) + ': ' + linksList[x])
    rabbitHoles += 1

rabbitHoles = 0
def gameInfo(schroedingersBunny):
    cls()
    print(f'Rabbit holes entered: {rabbitHoles}    Current article: {currentTitle}    Goal article: {goalTitle}')
    if schroedingersBunny == 'alive':
        print(randomRabbit())
    elif schroedingersBunny == 'dead':
        printRabbit(-1)
    else: 
        print(randomRabbit)

# Screen 1
print(f'Rabbit holes entered: {rabbitHoles}    Current article: {randomTitle}    Goal article: {goalTitle}')
print(randomRabbit())
print('The article you want to reach is ' + goalTitle)
print('The article you are starting with is ' + randomTitle)
input('Press enter to send your rabbit down the hole!')

# Screen 2
cls()
print(f'Rabbit holes entered: {rabbitHoles}    Current article: {randomTitle}    Goal article: {goalTitle}')
print(randomRabbit())
articleOptions()
articleInput = input('Enter article number then press enter: ')
currentPage = randomPage
currentTitle = ''
def currentArticleOptions():
    global rabbitHoles
    global currentTitle
    global currentPage
    linksList = []

    x = requests.get(currentPage)
    currentSoup = BeautifulSoup(x.content, 'html.parser')
    currentTitle = currentSoup.find(class_ = "firstHeading").text

    gameInfo('alive')

    allLinks = currentSoup.find(id='bodyContent').find_all('a', href=re.compile('/wiki/'))
    for item in allLinks:
        linksList.append(item)
    random.shuffle(linksList)

    currentPage = 'http://en.wikipedia.org' + linksList[int(articleInput) - 1].get('href')


    print('Your choices are')
    if len(linksList) == 0:
        print('Dead end! Thats game over! bitch!')
    elif len(linksList) < 5:
        for x in range(0, len(linksList)):
            print( str(x+1) + ': ' + linksList[x]['title'])
    else:
        for x in range(0,5):
            try: 
                print( str(x+1) + ': ' + linksList[x]['title'])
            except TypeError:
                print( str(x+1) + ': ' + linksList[x])
            except KeyError:
                print( str(x+1) + ': ' + linksList[x])
    rabbitHoles += 1

#Screen 3 - Infinity
def gameFlow():
    currentArticleOptions()
    articleInput = input('Enter article number then press enter: ')

def gameOver():
    gameInfo('dead')
    print('The Wikipedia rabbit has gone down too many holes and has fucking died.')
    
while currentTitle != goalTitle:
    gameFlow()
    if rabbitHoles > 10:
        break
gameOver()