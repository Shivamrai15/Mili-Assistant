import os
import psutil
import pymongo
import requests
import platform
import subprocess
import pyscreenshot
from win32 import win32cred
from threading import Thread
from datetime import datetime
from tkinter import messagebox
from functools import lru_cache
from encryption import Encryption
from location import geoLogicalCoordinate, GPS


application_directory = os.getcwd()


# This class provides functions for reading, writing, and deleting credentials stored in the Credential Manager
# ------------------------------------------------------------------------------------------------------------
class CredentialManager:
    def __init__(self):
        self.target_name = "MiliCredential-WZp25giS54qFf44"

    def read_credential(self) -> str:
        try:
            credential = win32cred.CredRead(
                self.target_name, win32cred.CRED_TYPE_GENERIC, 0
            )
            username = credential["UserName"]
            password = credential["CredentialBlob"]
            username = Encryption(username.encode("utf-8")).decrypt_text()
            password = Encryption(
                (password.decode("utf-16")).encode("utf-8")
            ).decrypt_text()
            return username, password
        except Exception as e:
            return None, None

    def write_credential(self, username, password):
        try:
            username = Encryption(username).encrypt_text().decode()
            password = Encryption(password).encrypt_text().decode()
            credential = {
                "Type": win32cred.CRED_TYPE_GENERIC,
                "TargetName": self.target_name,
                "UserName": username,
                "CredentialBlob": password,
                "Persist": win32cred.CRED_PERSIST_ENTERPRISE,
            }
            win32cred.CredWrite(credential, 0)
            return True
        except Exception as e:
            messagebox.showerror(title="Mili", message=f"{e}")
            return False

    def delete_credential(self):
        try:
            win32cred.CredDelete(self.target_name, win32cred.CRED_TYPE_GENERIC, 0)
            return True
        except:
            return False


# ------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------
@lru_cache(maxsize=1)
def UserCredentials(Id) -> dict:
    if Id is None:
        Id, password = CredentialManager().read_credential()
    if Id is not None:
        try:
            url = Encryption(
                b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
            ).decrypt_text()
            client = pymongo.MongoClient(url)
            db = client["Assistant"]
            collection = db["User Credentials"]
            query = {"email": Id}
            data = collection.find_one(query, {"previous_passwords": 0})
            return data
        except:
            return None
    else:
        return None


# ------------------------------------------------------------------------------------------------------------


