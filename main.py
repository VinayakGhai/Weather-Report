import requests
import numpy as np
from termcolor import colored  # For colored text
from config import API_KEY

# Define Mumbai's coordinates
city = "Mumbai"
coords = (19.0760, 72.8777)  # Latitude and Longitude for Mumbai

def get_weather(lat, lon):
    url = f'https://api.weatherbit.io/v2.0/current?lat={lat}&lon={lon}&key={API_KEY}'
    response = requests.get(url)
    return response.json()

def analyze_weather(weather_data):
    if 'data' in weather_data:
        main = weather_data['data'][0]
        return {
            "Temperature": main['temp'],
            "Humidity": main['rh'],
            "Wind Speed": main['wind_spd'],
            "Rain Probability": main['precip'] * 100,
            "Weather": main['weather']['description']
        }
    else:
        print("Error retrieving weather data:", weather_data.get('error', 'Unknown error'))
        return None

def calculate_rain_probabilities(humidity, temperature, wind_speed):
    # Example complex formulas for rain probability
    prob1 = 0.1 * humidity + 0.05 * temperature - 0.02 * wind_speed
    prob2 = 0.08 * humidity + 0.06 * temperature - 0.01 * wind_speed
    prob3 = 0.12 * humidity + 0.03 * temperature - 0.03 * wind_speed
    prob4 = 0.09 * humidity + 0.07 * temperature - 0.04 * wind_speed
    prob5 = 0.11 * humidity + 0.04 * temperature - 0.02 * wind_speed
    prob6 = 0.07 * humidity + 0.08 * temperature - 0.01 * wind_speed
    prob7 = 0.1 * humidity + 0.05 * temperature - 0.03 * wind_speed
    
    return [prob1, prob2, prob3, prob4, prob5, prob6, prob7]

def display_weather(weather_report):
    if weather_report:
        print(colored("\n--- Weather Report for Mumbai ---", 'cyan'))
        print(colored(f"Temperature: {weather_report['Temperature']}°C", 'magenta'))
        print(colored(f"Weather: {weather_report['Weather']}", 'yellow'))
        
        # Display Humidity and Weather Percentages
        humidity_percentage = weather_report['Humidity']
        weather_description = weather_report['Weather']
        
        print(colored(f"Humidity: {humidity_percentage}%", 'green'))
        print(colored(f"Weather Description: {weather_description}", 'blue'))

        # Calculate and display rain probabilities
        humidity = weather_report['Humidity']
        temperature = weather_report['Temperature']
        wind_speed = weather_report['Wind Speed']
        
        probabilities = calculate_rain_probabilities(humidity, temperature, wind_speed)
        avg_probability = np.mean(probabilities)
        
        print(colored("\n--- Rain Probability Calculations ---", 'cyan'))
        for i, prob in enumerate(probabilities, start=1):
            print(colored(f"Formula {i}: {prob:.2f}%", 'yellow'))
        
        print(colored(f"\nFinal Average Rain Probability: {avg_probability:.2f}%", 'red'))

def main():
    lat, lon = coords
    weather_data = get_weather(lat, lon)
    report = analyze_weather(weather_data)
    display_weather(report)

if __name__ == "__main__":
    main()
