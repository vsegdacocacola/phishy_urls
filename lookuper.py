from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import dns.resolver, whois, json, requests, base64, sys, re
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import render_template
from time import sleep

PATH = "<path to chromedriver>"

# Init app
app = Flask(__name__, template_folder='static')

auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello")
}

def isSafe(req_string, type):
    if(req_string == ""):
        return False
    elif(type=="hostname") and not (re.match(r"^[A-Za-z0-9\.]+$", req_string) or re.match(r"^[\d]+\.[\d]+\.[\d]+\.[\d]+$", req_string)) and re.match( r".*localhost.*|.*127\.[\d]+\.[\d]+\.[\d]+.*|.*192\.168\.[\d]+\.[\d]+.*|.*10\.[\d]+\.[\d]+\.[\d]+.*|.*172\.16\.[\d]+\.[\d]+.*", req_string):
        return False
    elif(type=="url"):
        parsed_url = urlparse(req_string)
        if( parsed_url.scheme not in ["http", "https"]):
            return isSafe(parsed_url.netloc, 'hostname')
        else:
            return True
    else:
        return True

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return render_template("index.html")

# DNS 
@app.route('/api/dns', methods=['POST'])
@auth.login_required
def resolve():
    if('host' in request.json.keys()):
        host = request.json['host'].strip()
        if(not isSafe(host, 'hostname')):
            return jsonify({'error' : 'host is invalid!'})
    else:
        return jsonify({'error' : 'host is not provided!'})
    ids = ['A', 'TXT', 'MX', 'SPF']
    result = {}
    for id in ids:
        try:
            answers = dns.resolver.resolve(host, id)
        except:
            pass
        result[id] = []
        for rdata in answers:
            result[id].append(rdata.to_text())
    return jsonify(result)

# Whois
@app.route('/api/whois', methods=['POST'])
@auth.login_required
def check_whois():
    if('host' in request.json.keys()):
        host = request.json['host'].strip()
        if(not isSafe(host, 'hostname')):
            return jsonify({'error' : 'host is invalid!'})
    result = {}
    try:
        result = whois.whois(host)
    except:
        result['erorr'] = sys.exc_info()[0]
    return jsonify(result)

# URL parse
@app.route('/api/url', methods=['POST'])
@auth.login_required
def parse_url():
    if('url' in request.json.keys()):
        url = request.json["url"].strip()
        if(not isSafe(url, 'url')):
            return jsonify({'error' : 'url is invalid!'})
    else:
        return jsonify({'error': 'url is not provided!'})
    result = {}
    result = dict(zip(['scheme', 'netloc', 'path', 'params', 'query', 'fragment'], urlparse(url)))
    return jsonify(result)

# Head
@app.route('/api/head', methods=['POST'])
@auth.login_required
def expand_url():
    if('url' in request.json.keys()):
        url = request.json["url"].strip()
        if(not isSafe(url, 'url')):
            return jsonify({'error' : 'url is invalid!'})
    else:
        return jsonify({'error': 'url is not provided!'})
    result = {}
    try:
        response = requests.head(url)
    except:
        return jsonify({'error' : sys.exc_info()[0]})
    return jsonify(dict(response.headers))

# Make screenshot
@app.route('/api/screenshot', methods=['POST'])
@auth.login_required
def make_screenshot_mobile():
    if('url' in request.json.keys()):
        url = request.json['url'].strip()
        if(not isSafe(url, 'url')):
            return jsonify({'error' : 'url is invalid!'})
    else:
        return jsonify({'error' : 'url is not provided'})
    if('device' in request.json.keys()):
        device = request.json['device']
    else:
        device = ""

    if(device=="mobile"):
        device_emulation = {
            "userAgent": "Mozilla/5.0 (iPod; CPU iPhone OS 12_0 like macOS) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/12.0 Mobile/14A5335d Safari/602.1.50"
        }
    else:
        device_emulation = {
            "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }
    result = {}
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", device_emulation)
        driver = webdriver.Chrome(
            executable_path=PATH, options=chrome_options
        )
        driver.get(url)
        sleep(1)
        result['image'] = driver.get_screenshot_as_base64()
        driver.close()
    except:
        result['erorr'] = sys.exc_info()[0]
    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True)
