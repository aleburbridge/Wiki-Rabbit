import os  # for clearing screen
import random  # holds up spork
import re  
import sys  
import time  
import requests  # for the http requests
import wikipedia  # the free encyclopedia
from bs4 import BeautifulSoup  # get that ugly soup away from me i dont want no ugly soup

cls = lambda: os.system('cls')
cls()

# Building the bunny
faces = ['^.^','>.>','<.<','o.o','o.O','@.@','u.u','*.*','v.v','O.O','-.-','^v^','x.x'] 
def printRabbit(i):
    print(f' (\_/)\n ({faces[i]})\n (___)!')
def randomNumber():
    return random.randint(0, (len(faces)) - 3)
faceNum = randomNumber()
rabbitHoles = 0

def print_(text_to_print):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text_to_print)
    time.sleep(1)

def suspense(message):
    print_(message)
    print_(message + '.')
    print_(message + '..')
    print_(message + '...\n')

# Main Wikipedia article
response = requests.get(
    url='https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages'
)
soup = BeautifulSoup(response.content, 'html.parser')
mostViewedTable = soup.find('tbody') # the table of most viewed articles has no id >:( but luckily it is the only element with a <tbody> tag
mostViewedLinks = []
for link in mostViewedTable.find_all('a'):
    mostViewedLinks.append('http://en.wikipedia.org' + link.get('href'))

# creating the start and end page
def starterArticles():
    goalLink = mostViewedLinks[(random.randint(0, (len(mostViewedLinks) - 1)) )] # taking a random link from the table
    a = requests.get(url=goalLink) # making the http request
    goalSoup = BeautifulSoup(a.content, 'html.parser')
    goalTitle = goalSoup.find(class_ = 'firstHeading').text 
    badArticles = {'Main Page','Special:Search','Special:Random','-','Undefined','Special:Watchlist','Special:Randompage','Wiki','404.php','Portal:Current events','Special:Book','Special:CreateAccount','Search','Wikipedia:Your first article','Special:RecentChanges','Creative Commons Attribution','Wsearch.php','Portal:Contents','Wikipedia:Contact us','Talk:Main Page','Export pages', 'Wikipedia:Special:Export'}
    if goalTitle in badArticles:
        return starterArticles()
        # the table in the wiki article includes articles that are special mentions, but i dont want any of those to be the goal article

    randomLink = "https://en.wikipedia.org/wiki/Special:Random" # this link takes you to a random wikipedia article, like hitting the 'random article' button 
    b = requests.get(url=randomLink) 
    randomSoup = BeautifulSoup(b.content, 'html.parser')
    randomTitle = randomSoup.find(class_ = 'firstHeading').text

    return {'goalTitle': goalTitle, 'randomSoup': randomSoup, 'randomTitle': randomTitle}
articleInfo = starterArticles()
# now we have a useful dictionary that includes the starter article, end article, and random soup for the next bit of parsing
# to make this useful again, we just have to update randomsoup
c = {}
def articleOptions():
    linksList = articleInfo['randomSoup'].find(id='bodyContent').find_all('a', href=re.compile('/wiki/'))
    random.shuffle(linksList)
    suspense('Your options are')

    if len(linksList) == 0:
        print('Dead end! Thats game over! Also the rabbit is dead! You killed him!')
    elif len(linksList) < 5:
        for x in range(0, (len(linksList) - 1) ):
            print( str(x+1) + ': ' + linksList[x]['title'])
    else:
        for x in range(0, 5):
            try: 
                print( str(x+1) + ': ' + linksList[x]['title'])
            except KeyError:
                try: 
                    print( str(x+1) + ': ' + linksList[6]['title'])
                except KeyError:
                    print( str(x+1) + ': ' + linksList[7]['title'])
    articleInfo['linksList'] = linksList


def gameStats(schroedinger='alive', current=articleInfo['randomTitle']):
    cls()
    print(f'Rabbit holes entered: {rabbitHoles}    Current article: {current}    Goal article: {articleInfo["goalTitle"]}')
    if schroedinger == 'dead':
        printRabbit(-1)
    else: 
        printRabbit(faceNum)

def introScreen():
    printRabbit(0)
    input('This is the Wikipedia rabbit\nHe likes to go down rabbit holes to find Wikipedia articles\nYour goal is to guide him down the proper holes to his destination\nHe will start on a random article\nPress enter to begin')
    cls()

def userInput():
    global rabbitHoles
    linksList = articleInfo['linksList']
    choice = 0 
    choice = input('Enter article number then press Enter. For 5 more options, type \'6\' then Enter.\n')
    '''if choice == 'help':
        print('To view an article summary of each article, type the article number followed by an \'s\' (ex. \'1s\' to see summary of first article)')
        userInput()'''
    rabbitHoles += 1
    choice = int(choice) - 1
    if choice == 5:
        for x in range (5, 10):
            if len(linksList) < 5:
                for x in range(0, (len(linksList) - 1) ):
                    print( str(x+1) + ': ' + linksList[x]['title'])

            else:
                for x in range(5, 10):
                    try: 
                        print( str(x+1) + ': ' + linksList[x]['title'])
                    except KeyError:
                        try: 
                            print( str(x+1) + ': ' + linksList[6]['title'])
                        except KeyError:
                            print( str(x+1) + ': ' + linksList[7]['title'])
    return choice

def articleOptionsTwo():
    global choice

    currentLink = articleInfo['linksList'][int(choice)]
    currentLink = ('http://en.wikipedia.org' + currentLink.get('href'))
    c = requests.get(url=currentLink)
    currentSoup = BeautifulSoup(c.content, 'html.parser')
    currentTitle = currentSoup.find(class_ = 'firstHeading').text

    gameStats('alive', currentTitle)

    linksList = currentSoup.find(id='bodyContent').find_all('a', href=re.compile('/wiki/'))
    random.shuffle(linksList)
    suspense('Your options are')

    if len(linksList) == 0:
        print('Dead end! Thats game over! Also the rabbit is dead! You killed him!')
    elif len(linksList) < 5:
        for x in range(0, (len(linksList) - 1) ):
            print( str(x+1) + ': ' + linksList[x]['title'])
    else:
        for x in range(0, 5):
            try: 
                print( str(x+1) + ': ' + linksList[x]['title'])
            except KeyError:
                try: 
                    print( str(x+1) + ': ' + linksList[6]['title'])
                except KeyError:
                    print( str(x+1) + ': ' + linksList[7]['title'])
    articleInfo['currentTitle'] = currentTitle
    articleInfo['linksList'] = linksList

# Play the game!
introScreen()
gameStats()
linksList = articleOptions()
for x in range (0,9):
    choice = userInput()
    articleOptionsTwo() 
    if articleInfo['currentTitle'] == articleInfo['goalTitle']:
        cls()
        printRabbit(-2)
        print('u win!')
        break