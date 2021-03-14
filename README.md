# Phishy URLs

Performs simple lookups of suspicious phishy URLs. No API KEYs required:

1. Whois lookup
2. DNS records (A, MX, SPF, TXT, CNAME)
3. Peforms HEAD request to get headers (useful if there is URL is shortened or there redirect based on Location header)
4. Take screenshots of web-site (mobile and desktop)

# Installation

```bash
virtualenv env
source bin/activate
pip install -r requirements.txt
```

# Run

```bash
python lookuper.py
```
