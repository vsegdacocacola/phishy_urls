# Phishy URLs

Performs simple lookups of suspicious phishy URLs. No API KEYs required:

1. Whois lookup
2. DNS records (A, MX, SPF, TXT, CNAME)
3. Peforms HEAD request to get headers (useful if there is URL is shortened or there redirect based on Location header)
4. Take screenshots of web-site (mobile and desktop)

# Installation

1. Requires chrome as well as [chrome driver](https://chromedriver.chromium.org/)

2. Change PATH variable to location of chromedriver 

3. Setup virtualenv and install required packages

```bash
virtualenv env
source bin/activate
pip install -r requirements.txt
```

# Run

```bash
python lookuper.py
```