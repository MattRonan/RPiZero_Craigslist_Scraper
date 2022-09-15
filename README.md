# RPiZero_Craigslist_Scraper

  Lets say you're looking on Craigslist for a slightly obscure tool, a specific car, etc.
You may have to wait weeks or months for the right post to show up, checking daily, and if its a really hot item it might be gone before you even have a chance.

  This scraper system uses a Raspberry Pi Zero to run a search every 5 minutes using Requests and Beautiful Soup.
It maintains some simple log files so it knows when a new hit has appeared and blinks a nice red LED to get your attention.  The RPi uses an Apache server to post to a page, viewable via the local network, where it shows the current search hits with the new hits marked.  You can then check them out and click a button to mark them as seen so it'll stop blinking.
