# RPiZero_Craigslist_Scraper

Searching for a planer in Brooklyn:
![script](https://user-images.githubusercontent.com/11184076/190838393-18e975b5-6399-4f0c-b5b9-ee661e0e7636.gif)

  Lets say you're looking on Craigslist for a slightly obscure tool, a specific car, etc.
You may have to wait weeks or months for the right post to show up, checking daily, and if it's really popular it might be gone before you even have a chance.

  This scraper system uses a Raspberry Pi Zero to run a search every few minutes using Requests and breaks down the results with Beautiful Soup.
It maintains some log files so it knows when a new hit has appeared and blinks a nice red LED to get your attention.  The RPi uses an Apache server to post to a page, viewable via the local network, where it shows the current search hits with the new hits highlighted in red.  You can then check them out and click a button to mark them as seen so it'll stop blinking. 

RPi's page lists the hits found.  Button lets you reset the LED once you've checked them out:
![WebsiteAndLED](https://user-images.githubusercontent.com/11184076/190838582-4b59c5e5-288a-4d0a-a981-38dd669ecaf3.gif)



To get this running, the first step is to install Apache on the RPi.  After that, the CLScraper folder goes into the root of the Apache server, which is something like /var/www/html ie wherever the index.html file is.  Then the included php and css files go in the root alongside the CLScraper folder.  You need to make sure that the files in the CLScraper folder have their read/write/execute permissions set to "Anybody", so do 'sudo chmod a+rwx /filepath' for each one.  Now to view the output you can connect to the RPi using its IP Address and load up the CLScraper.php page.

You can either manually start the python script, or use the included .desktop file to make it run automatically at startup.  I also installed xterm so that it'll open up in the terminal, but if you don't want that you can remove the xterm stuff from the "Exec" line.  The .desktop file can go in a few different folders but the easiest one is for me  /home/matt/.config/autostart.  Replace 'matt' with your username.  The .config folder is hidden so you need to show hidden files to see it. 
This file may also require setting its rwx permissions to Anyone.  You can check to make sure .desktop files work by clicking them like any script and hitting execute.

For the actual Craigslist search itself, you can change the parameters in the Python file.  There is a parameter called "strictness" which will remove any hits that don't contain your search terms (case insensitve) in the actual title.  Often a hit comes from someone mentioning the thing you want in the description despite the listing being for something else.  Happens all the time with tools or car dealerships.
