# EDGAR Filings Scraper


Steps to run scraper:

1. Install [GeckoDriver](https://github.com/mozilla/geckodriver/releases) and [FireFox](https://www.mozilla.org/en-US/firefox/new/)\
  a. on line 13 in ```main.py```, replace the given GeckoDriver executable's location with yours. 
    For example:
    
     ```
      executable_path="/path/to/geckodriver"
     ```
      Becomes
     ```
      executable_path="/Users/archisharun/Downloads/geckodriver"
     ```
     on my own machine, since my GeckoDriver was installed in my Downloads folder.

2. Clone Repo and run the following commands in terminal

```
cd your/path/to/edgar-scraper
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```
3. Run project with the following command! 
```
python3 main.py
```

Note: An instance of Firefox will automatically open when the program starts. This doesn't necessarily mean that it will work all the way through. Depending on the day, I estimate that the process should take 20-30 mins (working on testing and optimizing!)
