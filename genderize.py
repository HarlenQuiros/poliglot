import requests

def predict_gender(name):
    url = "https://api.genderize.io"
    params = {"name": name}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("gender", "male")
    else:
        print(f"Error: {response.status_code}")
        return "male"  # Default value
