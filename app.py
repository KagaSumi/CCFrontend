from flask import Flask, render_template
import requests
import sys

app = Flask(__name__)

@app.route('/')
def send_request():
    url = sys.argv[1]+"api/product/apple"  # Replace with the URL of the web application you want to send a request to
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return render_template('base.html', data=response.text)
        else:
            return render_template('base.html', data=f"Failed to send request. Status code: {response.status_code}")
    except requests.RequestException as e:
        return render_template('base.html', data=f"Request failed with error: {e}")

def main(url):
    app.run(debug=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a valid URL.")
