from flask import Flask, render_template, redirect,request
import bs4
import requests
import os
app = Flask(__name__)


def scrape_site(URL, keyword):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text)
    ##results = [ [a.attrs.get('href'), a.contents[0]] for a in soup.select('a[href^=' + URL + ']') if keyword.lower() in str(a.contents[0]).lower() ]
    results = [ [a.attrs.get('href'), a.get_text()] for a in soup.select('a[href^=' + URL + ']') if keyword.lower() in str(a.contents[0]).lower() ]
    print(soup.find_all("h3")[0].parent.attrs.get('href'))
    results = results = [ [a.parent.attrs.get('href'), a.get_text()] for a in soup.find_all('h3') if keyword.lower() in str(a.get_text()).lower()]
    ##results = resullt + [ ["", a] for a in soup.find_all('h3') ]
    ##results = results + [ [URL + a.attrs.get('href'), a.contents[0]] for a in soup.select('a[href^=/]')  if keyword.lower() in str(a.contents[0]).lower() ]
    results = results + [ [URL + a.attrs.get('href'), a.get_text()] for a in soup.select('a[href^=/]')  if keyword.lower() in str(a.contents[0]).lower() ]
    b_set = set(tuple(x) for x in results)
    b = [ list(x) for x in b_set ]
    b.sort(key = lambda x: results.index(x) )
    results = b
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods = ['POST'])
def scrape_and_show():
    URL = request.form['url']
    keyword = request.form['keyword']
    result = scrape_site(URL, keyword)
    return render_template('results.html', keyword=keyword, URL=URL, result=result)

@app.route('/back')
def home():
    return redirect("/")

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))
