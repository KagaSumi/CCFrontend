from flask import Flask, render_template
import requests
import sys

app = Flask(__name__)

def get_instance_metadata():
    metadata = {}
    try:
        metadata['region'] = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone').text[:-1]
        metadata['zone'] = requests.get('http://169.254.169.254/latest/meta-data/placement/availability-zone').text
        metadata['subnet'] = requests.get('http://169.254.169.254/latest/meta-data/network/interfaces/macs/{}/subnet-id'.format(requests.get('http://169.254.169.254/latest/meta-data/mac').text)).text
        metadata['instance_id'] = requests.get('http://169.254.169.254/latest/meta-data/instance-id').text
    except requests.RequestException as e:
        metadata['error'] = str(e)

    return metadata

@app.route('/')
def send_request():
    metadata = get_instance_metadata()
    url = sys.argv[1]+"/api/product/apple"  # Replace with the URL of the web application you want to send a request to
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return render_template('base.html', data=response.text, region=metadata['region'], zone=metadata['zone'], subnet=metadata['subnet'], instance_id=metadata['instance_id'])
        else:
            return render_template('base.html', data=f"Failed to send request. Status code: {response.status_code}", region=metadata['region'], zone=metadata['zone'], subnet=metadata['subnet'], instance_id=metadata['instance_id'])
    except requests.RequestException as e:
        return render_template('base.html', data=f"Request failed with error: {e}",region=metadata['region'], zone=metadata['zone'], subnet=metadata['subnet'], instance_id=metadata['instance_id'])

def main(url):
    app.run(debug=True)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a valid URL.")