# class to retrieve weather data
# this function returns the data as a dictionary object
# for this use weather.com api and web scraping to scrap data
# ------------------------------------------------------------------------------------------------------------
class Weather:
    def __init__(self, location):
        self.location = location
        if self.location is not None:
            try:
                self.coordinates = geoLogicalCoordinate(self.location)
            except:
                self.coordinates = GPS.getLocation()
        else:
            self.coordinates = GPS.getLocation()
        self.hourly_forecast = None
        self.API_data = None

    # -------------------------------------------------------------------------------------------
    def dataProcessing(self, response):
        daily_forecast = response.get("forecast")
        day_1_forecast = []
        day_2_forecast = []
        forecast_day_1 = daily_forecast.get("forecastday")[0]
        forecast_day_2 = daily_forecast.get("forecastday")[1]
        hourly_forecast_day_1 = forecast_day_1.get("hour")
        hourly_forecast_day_2 = forecast_day_2.get("hour")
        for dict in hourly_forecast_day_1:
            data = {
                "time": dict.get("time"),
                "temp": dict.get("temp_c"),
                "condition": dict.get("condition").get("text"),
            }
            day_1_forecast.append(data)
        for dict in hourly_forecast_day_2:
            data = {
                "time": dict.get("time"),
                "temp": dict.get("temp_c"),
                "condition": dict.get("condition").get("text"),
            }
            day_2_forecast.append(data)
        day_1_forecast.extend(day_2_forecast)
        current_hour = datetime.now().hour
        self.hourly_forecast = day_1_forecast[current_hour : (current_hour + 6)]

    # -------------------------------------------------------------------------------------------

    # fetching data from the weather.com api
    # data is uv index, feels like temperature, pressure, visibility
    # current temperature,  humidity, windspeed
    # -------------------------------------------------------------------------------------------------------

    def weatherForecastAPI(self):
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        querystring = {
            "q": f"{self.coordinates[0]}, {self.coordinates[1]}",
            "days": "3",
        }
        headers = {
            "X-RapidAPI-Key": Encryption(
                b"gAAAAABkdMK34LRPYmOl0yqr9j-_cd6WAa_Kq2fX039EFe9fDQ5l5DeIha1SDIN5x5Gsp2Ly00_S_G68-1BfaqKATyKjRu60N2XOkLvZ7jS6_9YE2scWEQ59mrDWfKSKBl-rJEG_B5En8RWu_z3uXWICOa5fe5kH4A=="
            ).decrypt_text(),
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com",
        }
        response = requests.get(url, headers=headers, params=querystring)
        response = response.json()

        thread = Thread(target=self.dataProcessing, args=(response,))
        thread.start()
        location = response.get("location")
        city = location.get("name")
        region = location.get("region")
        current_data = response.get("current")
        current_temp = current_data.get("temp_c")
        weather_condition = current_data.get("condition").get("text")
        feels_like_temp = current_data.get("feelslike_c")
        wind_speed = current_data.get("wind_kph")
        visibility = current_data.get("vis_km")
        humidity = current_data.get("humidity")
        pressure = current_data.get("pressure_mb")
        uv_index = current_data.get("uv")
        uv_index = current_data.get("uv")
        precipation = current_data.get("precip_in")
        daily_forecast = response.get("forecast")
        forecast_day = daily_forecast.get("forecastday")[0].get("day")
        rain_prediction = forecast_day.get("daily_chance_of_rain")
        max_temp = forecast_day.get("maxtemp_c")
        min_temp = forecast_day.get("mintemp_c")
        astro = daily_forecast.get("forecastday")[0].get("astro")
        sunrise = astro.get("sunrise")
        sunset = astro.get("sunset")
        thread.join()
        # ----------------------------------------------------------------------------------
        self.API_data = {
            "location": f"{city}, {region}",
            "current_temp": current_temp,
            "condition": weather_condition,
            "feels_like_temp": feels_like_temp,
            "wind_speed": wind_speed,
            "visibility": visibility,
            "humidity": humidity,
            "pressure": pressure,
            "uv_index": uv_index,
            "precipation": precipation,
            "rain_prediction": rain_prediction,
            "max_temp": max_temp,
            "min_temp": min_temp,
            "sunrise": sunrise,
            "sunset": sunset,
            "hourly_forecast": self.hourly_forecast,
        }

    # -------------------------------------------------------------------------------------------------------

    # This function is used to execute weatherForecastAPI() function and scrapingWeatherData(self)
    # This function used multithreading for faster execution
    # -------------------------------------------------------------------------------------------------------
    def data_handling(self):
        thread1 = Thread(target=self.weatherForecastAPI)
        thread1.start()
        thread1.join()
        return self.API_data

    # -------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------------


# This class facilitates the process of capturing and saving screenshots.
# It offers a functionality to capture screenshots and automatically save them in the "Pictures" directory located in the C drive.
# ------------------------------------------------------------------------------------------------------------
class ScreenShot:
    def __init__(self):
        self.filepath = None

    def file_name(self):
        users = psutil.users()[0]
        username = users.name
        file_name = f"Screenshot {datetime.strftime(datetime.now(), '%Y-%m-%d')} {int(datetime.timestamp(datetime.now()))}.png"
        self.filepath = f"C:\\Users\\{username}\\Pictures\\Screenshots\\{file_name}"

    def take_screenshot(self):
        thread = Thread(target=self.file_name)
        thread.start()
        image = pyscreenshot.grab()
        thread.join()
        image.save(self.filepath)


# ------------------------------------------------------------------------------------------------------------


# This function returns the name of the windows device
# ------------------------------------------------------------------------------------------------------------
def device_name() -> str:
    deviceName = subprocess.check_output(["wmic", "csproduct", "get", "name"])
    deviceName = deviceName.decode().split()
    deviceName.pop(0)
    return " ".join(deviceName)


# ------------------------------------------------------------------------------------------------------------


# This function returns the model name of the windows device
# ------------------------------------------------------------------------------------------------------------
def device_Model() -> str:
    device_name = platform.node()
    return device_name


# ------------------------------------------------------------------------------------------------------------
