# Wiki Rabbit
Everybody's favorite Wikipedia game, now in your terminal
![intro-screen](https://i.imgur.com/x4giUCy.png)
## The game
First, an article is randomly selected from [the page containing Wikipedia's most visited articles](https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages)

A random article is then selected as your starting point 

All the hyperlinks to other Wikipedia articles are selected from the page you are currently on, 5 will be randomly selected for you to choose from 

![choices](https://i.imgur.com/iMBny7f.png)

If you can navigate the Wikipedia rabbit to the goal page within 10 turns, you win!

## Getting started 
You will need to have 2 python packages installed (if you don't have them already)

First, you will need [the wikipedia api](https://pypi.org/project/wikipedia/)

And, of course, [beautiful soup for scraping through the articles](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

These can both be easily installed in terminal with `pip install wikipedia` and `pip install beautifulsoup4`

In your terminal, navigate to the python file, run it, and badabing badaboom
