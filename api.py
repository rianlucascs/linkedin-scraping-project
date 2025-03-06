import requests
url = "https://raw.githubusercontent.com/rianlucascs/linkedin-scraping-project/main/extracetd_data.py"

response = requests.get(url)

exec(response.text)

