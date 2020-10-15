from flask import request, Flask
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

app = Flask(__name__)

@app.route('/')
def hello_world():
    session = HTMLSession()
    response = session.get("https://weather.com/en-IN/weather/tenday/l/8bc076d687d001f1e0e56eee869718d3b71f50bb7562ff6323d0d7547a8812c6")
    soup = BeautifulSoup(response.content, "html.parser")

    temp = soup.find('span', {'data-testid': 'TemperatureValue'}).text
    return f"Current temperature in Gdansk: {temp}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")