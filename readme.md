Steps to run scraper:

1. Install GeckoDriver and FireFox
  a. on line 13 in ```main.py```, replace the given GeckoDriver executable's location with yours. 
    For example:
    
     ```
      executable_path="/path/to/geckodriver"
     ```
      becomes
     ```
      executable_path="/Users/archisharun/Downloads/geckodriver"
     ```
     on my own machine, as my GeckoDriver was installed in my Downloads folder.

2. Clone Repo and run the following commands in terminal

```
cd your/path/to/edgar-scraper
python3 -m venv venv
source venv/bin/activate
pip install requirements.txt
```
3. Run project!
```
python3 main.py
```

