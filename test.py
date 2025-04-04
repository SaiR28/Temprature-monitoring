import requests
import time
import os

def test_log_temperature(url, temperature):
    response = requests.post(f"{url}/log", json={"temperature": temperature})
    print("Log Temperature Response:", response.json())

def test_last_entry(url):
    response = requests.get(f"{url}/last_entry")
    print("Last Entry Response:", response.json())

def test_temperature_data(url):
    response = requests.get(f"{url}/temperature_data")
    print("Temperature Data Response:", response.json())

def test_download_csv(url, filename="temperature_log.csv"):
    response = requests.get(f"{url}/download")
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"CSV file downloaded successfully as {filename}")
    else:
        print("Failed to download CSV file")

if __name__ == "__main__":
    BASE_URL = "https://temprature-monitoring.onrender.com/"  # Update if running on a different host
    
    print("Starting API tests...")
    
    # Log multiple temperature values
    for temp in [22.5, 23.1, 24.0, 25.3, 26.7]:
        test_log_temperature(BASE_URL, temp)
        time.sleep(1)  # Small delay to simulate real logging
    
    # Retrieve last logged entry
    test_last_entry(BASE_URL)
    
    # Retrieve last 20 temperature entries with min/max calculation
    test_temperature_data(BASE_URL)
    
    # Download and save CSV file
    test_download_csv(BASE_URL)
    
    print("API tests completed.")