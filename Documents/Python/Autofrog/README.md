# What is this?
This is an ugly mashup of bash and python which will crawl a list of sites sequentially, then compare the resultant export file to a previously created list of known URLs. It will then generate a single file listing all known URLs

## How do I use this?
* Start by installing [python3](https://www.python.org/downloads/) and ensure you have pandas. Use the cmd pip3 install pandas. *Make sure you add Python to your path* [like so](https://vgkits.org/blog/wp-content/uploads/2018/05/windows-add-python-path.jpg)
* Populate a list of sites you want to crawl in the sites.txt file
* Create your own [core.seospiderconfig](https://www.screamingfrog.co.uk/11-little-known-features/#:~:text=Using%2520Saved%2520Configuration%2520Profiles%2520With%2520The%2520CLI+screaming+frog) to control what and how Screaming Frog crawls. USeragent, inclusion and exclusion paths etc.
* Edit the Crawler.bat file replacing *C:\Users\josh.fegan\AppData\Local\Programs\Python\Python38\python.exe* with the path to your own version of python
* Add the Crawler.bat file to [Windows Task Scheduler](https://www.thewindowsclub.com/how-to-schedule-batch-file-run-automatically-windows-7
) selecting a time, date and frequency to run
* Double Click on Crawler.bat to create the known lists of URLs

## How exactly does this work?
The bash script parses a sites.txt file then sequentially crawls each site in Screaming Frog based on the contents of the core.seospiderconfig. It then creates a folder for that site if it doesn't already exist, and then saves the crawl, and *internal_all.csv* in the folder.

Upon completion of crawling the python script will fire, parse the sites.txt file and loop through each folder in turn. If no known.json file exists this will be created, if this file does exist the script will compare the contents of *internal_all.csv* to the list of known URLs and add any new URLs (which are HTML and have a 200 status code) to a dictionary. Assuming there are any new URLs to report in this dictionary these will then be saved to *New-URLs.csv*

## Crawler.bat is scary
Yep, its a terrible language but it does the job better than python could alone (as it wont monitor Screaming Frog to wait for completion before moving on) and simpler for the user to set up in Windows Task Scheduler than powershell.

## Why have you done this?
It wasn't my idea. Sorry

## This is terrible
Sure. Want to help improve it? Create a pull request!