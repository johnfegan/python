:: Turning off code announcements and setting variables
@echo off
SET dir=%~dp0
SET conf=core.seospiderconfig
cd "C:\Program Files (x86)\Screaming Frog SEO Spider"
:: Horrendous for loop splitting URL using forward slash
for /f "tokens=1,2 delims=/" %%G in (%~dp0\sites.txt) do (
	:: creating folder for site if it doesn't exist
	if not exist %~dp0\%%H mkdir %~dp0\%%H
	:: Crawling the site and saving the internal_all.csv file in the (possibly) created folder 
	ScreamingFrogSEOSpiderCli.exe --crawl %%G//%%H --config %dir%%conf% --headless --save-crawl --output-folder %dir%%%H  --overwrite --export-tabs "Internal:All"
)
:: You'll need to change the below to point to your python instance
C:\Users\josh.fegan\AppData\Local\Programs\Python\Python38\python.exe %dir%//urlFinder.py"
pause