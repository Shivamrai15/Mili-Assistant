import os
import json
import time
import pickle
import random
import pathlib
import zipfile
import pymongo
import datetime
import tempfile
import requests
import webbrowser
import customtkinter
from tkinter import *
from PIL import Image
from tkinter import ttk
from location import GPS
from random import randint
from functions import Weather
from functools import lru_cache
from greetMail import greetEmail
from encryption import Encryption
from threading import Thread, Lock
from emailMessage import MailToUser
from functions import UserCredentials
from functions import CredentialManager
from passlib.context import CryptContext
from tkinter import messagebox, filedialog
from functions import device_name, device_Model
from location import ip_based_location, reverseGeocoding


# Current directory of the application
application_directory = os.getcwd()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Class to download the file
# ---------------------------------------------------------------------------------------------------
class Downloaded_Data:
    def __init__(self, data: dict, chats, search_history, save_file_path):
        self.data = data
        self.search_history = search_history
        self.chats = chats
        self.save_file_path = save_file_path

    def create_directory(self, dir_name):
        tempfile.tempdir = dir_name
        path = tempfile.gettempdir()
        return path

    def user_personal_details(self):
        path = self.create_directory("Personal Details")
        file_name = "personal_details.json"
        file_path = os.path.join(path, file_name)
        file = {
            "id": str(self.data.get("_id")),
            "user_name": self.data.get("name"),
            "phone number": self.data.get("phone number"),
            "email": self.data.get("email"),
            "gender": self.data.get("gender"),
            "data of birth": self.data.get("DOB").timestamp(),
            "other_info": self.data.get("personal_info"),
        }
        jsonfile = json.dumps(file, indent=5)
        return jsonfile, file_path

    def user_account_details(self):
        path = self.create_directory("Account Details")
        file_name = "account_details.json"
        file_path = os.path.join(path, file_name)
        previous_login_list = self.data.get("login_dates")
        previous_login_details = []
        for doc in previous_login_list:
            doc["time"] = doc["time"].timestamp()
            previous_login_details.append(doc)

        file = {
            "previous_passwords": self.data.get("previous_passwords"),
            "account_created": self.data.get("ac_date").timestamp(),
            "last_login_date": self.data.get("last_login_date").timestamp(),
            "last_login_device_model": self.data.get("last_login_device_model"),
            "last_login_coordinates": {
                "latitude": self.data.get("last_login_coordinates")[0],
                "longitude": self.data.get("last_login_coordinates")[1],
            },
            "last_login_location": self.data.get("last_login_location"),
            "last_login_ip": self.data.get("last_login_ip"),
            "previous_login_details": previous_login_details,
        }
        jsonfile = json.dumps(file, indent=4)
        return jsonfile, file_path

    def parsing_data(self) -> list:
        jsonfile_1, directory_1 = self.user_personal_details()
        jsonfile_2, directory_2 = self.user_account_details()

        data = [
            {"file": jsonfile_1, "directory": directory_1},
            {"file": jsonfile_2, "directory": directory_2},
        ]
        return data

    def createFile(self):
        try:
            data = self.parsing_data()
            file_name = f"mili_{str(self.data.get('email')).replace('@gmail.com', '').strip()}.zip"
            zip_file_path = os.path.join(self.save_file_path, file_name)
            password = self.data.get("password")
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.setpassword(password.encode())
                for doc in data:
                    file_path = doc.get("directory")
                    file = doc.get("file")
                    zip_file.writestr(file_path, file)
            return True
        except:
            return False


# ---------------------------------------------------------------------------------------------------------


# Class to hash the password and verify the hashed password
# ---------------------------------------------------------------------------------------------------------
class Hash:
    def generateHashedPassword(password: str) -> str:
        hashed_password = pwd_context.hash(password)
        return hashed_password

    def verifyCredential(hashedPassword: str, userPassword: str):
        return pwd_context.verify(userPassword, hashedPassword)


# ---------------------------------------------------------------------------------------------------------


# This Class finds the size of all cache files present in the directory
# Also deletes the cache files
# ----------------------------------------------------------------------------------------------------------
class Cache:
    def __init__(self):
        self.path = os.getcwd()
        self.cacheFiles = []
        self.extensions = (".cache", ".json", ".tmp", ".pyc", ".bin")
        self.protectedFiles = (
            "Credentials.cache",
            "complements.json",
            "Grocery items.bin",
            "mili_rap_songs.json",
            "mili_songs.json",
            "poems.json",
            "riddles.json",
        )
        self.temporaryFiles = ("CAPTCHA.png", ".cache", ".google-cookie")
        self.cacheMemory = 0

    def CacheFiles(self, dir):
        all_files = os.listdir(dir)
        for file in all_files:
            file_dir = os.path.join(dir, file)
            if os.path.isfile(file_dir):
                extension = pathlib.Path(file_dir).suffix
                if extension in self.extensions and file not in self.protectedFiles:
                    self.cacheFiles.append(file_dir)
                elif file in self.temporaryFiles:
                    self.cacheFiles.append(file_dir)
            elif os.path.isdir(file_dir):
                self.CacheFiles(file_dir)

    def cacheMemorySize(self):
        self.CacheFiles(self.path)
        for file in self.cacheFiles:
            size = os.path.getsize(filename=file)
            self.cacheMemory += size
        self.cacheMemory = round(self.cacheMemory / 1024, 2)
        return self.cacheMemory

    def clearCacheMemory(self):
        self.CacheFiles(self.path)
        for file in self.cacheFiles:
            os.remove(file)

    def extractCacheFiles(self):
        self.CacheFiles(self.path)
        print("Cache files")
        for file in self.cacheFiles:
            print(file)


# ----------------------------------------------------------------------------------------------------------


# This class returns the appliction size of the assistant
# ----------------------------------------------------------------------------------------------------------
class ApplicationSize:
    def __init__(self):
        self.path = application_directory
        self.size = 0

    def readfiles(self, path):
        files = os.listdir(path)
        for file in files:
            dir = os.path.join(path, file)
            if os.path.isfile(dir):
                self.size += os.path.getsize(dir)
            else:
                self.readfiles(dir)

    def memory(self):
        self.readfiles(self.path)
        return round(self.size / (1024 * 1024), 2)


# ----------------------------------------------------------------------------------------------------------


class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mili")
        self.GUI_geometry()
        self.iconbitmap(application_directory + "\\Data\\Images\\GUI\\logo.ico")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.profileFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.profileFrame.grid(row=0, column=0, sticky="nsew")
        self.weatherFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.weatherFrame.grid(row=0, column=0, sticky="nsew")
        self.logFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.logFrame.grid(row=0, column=0, sticky="nsew")

        self.gameConsoleFrame = customtkinter.CTkFrame(
            self, fg_color="#252525", corner_radius=0
        )
        self.gameConsoleFrame.grid(row=0, column=0, sticky="nsew")

    # Function which return the ctk object of the image
    # url = file path, height = required height of image, width = required width of image
    # ---------------------------------------------------------------------------------------------------
    def ImageObject(self, url, height, width):
        img = Image.open(os.path.join(application_directory, url))
        img = customtkinter.CTkImage(img, size=(height, width))
        return img

    # ---------------------------------------------------------------------------------------------------

    # Function which sets the window in the center of screen
    # ---------------------------------------------------------------------------------------------------
    def GUI_geometry(self):
        w = 1100
        h = 650
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # ---------------------------------------------------------------------------------------------------

    # Function to  raise a frame in top level
    # ---------------------------------------------------------------------------------------------------
    def showFrame(self, frame):
        frame.tkraise()

    # ---------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------
    def Profile(self):
        # class to download the data
        # ----------------------------------------------------------------------------------------------------
        class request_model:
            def __init__(self):
                self.path = None
                self.account_data = None
                self.chats = None
                self.history = None

                self.frame = customtkinter.CTkFrame(
                    download_data_frame, fg_color="#FFF5EE", corner_radius=0
                )
                self.frame.grid(row=1, column=0, sticky="nsew")
                customtkinter.CTkLabel(
                    self.frame,
                    text="Download your data",
                    fg_color="#FFF5EE",
                    text_color="#111",
                    font=("Sitka Small", 16, "bold"),
                ).pack(side=TOP, anchor="center", pady=(30, 0))
                customtkinter.CTkLabel(
                    self.frame,
                    text="We'll download a file with your information. You can receive\nit in JSON, which may be easier to import to another service.",
                    fg_color="#FFF5EE",
                    text_color="#111",
                    font=("Sitka Small", 12, "normal"),
                ).pack(side=TOP, anchor="center")
                self.progress_bar = customtkinter.CTkProgressBar(
                    self.frame,
                    width=300,
                    height=15,
                    orientation="horizontal",
                    mode="determinate",
                    fg_color="#FFF5EE",
                    progress_color="#19b04f",
                )
                download_file_button = customtkinter.CTkButton(
                    self.frame,
                    text="Download",
                    corner_radius=5,
                    font=("Sitka Small", 15, "bold"),
                    height=40,
                    width=270,
                    text_color="#111",
                    fg_color="#1ed760",
                    border_color="#111",
                    hover_color="#19b04f",
                    command=lambda: Thread(target=self.download_path).start(),
                )
                download_file_button.pack(side=BOTTOM, anchor="center", pady=(0, 40))

            def download_account_data(self):
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                client = pymongo.MongoClient(self.url)
                db = client["Assistant"]
                collection = db["User Credentials"]
                data = collection.find_one({"email": gmail})
                self.progress_bar.set(0.3)
                self.account_data = data

            def download_chats(self):
                self.progress_bar.set(0.6)
                return None

            def download_history(self):
                self.progress_bar.set(0.8)
                return None

            def download_data(self):
                exit_button.configure(state="disable", hover=False)
                self.progress_bar.pack(side=TOP, anchor="center", pady=(30, 20))
                self.progress_bar.set(0)
                self.download_account_data()
                self.download_chats()
                self.download_history()
                confidence = Downloaded_Data(
                    self.account_data, self.chats, self.history, self.path
                ).createFile()
                if confidence is True:
                    messagebox.showwarning(
                        "Mili",
                        "Thankyou for using our services. Your data has been downloaded",
                    )
                    self.progress_bar.set(1)
                else:
                    messagebox.showwarning("Mili", "Network issue. Please try again.")

                exit_button.configure(
                    state="enable", hover=True, command=securityFrame.tkraise
                )
                download_userID.delete(0, END)

            def download_path(self):
                self.path = filedialog.askdirectory()
                if len(self.path) != 0:
                    exit_button.configure(state="disable", hover=False)
                    thread = Thread(target=self.download_data)
                    thread.start()
                    thread.join()

            def verify_credentials(self):
                if not Hash.verifyCredential(password, download_userID.get()):
                    messagebox.showwarning(
                        "Mili", "The password you entered is invalid. Please try again."
                    )
                else:
                    self.frame.tkraise()

        # -------------------------------------------------------------------------------------------------

        def showDownloadFrame():
            self.showFrame(downloadFrame)
            self.showFrame(download_verification_frame)

        # class for the application updates
        # -------------------------------------------------------------------------------------------------
        class Updates:
            def __init__(self) -> None:
                self.update_url = None
                self.file_size = None
                self.file_path = application_directory + "\\Data\\Cache\\Updates.hg"
                self.file_name = None

            # Checking update in the database
            # If update available then extracting the url of update package
            def checkupdate(self):
                url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                client = pymongo.MongoClient(url)
                db = client["Assistant"]
                collection = db["Updates"]
                doc = collection.find_one({"url_id": "647a5ffcbf4caa2ac124df88"})
                if doc is not None:
                    self.update_url = doc.get("url")

            # Storing update history and removing non required files
            def installation(self):
                data = {
                    "date": datetime.datetime.strftime(
                        datetime.datetime.now(), "%A %d %B, %Y"
                    ),
                    "time": datetime.datetime.strftime(
                        datetime.datetime.now(), "%I:%M %p"
                    ),
                    "file size": round(
                        (self.file_size / 1048576), 2
                    ),  # Size of update is in MB
                    "file_name": self.file_name,
                }
                if os.path.exists(self.file_path):
                    with open(self.file_path, "rb+") as file:
                        list = pickle.load(file)
                        list.append(data)
                        file.seek(0)
                        pickle.dump(list, file)
                        file.close()
                else:
                    with open(self.file_path, "wb") as file:
                        pickle.dump([data], file)
                        file.close()

            # Downloading the package
            def download_updates(self):
                progressBar.stop()
                progressBar.configure(mode="determinate")
                progressBar.set(0)
                data = 0
                chunk_size = 1048576
                progressLabel.configure(text=f"Downloading {data}%")
                progressLabel.pack_configure(anchor="ne")
                r = requests.get(url=self.update_url, stream=True)
                file_size = int(r.headers.get("Content-Length"))
                self.file_size = file_size
                self.file_name = self.update_url.split("/")[-1]
                with open(self.file_name, "wb") as fd:
                    for chunk in r.iter_content(chunk_size):
                        data += (100 * chunk_size) / file_size
                        progress_status = data / 100
                        progressBar.set(progress_status)
                        progressLabel.configure(
                            text=f"Downloading {int(round(data, 0))}%"
                        )
                        progressBar.update_idletasks()
                        fd.write(chunk)
                progressLabel.configure(text="Installing")

            def updateFiles(self):
                progressLabel.configure(text="Checking for updates...")
                progressBar.pack(side=TOP, anchor="nw")
                progressBar.start()
                updateButton.configure(
                    command=None,
                    fg_color="#393939",
                    border_color="#111",
                    border_width=1,
                    text_color="#111",
                    hover=False,
                )
                thread = Thread(target=self.checkupdate)
                thread.start()
                thread.join()
                try:
                    file_name = self.update_url.split("/")[-1]
                except:
                    file_name = None
                if self.update_url is None or os.path.exists(file_name):
                    progressLabel.configure(text="You are up to date")
                    progressBar.stop()
                    progressBar.pack_forget()
                    updateButton.configure(
                        command=lambda: Thread(target=Updates().updateFiles).start(),
                        fg_color="#1ed760",
                        text_color="#111",
                        hover_color="#19b04f",
                        border_width=0,
                    )
                else:
                    thread = Thread(target=self.download_updates)
                    thread.start()
                    thread.join()
                    installThread = Thread(target=self.installation)
                    installThread.start()
                    installThread.join()
                    progressLabel.configure(text=f"You are up to date")
                    progressLabel.pack_configure(anchor="nw")
                    updateButton.configure(
                        command=lambda: Thread(target=Updates().updateFiles).start(),
                        fg_color="#1ed760",
                        text_color="#111",
                        hover_color="#19b04f",
                        border_width=0,
                    )

        # Function for update history frame
        # --------------------------------------------------------------------------------------------------
        def updateHistory():
            scrollFrame = customtkinter.CTkScrollableFrame(
                updateHistoryFrame, fg_color="#252525", corner_radius=0, height=700
            )
            scrollFrame.pack(side=TOP, anchor="center", fill=BOTH)
            customtkinter.CTkButton(
                scrollFrame,
                fg_color="#911d5a",
                text_color="white",
                hover_color="#78184A",
                border_width=0,
                corner_radius=5,
                font=("Sitka Small", 13, "normal"),
                text="Back",
                height=32,
                width=60,
                command=lambda: self.showFrame(updatesFrame),
            ).pack(side=TOP, anchor="ne", padx=20, pady=20)

            if (
                os.path.exists(application_directory + "\\Data\\Cache\\Updates.hg")
                is False
            ):
                customtkinter.CTkLabel(
                    scrollFrame,
                    text="History Not Available",
                    fg_color="#252525",
                    text_color="#7f7f7f",
                    font=("Sitka Small", 50, "bold"),
                ).pack(side=TOP, anchor="center", pady=200)
            else:
                customtkinter.CTkLabel(
                    scrollFrame,
                    text="Updates",
                    fg_color="#252525",
                    text_color="#fff",
                    font=("Sitka Small", 15, "bold"),
                ).pack(side=TOP, anchor="w", padx=30, pady=(30, 20))
                with open(
                    application_directory + "\\Data\\Cache\\Updates.hg", "rb"
                ) as file:
                    data = pickle.load(file)
                for updates in data:
                    updateDataFrame = customtkinter.CTkFrame(
                        scrollFrame, fg_color="#175a99", corner_radius=5
                    )
                    updateDataFrame.pack(side=TOP, anchor="center", fill=X, padx=30)

            self.showFrame(updateHistoryFrame)

        # Function to traverse slider
        # --------------------------------------------------------------------------------------------------
        def traverse(arrayFrame, currentValue, flag):
            big_dot = self.ImageObject("Data\\Images\\Slider\\circle.png", 15, 15)
            if flag == 1:
                mode = currentValue.pop()
                mode = (mode + 1) % len(arrayFrame)
                currentValue.append(mode)
                self.showFrame(arrayFrame[mode])
            else:
                mode = currentValue.pop()
                mode = mode - 1
                if mode == -1:
                    mode = len(arrayFrame) - 1
                currentValue.append(mode)
                self.showFrame(arrayFrame[mode])
            dots = (dot_a, dot_b, dot_c, dot_d, dot_e, dot_f)
            for dot in dots:
                if dots.index(dot) == mode:
                    dot.configure(image=big_dot)
                else:
                    dot.configure(image=dot_image)

        # ------------------------------------------------------------------------------------------------

        # Function to clear cache memory
        # ------------------------------------------------------------------------------------------------
        def clearCacheMemory():
            Cache().clearCacheMemory()
            cacheSizeLabel.configure(text=f"{Cache().cacheMemorySize()} KB")

        # ------------------------------------------------------------------------------------------------

        # Class to handle settings values
        # ------------------------------------------------------------------------------------------------
        class SettingCommands:
            def __init__(self):
                pass

            def explicitCommandOption(self):
                with open(
                    application_directory + "\\Data\\Cache\\Mili Settings.settings",
                    "rb+",
                ) as file:
                    settingsData = pickle.load(file)
                    settingsData.update({"Explicit content": explicitContentVar.get()})
                    file.seek(0)
                    pickle.dump(settingsData, file)
                    file.close()

            def productEmailCommand(self):
                with open(
                    application_directory + "\\Data\\Cache\\Mili Settings.settings",
                    "rb+",
                ) as file:
                    settingsData = pickle.load(file)
                    settingsData.update({"Product emails": productEmailVar.get()})
                    file.seek(0)
                    pickle.dump(settingsData, file)
                    file.close()

        # ------------------------------------------------------------------------------------------------

        # Function to destroy window
        # ------------------------------------------------------------------------------------------------
        def destroy_window():
            self.destroy()

        # ------------------------------------------------------------------------------------------------

        # Class to reset the password
        # ------------------------------------------------------------------------------------------------
        class ResetPasswordBackend:
            def __init__(self):
                resetButtonVariable.set("Resetting...")
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]

            def model(self):
                current_password = resetCurrentPasswordEntry.get()
                new_password = resetNewPasswordEntry.get()
                previous_passwords = self.collection.find_one(
                    {"email": gmail}, {"previous_passwords": 1}
                ).get("previous_passwords")
                password_list = []
                for element in previous_passwords:
                    password_list.append(element.get("password"))
                if (
                    current_password is None
                    or new_password is None
                    or current_password == ""
                    or new_password == ""
                ):
                    messagebox.showwarning(
                        title="Mili",
                        message="The password fields for this app are unfilled.\nPlease enter a password in both fields to proceed.",
                    )
                    resetButtonVariable.set("Reset")
                else:
                    if current_password == new_password:
                        messagebox.showerror(
                            title="Mili",
                            message="Your password cannot be reused. Please choose a new password.",
                        )
                        resetButtonVariable.set("Reset")
                        return None
                    elif not Hash.verifyCredential(password, current_password):
                        messagebox.showerror(
                            title="Mili",
                            message="Please check your current password and try again.",
                        )
                        resetButtonVariable.set("Reset")
                        return None
                    for pwd in password_list:
                        if Hash.verifyCredential(pwd, new_password):
                            messagebox.showerror(
                                title="Mili",
                                message="Your password cannot be reused. Please choose a new password.",
                            )
                            resetButtonVariable.set("Reset")
                            return None
                    else:
                        new_hashed_password = Hash.generateHashedPassword(new_password)
                        previous_passwords.append(
                            {
                                "timestamp": datetime.datetime.timestamp(
                                    datetime.datetime.now()
                                ),
                                "password": password,
                            }
                        )
                        self.collection.update_one(
                            {"email": gmail},
                            {
                                "$set": {
                                    "password": new_hashed_password,
                                    "previous_passwords": previous_passwords,
                                }
                            },
                        )
                        CredentialManager().write_credential(gmail, new_hashed_password)
                        resetUpdateFrame.tkraise()
                        resetCurrentPasswordEntry.delete(0, END)
                        resetNewPasswordEntry.delete(0, END)
                resetButtonVariable.set("Reset Password")

        # ------------------------------------------------------------------------------------------------

        # Class to delete account
        # ------------------------------------------------------------------------------------------------
        class DeleteAccount:
            def __init__(self):
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]

            def deleteAccount(self):
                try:
                    self.collection.delete_one({"email": gmail})
                    messagebox.showinfo(
                        "Mili", "Your account has been deleted successfully"
                    )
                    CredentialManager().delete_credential()
                    destroy_window()
                except:
                    messagebox.showerror("Mili", "Connection error\nTry Again")

            def passwordConfirmation(self):
                enteredPassword = passwordEntry.get()
                value = agreeCheckBoxVar.get()
                if value == 0:
                    messagebox.showinfo("Mili", "Please accept self declaration")
                elif not Hash.verifyCredential(password, enteredPassword):
                    messagebox.showinfo("Mili", "You have entered incorrect password")
                else:
                    self.deleteAccount()

        # ------------------------------------------------------------------------------------------------

        # Class to edit profile
        # ------------------------------------------------------------------------------------------------
        class EditProfile:
            def __init__(self):
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]
                self.userName = None
                self.phoneNumber = None
                self.gender = None
                self.date = None
                self.month = None
                self.year = None
                self.email = gmail
                self.data = None
                self._DOB = None

            def updateDataBase(self):
                try:
                    self.collection.update_one(
                        {"email": self.email}, {"$set": self.data}
                    )
                    savingVar.set("Save Profile")
                    messagebox.showinfo(
                        "Mili", "You have sucessfully updated your profile"
                    )
                    if self.gender == "Male":
                        genderIcon = maleGenderIcon
                    elif self.gender == "Female":
                        genderIcon = femaleGenderIcon
                    else:
                        genderIcon = othersGenderIcon
                    genderLabel.configure(image=genderIcon)
                    userNameLabel.configure(text=self.userName)
                    contactNumberLabel.configure(text=self.phoneNumber)
                    DOB_Label.configure(
                        text=f'{datetime.datetime.strftime(self._DOB, "%B %d, %Y")}'
                    )
                except:
                    messagebox.showerror("Mili", "Connection error\nTry Again")

            def updateProfile(self):
                self.userName = userNameEntry.get()
                self.phoneNumber = contactNumberEntry.get()
                self.gender = genderVar.get()
                self.month = monthVar.get()
                self.date = dateEntry.get()
                self.year = yearEntry.get()
                if self.userName is None or self.userName == "":
                    messagebox.showwarning("Mili", "Please enter your name")
                elif self.phoneNumber is None or len(self.phoneNumber) != 10:
                    messagebox.showwarning("Mili", "Please enter valid phone number")
                elif self.gender is None or self.gender == "":
                    messagebox.showwarning("Mili", "Please select your gender")
                elif (
                    self.date is None
                    or len(self.date) > 2
                    or len(self.date) <= 0
                    or int(self.date) > 31
                ):
                    messagebox.showwarning("Mili", "Please enter valid date of birth")
                elif self.month is None or self.month == "":
                    messagebox.showwarning("Mili", "Please select month")
                elif self.year is None or len(self.year) != 4:
                    messagebox.showwarning("Mili", "Please enter valid year of birth")
                else:
                    try:
                        self._DOB = datetime.datetime.strptime(
                            f"{self.date} {self.month} {self.year}", "%d %B %Y"
                        )
                    except:
                        self._DOB = None
                    if self._DOB is None:
                        messagebox.showwarning(
                            "Mili", "Please enter valid Date of Birth"
                        )
                    else:
                        savingVar.set("Saving Profile")
                        self.data = {
                            "name": self.userName,
                            "phone number": self.phoneNumber,
                            "gender": self.gender,
                            "DOB": self._DOB,
                        }
                        thread = Thread(target=self.updateDataBase)
                        thread.start()

        # ------------------------------------------------------------------------------------------------

        # Function for Option
        # --------------------------------------------------------------------------------------------------

        def Options(mode):
            if mode == "Logout":
                response = messagebox.askquestion("Mili", "Are you confirmed?")
                if response == "yes":
                    flag = CredentialManager().delete_credential()
                    if flag is True:
                        self.destroy()
                    else:
                        messagebox.showerror(
                            "Mili",
                            "An error occurred during logout. Please try again later.",
                        )
            elif mode == "Edit Profile":
                self.showFrame(editProfileFrame)
            elif mode == "Delete Account":
                self.showFrame(deleteAccountFrame)
            elif mode == "Settings":
                self.showFrame(settingsFrame)
            elif mode == "Reset Password":
                self.showFrame(resetPasswordFrame)
            elif mode == "Updates":
                self.showFrame(updatesFrame)

        # --------------------------------------------------------------------------------------------------
        credentials = UserCredentials(None)
        ID = credentials.get("_id")
        gmail = credentials.get("email")
        userName = credentials.get("name")
        firstName = userName.split()[0]
        contactNumber = credentials.get("phone number")
        DOB = credentials.get("DOB")
        gender = credentials.get("gender")
        password = credentials.get("password")
        login_details = credentials.get("login_dates")
        last_login_location = credentials.get("last_login_location")
        last_login_device_model = credentials.get("last_login_device_model")
        last_login_coordinates = credentials.get("last_login_coordinates")
        last_login_date = credentials.get("last_login_date")

        # ---------------------------------------------------------------------------------------------------
        self.profileFrame.configure(fg_color="#252525")
        self.profileFrame.grid_columnconfigure(1, weight=1)
        self.profileFrame.grid_columnconfigure((2, 3), weight=0)
        self.profileFrame.grid_rowconfigure((0, 1, 2), weight=1)
        line_style = ttk.Style()
        line_style.configure("Line.TSeparator", background="#282828")

        # SideBar Frame-------------------------------------------------------------------------------------
        sidebar_frame = customtkinter.CTkFrame(
            self.profileFrame, width=200, fg_color="#171717", corner_radius=0
        )
        sidebar_frame.grid(row=0, column=0, sticky="nsew")
        sidebar_frame.grid_rowconfigure(5, weight=2)

        telebot_frame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        telebot_frame.grid(row=0, column=1, sticky="nsew")

        about_frame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        about_frame.grid(row=0, column=1, sticky="nsew")

        securityFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        securityFrame.grid(row=0, column=1, sticky="nsew")

        downloadFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        downloadFrame.grid(row=0, column=1, sticky="n", padx=200, pady=150)

        userFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        userFrame.grid(row=0, column=1, sticky="nsew")

        editProfileFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        editProfileFrame.grid(row=0, column=1, sticky="nsew")

        deleteAccountFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        deleteAccountFrame.grid(row=0, column=1, sticky="nsew")

        settingsFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        settingsFrame.grid(row=0, column=1, sticky="nsew")

        updatesFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        updatesFrame.grid(row=0, column=1, sticky="nsew")

        updateHistoryFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#252525", corner_radius=0
        )
        updateHistoryFrame.grid(row=0, column=1, sticky="nsew")

        resetPasswordFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#FDB0C0", corner_radius=0
        )
        resetPasswordFrame.grid(row=0, column=1, sticky="nsew")
        resetUpdateFrame = customtkinter.CTkFrame(
            self.profileFrame, fg_color="#FDB0C0", corner_radius=0
        )
        resetUpdateFrame.grid(row=0, column=1, sticky="nsew")

        # SideBar FrameCode----------------------------------------------------------------------------------

        customtkinter.CTkLabel(
            sidebar_frame,
            fg_color="#171717",
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\logo.png", 130, 130),
        ).grid(row=0, column=0, sticky="nsew", padx=15, pady=(10, 30))
        profile_button = customtkinter.CTkButton(
            sidebar_frame,
            corner_radius=5,
            height=35,
            image=self.ImageObject("Data\\Images\\GUI\\homeRevert.png", 17, 17),
            text="Profile",
            compound="left",
            anchor="w",
            fg_color="#171717",
            font=("Sitka Small", 14, "bold"),
            hover_color="#252525",
            command=lambda: self.showFrame(userFrame),
        )
        profile_button.grid(row=1, column=0, sticky="n")
        security_button = customtkinter.CTkButton(
            sidebar_frame,
            corner_radius=5,
            height=35,
            image=self.ImageObject("Data\\Images\\GUI\\privacyRevert.png", 17, 17),
            text="Security",
            compound="left",
            anchor="w",
            fg_color="#171717",
            font=("Sitka Small", 14, "bold"),
            hover_color="#252525",
            command=lambda: self.showFrame(securityFrame),
        )
        security_button.grid(row=2, column=0, sticky="n")
        about_button = customtkinter.CTkButton(
            sidebar_frame,
            corner_radius=5,
            height=35,
            image=self.ImageObject("Data\\Images\\GUI\\aboutRevert.png", 17, 17),
            text="About",
            compound="left",
            anchor="w",
            fg_color="#171717",
            font=("Sitka Small", 14, "bold"),
            hover_color="#252525",
            command=lambda: self.showFrame(about_frame),
        )
        about_button.grid(row=3, column=0, sticky="n")
        teleBot_button = customtkinter.CTkButton(
            sidebar_frame,
            corner_radius=5,
            height=35,
            image=self.ImageObject("Data\\Images\\GUI\\telegram icon.png", 17, 17),
            text="Mili Bot",
            compound="left",
            anchor="w",
            fg_color="#171717",
            font=("Sitka Small", 14, "bold"),
            hover_color="#252525",
            command=lambda: self.showFrame(telebot_frame),
        )
        teleBot_button.grid(row=4, column=0, sticky="n")

        # teleBotFrame --------------------------------------------------------------------------------------

        teleBot_text_Frame = customtkinter.CTkFrame(
            telebot_frame, fg_color="#252525", corner_radius=0
        )
        teleBot_text_Frame.grid(row=0, column=0, sticky="new", pady=30)
        t1 = "Hello there, I am your new personal assistant. My name is Mili. I'm here to help you with anything you need,      \n"
        t2 = "from managing your desires to answering your questions My goal is to provide you with a seamless experience.   \n"
        t3 = "I'm designed to understand natural language, so you can talk to me like you would with any other person. To get \n"
        t4 = "started, just say Hey and tell me what you need. From there, I'll take care of rest. And don't worry, I'm always    \n"
        t5 = "learning and improving, so I'll be better tomorrow tahn I am today.                                                                                \n"
        botIntroduction = t1 + t2 + t3 + t4 + t5
        customtkinter.CTkLabel(
            teleBot_text_Frame,
            text=botIntroduction,
            fg_color="#252525",
            text_color="#848488",
            font=("Sitka Small", 11),
        ).grid(row=0, column=0, sticky="n", padx=157)
        telebotRegisterFrame = customtkinter.CTkFrame(
            telebot_frame, fg_color="#252525", corner_radius=0
        )
        telebotRegisterFrame.grid(row=1, column=0, sticky="n", pady=(10, 235))
        customtkinter.CTkLabel(
            telebotRegisterFrame,
            text="Register by using your Chat Id",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13),
        ).grid(row=0, column=0, columnspan=2, sticky="n")
        chatId_input = customtkinter.CTkEntry(
            telebotRegisterFrame,
            placeholder_text="Chat Id",
            placeholder_text_color="#848488",
            font=("Sitka Small", 16, "normal"),
            fg_color="#171717",
            text_color="#fff",
            corner_radius=5,
            border_width=0,
            width=200,
            height=40,
        )
        chatId_input.grid(row=1, column=0, sticky="s", padx=15)
        chatIDButton = customtkinter.CTkButton(
            telebotRegisterFrame,
            width=200,
            text="Continue",
            height=40,
            border_width=0,
            corner_radius=5,
            font=("Sitka Small", 17, "bold"),
            bg_color="transparent",
            fg_color="#1ed760",
            hover_color="#19b04f",
            text_color="#111",
        )
        chatIDButton.grid(row=2, column=0, sticky="n", pady=15, padx=15)
        customtkinter.CTkLabel(
            telebotRegisterFrame,
            image=self.ImageObject("Data\\Images\\GUI\\QR Code.png", 200, 200),
            text="",
            fg_color="#252525",
        ).grid(row=1, column=1, rowspan=2, padx=15, pady=10)

        # About Mili Frame----------------------------------------------------------------------------------

        contentframe = customtkinter.CTkScrollableFrame(
            about_frame, fg_color="#252525", height=700
        )
        contentframe.pack(side="top", anchor="center", fill="both")
        customtkinter.CTkLabel(
            contentframe,
            text=f"What can I do for you {firstName}?",
            fg_color="#252525",
            text_color="#fff",
            font=("Cooper Black", 20),
            anchor="center",
        ).grid(row=0, column=0, sticky="n", pady=20, padx=310)
        ttk.Separator(contentframe, orient="horizontal", style="Line.TSeparator").grid(
            row=2, column=0, sticky="nsew"
        )
        customtkinter.CTkLabel(
            contentframe,
            text="About these suggestions?",
            fg_color="#252525",
            text_color="#848488",
            font=("Sitka Small", 10),
            anchor="center",
        ).grid(row=3, column=0, sticky="n")
        sliderFrame = customtkinter.CTkFrame(
            contentframe, fg_color="#252525", corner_radius=0
        )
        sliderFrame.grid(row=4, column=0, sticky="n", pady=30)
        sliderContentFrame = customtkinter.CTkFrame(
            sliderFrame, fg_color="#252525", corner_radius=0
        )
        sliderContentFrame.grid(row=0, column=1, sticky="n")
        slide_one_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_one_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_one_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\music.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(row=0, column=0, sticky="nsew", rowspan=2)
        slidertext_one = "From romantic zone to              \nparty songs Enjoy your              \nfavorite music using your voice"
        customtkinter.CTkLabel(
            slide_one_Frame,
            text=slidertext_one,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(10, 0))
        customtkinter.CTkLabel(
            slide_one_Frame,
            text="“Hey Mili play Kesariya”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(10, 0))

        slide_two_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_two_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_two_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\women.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(row=0, column=0, sticky="nsew", rowspan=2)
        slidertext_two = "Open your favorite apps\nand websites by voice   "
        customtkinter.CTkLabel(
            slide_two_Frame,
            text=slidertext_two,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(10, 14))
        customtkinter.CTkLabel(
            slide_two_Frame,
            text="“Just say open Spotify”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(10, 14))

        slide_three_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_three_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_three_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\order.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(row=0, column=0, sticky="nsew", rowspan=2)
        slidertext_three = "Indulge in rasgullas from     \nKolkata or homemade          \nghewar from Rajasthan, and\nshare some sweetness         \nwith the ones you love.       "
        customtkinter.CTkLabel(
            slide_three_Frame,
            text=slidertext_three,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(10, 10))
        customtkinter.CTkLabel(
            slide_three_Frame,
            text="“Where to eat ghewar?”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(10, 10))

        slide_four_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_four_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_four_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\cooking.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(row=0, column=0, sticky="nsew", rowspan=2)
        slidertext_four = "Find the perfect at-home\nsnack with simple and    \neasy pav bhaji, biryani,   \nor jalebi recipes.             "
        customtkinter.CTkLabel(
            slide_four_Frame,
            text=slidertext_four,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(10, 13))
        customtkinter.CTkLabel(
            slide_four_Frame,
            text="“Show me vada pav       \nrecipes on YouTube”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(10, 13))

        slide_five_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_five_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_five_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\translate.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(row=0, column=0, sticky="nsew", rowspan=2)
        slidertext_five = "With us, language diferences\nare not exceptional. From      \nenglish to hindi, bengali to    \nmarathi, almost every           \nlanguage translated.             "
        customtkinter.CTkLabel(
            slide_five_Frame,
            text=slidertext_five,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(10, 30))
        customtkinter.CTkLabel(
            slide_five_Frame,
            text="“Translate,How are\nyou? in Marathi”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(10, 30))

        slide_six_Frame = customtkinter.CTkFrame(
            sliderContentFrame, fg_color="#252525", corner_radius=0
        )
        slide_six_Frame.grid(row=0, column=0, sticky="n")
        customtkinter.CTkLabel(
            slide_six_Frame,
            image=self.ImageObject("Data\\Images\\Slider\\movies.png", 250, 250),
            text="",
            fg_color="#252525",
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            rowspan=2,
        )
        slidertext_six = "Discover the    \nperfect comedy\nor drama          "
        customtkinter.CTkLabel(
            slide_six_Frame,
            text=slidertext_six,
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#7f7f7f",
            font=("Sitka Small", 12),
        ).grid(row=0, column=1, sticky="sw", pady=(0, 15), padx=(25, 85))
        customtkinter.CTkLabel(
            slide_six_Frame,
            text="“Best movies\nof all time”",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=1, sticky="nw", padx=(25, 85))
        sliderArrayFrame = (
            slide_six_Frame,
            slide_one_Frame,
            slide_two_Frame,
            slide_three_Frame,
            slide_four_Frame,
            slide_five_Frame,
        )
        currentValue = [0]
        customtkinter.CTkButton(
            sliderFrame,
            text="",
            width=40,
            height=40,
            image=self.ImageObject("Data\\Images\\Slider\\left button.png", 20, 20),
            fg_color="#252525",
            hover_color="#404040",
            command=lambda: traverse(sliderArrayFrame, currentValue, 0),
        ).grid(row=0, column=0, padx=30)
        customtkinter.CTkButton(
            sliderFrame,
            text="",
            width=40,
            height=40,
            image=self.ImageObject("Data\\Images\\Slider\\right button.png", 20, 20),
            fg_color="#252525",
            hover_color="#404040",
            command=lambda: traverse(sliderArrayFrame, currentValue, 1),
        ).grid(row=0, column=2, padx=30)

        dotFrame = customtkinter.CTkFrame(
            sliderFrame, fg_color="#252525", corner_radius=0
        )
        dotFrame.grid(row=1, column=1, sticky="n", pady=10)
        dot_image = self.ImageObject("Data\\Images\\Slider\\circle.png", 10, 10)
        dot_a = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_a.grid(row=0, column=0, sticky="n", padx=3)
        dot_b = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_b.grid(row=0, column=1, sticky="n", padx=3)
        dot_c = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_c.grid(row=0, column=2, sticky="n", padx=3)
        dot_d = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_d.grid(row=0, column=3, sticky="n", padx=3)
        dot_e = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_e.grid(row=0, column=4, sticky="n", padx=3)
        dot_f = customtkinter.CTkLabel(
            dotFrame, text="", image=dot_image, bg_color="#252525"
        )
        dot_f.grid(row=0, column=5, sticky="n", padx=3)
        # -------------------------------------------------------------------------------------------

        # Table Frame 1
        # -------------------------------------------------------------------------------------------

        customtkinter.CTkLabel(
            contentframe,
            text="What I can do",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 15),
        ).grid(row=5, column=0, sticky="nw", padx=80)
        tableFrame1 = customtkinter.CTkFrame(
            contentframe, fg_color="#111", corner_radius=5
        )
        tableFrame1.grid(row=6, column=0, sticky="nsew", padx=80, pady=10)
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\chrome.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Open apps and website",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=0, column=0, sticky="w", padx=20, rowspan=2, pady=5)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Open your favorite apps and websites by voice",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=0, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1, text="Open Spotify", fg_color="#111", text_color="orange"
        ).grid(row=1, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=3
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\bluetooth.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Ask Mili to enable or disable bluetooth",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=3, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Mili turn on bluetooth",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=3, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1, text="Turn on bluetooth", fg_color="#111", text_color="orange"
        ).grid(row=4, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=5, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\music.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Ask Mili to play songs",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=6, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Play your favorite songs by voice",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=6, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1, text="Play song Kesariya", fg_color="#111", text_color="orange"
        ).grid(row=7, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=8, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\chatting.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Message",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=9, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Send messages to your're, loved one",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=9, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1,
            text="Send 'Hii, How are you?' to Karan",
            fg_color="#111",
            text_color="orange",
        ).grid(row=10, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=11, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\translate.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Translate",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=12, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Connect with people, places, and cultures without language barriers",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=12, column=1, sticky="sw", padx=(0, 35))
        customtkinter.CTkLabel(
            tableFrame1,
            text="Translate Hola in Marathi",
            fg_color="#111",
            text_color="orange",
        ).grid(row=13, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=14, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\map.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Map",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=15, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Ask nearby places from Mili",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=15, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1,
            text="Any chinese restaurants nearby me",
            fg_color="#111",
            text_color="orange",
        ).grid(row=16, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=17, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\google.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Google Search",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=18, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Search hands free using your voice",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=18, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1,
            text="what is the longest word in english",
            fg_color="#111",
            text_color="orange",
        ).grid(row=19, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=20, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\camera.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Camera",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=21, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Take hands free selfies using your voice",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=21, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1,
            text="Hey Mili, take my selfie",
            fg_color="#111",
            text_color="orange",
        ).grid(row=22, column=1, sticky="nw")
        ttk.Separator(tableFrame1, orient="horizontal", style="Line.TSeparator").grid(
            row=23, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame1,
            image=self.ImageObject("Data\\Images\\GUI\\clock.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Clock",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=24, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame1,
            text="Set Alarm and Timers",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=24, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame1,
            text="Set alarm at 8:00 am morning",
            fg_color="#111",
            text_color="orange",
        ).grid(row=25, column=1, sticky="nw")
        # ---------------------------------------------------------------------------------------------------------

        # Table Frame 2
        # ---------------------------------------------------------------------------------------------------------

        customtkinter.CTkLabel(
            contentframe,
            text="What's New For You",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 15),
        ).grid(row=7, column=0, sticky="nw", padx=80, pady=(40, 0))
        tableFrame2 = customtkinter.CTkFrame(
            contentframe, fg_color="#111", corner_radius=5
        )
        tableFrame2.grid(row=8, column=0, sticky="nsew", padx=80, pady=10)
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\calculator.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Calculation",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=0, column=0, sticky="w", padx=(20, 200), rowspan=2, pady=5)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Ask Mili to make calculations for you",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=0, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="What is the cube root of 27",
            fg_color="#111",
            text_color="orange",
        ).grid(row=1, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=3
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\cloudy-day.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Weather",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=3, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Get weather forcast and updates",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=3, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="What's the weather of haridwar today?",
            fg_color="#111",
            text_color="orange",
        ).grid(row=4, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=5, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\news.png", 30, 30),
            font=("Sitka Small", 13),
            text="       News",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=6, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Get the latest news from sources you trust",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=6, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2, text="Play today's news", fg_color="#111", text_color="orange"
        ).grid(row=7, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=8, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\movies.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Movies",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=9, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Discover the perfect comedy or drama",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=9, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Best movies of all time",
            fg_color="#111",
            text_color="orange",
        ).grid(row=10, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=11, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\Youtube Music.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Youtube music",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=12, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Play your favourite songs on Youtube Music",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=12, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Play Imagine Dragons on Youtube Music",
            fg_color="#111",
            text_color="orange",
        ).grid(row=13, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=14, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\vegetable.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Groceries",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=15, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="The simplest way to keep your grocery list synchronized",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=15, column=1, padx=(0, 100), sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Add milk and bread in my Grocery List",
            fg_color="#111",
            text_color="orange",
        ).grid(row=16, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=17, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\gmail.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Gmail",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=18, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Get the information about important mails",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=18, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Show my important mails",
            fg_color="#111",
            text_color="orange",
        ).grid(row=19, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=20, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\insta.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Instagram",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=21, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Get the information about posts of your favoutite celebrity",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=21, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Show Selena Gomez on Instagram",
            fg_color="#111",
            text_color="orange",
        ).grid(row=22, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=23, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\sunset.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Sunrise & Sunset",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=24, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Lookup the time for sunrise and sunset",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=24, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="when is sunset in Dehradun?",
            fg_color="#111",
            text_color="orange",
        ).grid(row=25, column=1, sticky="nw")
        ttk.Separator(tableFrame2, orient="horizontal", style="Line.TSeparator").grid(
            row=23, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame2,
            image=self.ImageObject("Data\\Images\\GUI\\reminder.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Reminders",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=24, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame2,
            text="Create reminders for tasks",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=24, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame2,
            text="Set reminder to call Mira after 30 minutes",
            fg_color="#111",
            text_color="orange",
        ).grid(row=25, column=1, sticky="nw")
        # -------------------------------------------------------------------------------------------------------

        # Table Frame 3
        # -------------------------------------------------------------------------------------------------------

        customtkinter.CTkLabel(
            contentframe,
            text="For Nostalgics",
            fg_color="#252525",
            anchor="w",
            compound="left",
            text_color="#fff",
            font=("Sitka Small", 15),
        ).grid(row=9, column=0, sticky="nw", padx=80, pady=(40, 0))
        tableFrame3 = customtkinter.CTkFrame(
            contentframe, fg_color="#111", corner_radius=5
        )
        tableFrame3.grid(row=10, column=0, sticky="nsew", padx=80, pady=10)
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\chat.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Chat with your assistant",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=0, column=0, sticky="w", padx=(20, 120), rowspan=2, pady=5)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Feeling bore? Chat with your assistant",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=0, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3, text="Can you dance", fg_color="#111", text_color="orange"
        ).grid(row=1, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=3
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\magnifier.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Fun Facts",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=3, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Your Mili Assistant knows thousand of interesting fun facts",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=3, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3, text="Joke", fg_color="#111", text_color="orange"
        ).grid(row=4, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=5, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\quotes.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Motivational Quotes",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=6, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Hear what successful people have said with Quotes",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=6, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="Tell me some motivational quotes",
            fg_color="#111",
            text_color="orange",
        ).grid(row=7, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=8, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\poems.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Poems",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=9, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="A large, lyrical collection of melodic poems",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=9, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3, text="Sing me a poem", fg_color="#111", text_color="orange"
        ).grid(row=10, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=11, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\thinking.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Question of the day",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=12, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Every day, Question of the Day poses a new trivia question for you",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=12, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="What is the Question of the Day",
            fg_color="#111",
            text_color="orange",
        ).grid(row=13, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=14, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\bedtime.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Classic Stories",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=15, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Enjoy classic short stories like The Snow Queen",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=15, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="Tell me a bed time story",
            fg_color="#111",
            text_color="orange",
        ).grid(row=16, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=17, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\youtube.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Youtube",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=18, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Top musics on Youtube",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=18, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="Play Calm Down on Youtube",
            fg_color="#111",
            text_color="orange",
        ).grid(row=19, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=20, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\conversions.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Unit Conversions",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=21, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Get conversions of global currencies and units",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=21, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="How many ounces are in a cup?",
            fg_color="#111",
            text_color="orange",
        ).grid(row=22, column=1, sticky="nw")
        ttk.Separator(tableFrame3, orient="horizontal", style="Line.TSeparator").grid(
            row=23, column=0, columnspan=2, sticky="nsew", pady=5
        )
        customtkinter.CTkLabel(
            tableFrame3,
            image=self.ImageObject("Data\\Images\\GUI\\spotify.png", 30, 30),
            font=("Sitka Small", 13),
            text="       Spotify",
            fg_color="#111",
            text_color="#fff",
            compound="left",
            anchor="nw",
        ).grid(row=24, column=0, sticky="w", padx=20, rowspan=2)
        customtkinter.CTkLabel(
            tableFrame3,
            text="Play your favourite playlists on Spotify",
            fg_color="#111",
            text_color="#7f7f7f",
        ).grid(row=24, column=1, sticky="sw")
        customtkinter.CTkLabel(
            tableFrame3,
            text="Play the playlist Pop Songs?",
            fg_color="#111",
            text_color="orange",
        ).grid(row=25, column=1, sticky="nw")

        customtkinter.CTkLabel(
            contentframe,
            text="Make life easier with a little help from our Assistant",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 15, "bold"),
        ).grid(row=11, column=0, sticky="n", pady=(70, 0))
        customtkinter.CTkLabel(
            contentframe,
            text="*Requires internet connection",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 11, "italic"),
        ).grid(row=12, column=0, sticky="nw", pady=5, padx=80)
        aboutUsFooterFrame = customtkinter.CTkFrame(
            contentframe, fg_color="#252525", corner_radius=0
        )
        aboutUsFooterFrame.grid(row=13, column=0, sticky="nw", padx=80, pady=10)
        customtkinter.CTkButton(
            aboutUsFooterFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\instagram.png", 30, 30),
            fg_color="#252525",
            width=25,
            hover=False,
            command=lambda: webbrowser.open_new_tab("https://www.instagram.com/miliassistant/"),
        ).grid(row=0, column=0, sticky="n", padx=(0, 15))
        customtkinter.CTkButton(
            aboutUsFooterFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\twitter.png", 30, 30),
            fg_color="#252525",
            width=25,
            hover=False,
        ).grid(row=0, column=1, sticky="n", padx=(0, 15))
        customtkinter.CTkButton(
            aboutUsFooterFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\github.png", 30, 30),
            fg_color="#252525",
            width=25,
            hover=False,
            command=lambda : webbrowser.open_new_tab(
                "https://github.com/Shivamrai15/Mili-Assistant"
            ),
        ).grid(row=0, column=2, sticky="n", padx=(0, 15))
        customtkinter.CTkLabel(
            contentframe,
            text="Copyright © 2022-2023 Mili",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=14, column=0, sticky="n", pady=(10, 40))

        # ---------------------------------------------------------------------------------------------------

        # Download user data frame
        # ---------------------------------------------------------------------------------------------------

        download_data_frame = customtkinter.CTkFrame(
            downloadFrame, fg_color="#FFF5EE", corner_radius=0
        )
        download_data_frame.grid(row=0, column=0, sticky="n")
        exitFrame = customtkinter.CTkFrame(
            download_data_frame, fg_color="#f2e0d3", corner_radius=0
        )
        exitFrame.grid(row=0, column=0, sticky="nsew")
        exit_button = customtkinter.CTkButton(
            exitFrame,
            text="X",
            font=("Sitka Small", 17, "bold"),
            width=40,
            corner_radius=0,
            fg_color="#f2e0d3",
            text_color="black",
            hover_color="red",
            command=lambda: self.showFrame(securityFrame),
        )
        exit_button.pack(side=TOP, anchor="e")
        download_verification_frame = customtkinter.CTkFrame(
            download_data_frame, fg_color="#FFF5EE", corner_radius=0
        )
        download_verification_frame.grid(row=1, column=0, sticky="nsew")
        customtkinter.CTkLabel(
            download_verification_frame,
            text="Enter Your Mili Password",
            fg_color="#FFF5EE",
            text_color="#111",
            font=("Sitka Small", 16, "bold"),
        ).pack(side=TOP, anchor="w", padx=64, pady=(30, 40))
        download_userID = customtkinter.CTkEntry(
            download_verification_frame,
            fg_color="#FFF5EE",
            border_width=2,
            border_color="#111",
            height=40,
            width=270,
            corner_radius=5,
            placeholder_text="Password",
            show="\U00002022",
            font=("Sitka Small", 15, "bold"),
            placeholder_text_color="#7f7f7f",
            text_color="#111",
        )
        download_userID.pack(side=TOP, anchor="center", padx=64)
        verifyCredential_button = customtkinter.CTkButton(
            download_verification_frame,
            text="Request Download",
            corner_radius=5,
            font=("Sitka Small", 15, "normal"),
            height=40,
            width=270,
            text_color="#111",
            fg_color="#1ed760",
            border_color="#111",
            hover_color="#19b04f",
            command=request_model().verify_credentials,
        )
        verifyCredential_button.pack(side=TOP, anchor="center", pady=5, padx=64)
        customtkinter.CTkButton(
            download_verification_frame,
            text="Forget your password?",
            corner_radius=5,
            font=("Sitka Small", 12, "normal"),
            text_color="#19b04f",
            fg_color="#FFF5EE",
            hover=False,
        ).pack(side=TOP, anchor="w", padx=64, pady=(5, 37))

        # ---------------------------------------------------------------------------------------------------

        # Security Frame
        # ---------------------------------------------------------------------------------------------------

        securityScrollableFrame = customtkinter.CTkScrollableFrame(
            securityFrame, height=650, fg_color="#252525"
        )
        securityScrollableFrame.pack(side=TOP, anchor="center", fill="both")

        customtkinter.CTkLabel(
            securityScrollableFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\security.png", 375, 250),
            fg_color="#252525",
        ).pack(side=TOP, anchor=CENTER, pady=20)

        securityMainFrame = customtkinter.CTkFrame(
            securityScrollableFrame, fg_color="#202020"
        )
        securityMainFrame.pack(side=TOP, anchor=CENTER, padx=100, fill=X)
        customtkinter.CTkLabel(
            securityMainFrame,
            text="You currently logged in the device",
            text_color="#fff",
            font=("Sitka Small", 15, "bold"),
        ).pack(side=TOP, anchor="w", padx=20, pady=(20, 10))

        last_login_frame = customtkinter.CTkFrame(securityMainFrame, fg_color="#202020")
        last_login_frame.pack(side=LEFT, anchor="w", pady=(0, 20), fill=X)
        customtkinter.CTkLabel(
            last_login_frame,
            text="Laptop Name",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=0, column=0, sticky="w", padx=20)
        customtkinter.CTkLabel(
            last_login_frame,
            text=f"{last_login_device_model}",
            text_color="#1ed760",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=0, column=1, sticky="w", padx=0)
        customtkinter.CTkLabel(
            last_login_frame,
            text="Time",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=1, column=0, sticky="w", padx=20)
        customtkinter.CTkLabel(
            last_login_frame,
            text=f'{datetime.datetime.strftime(last_login_date, "%d %B, %Y %I:%M %p")}',
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=1, column=1, sticky="w", padx=0)
        customtkinter.CTkLabel(
            last_login_frame,
            text="Location",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=2, column=0, sticky="w", padx=20)
        customtkinter.CTkLabel(
            last_login_frame,
            text=f"{last_login_location}",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=2, column=1, sticky="w", padx=0)

        customtkinter.CTkButton(
            securityMainFrame,
            text="Navigate to the location",
            text_color="#1ed760",
            height=130,
            width=200,
            image=self.ImageObject("Data\\Images\\GUI\\compass.png", 70, 70),
            font=("Sitka Small", 13, "bold"),
            fg_color="#202020",
            hover_color="#252525",
            compound="top",
            command=lambda: webbrowser.open_new_tab(
                f"https://www.google.com/maps/search/?api=1&query={last_login_coordinates[0]},{last_login_coordinates[1]}"
            ),
        ).pack(side=RIGHT, anchor="ne", padx=40, pady=(0, 20))

        customtkinter.CTkLabel(
            securityScrollableFrame,
            text="Your Devices",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 18, "bold"),
        ).pack(side=TOP, anchor=CENTER, pady=(50, 0))
        customtkinter.CTkLabel(
            securityScrollableFrame,
            text="Where you're signed in",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 12, "normal"),
        ).pack(side=TOP, anchor=CENTER, pady=(0, 30))
        securityTableFrame = customtkinter.CTkScrollableFrame(
            securityScrollableFrame, fg_color="#111", height=300
        )
        securityTableFrame.pack(side=TOP, anchor=CENTER, fill=X, padx=100)
        for row, docs in enumerate(login_details):
            customtkinter.CTkLabel(
                securityTableFrame,
                text="",
                image=self.ImageObject("Data\\Images\\GUI\\laptop.png", 80, 80),
                fg_color="#111",
            ).grid(row=row, column=0, sticky="nsew", padx=60)
            temporaryFrame = customtkinter.CTkFrame(
                securityTableFrame,
                fg_color="#111",
                border_color="#7f7f7f",
                border_width=2,
                corner_radius=10,
            )
            temporaryFrame.grid(
                row=row, column=1, sticky="nsew", padx=(30, 85), pady=10
            )
            customtkinter.CTkLabel(
                temporaryFrame,
                text=f"Device : {docs.get('device')}",
                fg_color="#111",
                text_color="#fff",
                font=("Sitka Small", 12, "normal"),
            ).grid(row=0, column=0, sticky="w", padx=20, pady=(5, 0))
            customtkinter.CTkLabel(
                temporaryFrame,
                text=f'Date : {datetime.datetime.strftime(docs.get("time"), "%B %d, %Y")}',
                fg_color="#111",
                text_color="#fff",
                font=("Sitka Small", 12, "normal"),
            ).grid(row=1, column=0, sticky="w", padx=20)
            customtkinter.CTkLabel(
                temporaryFrame,
                text=f'Time : {datetime.datetime.strftime(docs.get("time"), "%I:%M %p")}',
                fg_color="#111",
                text_color="#fff",
                font=("Sitka Small", 12, "normal"),
            ).grid(row=2, column=0, sticky="w", padx=20)
            customtkinter.CTkLabel(
                temporaryFrame,
                text=f"IP : {docs.get('ip_address')}",
                fg_color="#111",
                text_color="#fff",
                font=("Sitka Small", 12, "normal"),
            ).grid(row=3, column=0, sticky="w", pady=(0, 5), padx=20)
        customtkinter.CTkLabel(
            securityScrollableFrame,
            text="When you use our services, you’re trusting us with your information. We understand that this is a big responsibility \nand we work hard to protect your information and put you in control.",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 12, "normal"),
        ).pack(side=TOP, anchor=CENTER, pady=20)
        securityFooterFrame = customtkinter.CTkFrame(
            securityScrollableFrame, fg_color="#171717", corner_radius=12
        )
        securityFooterFrame.pack(side=TOP, anchor=CENTER, pady=(5, 30))
        customtkinter.CTkLabel(
            securityFooterFrame,
            text=f'Effective Date : {datetime.datetime.strftime(datetime.datetime.now(), "%B %d, %Y")}',
            fg_color="#171717",
            text_color="#fff",
            font=("Sitka Small", 12, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=15, pady=5)
        customtkinter.CTkButton(
            securityFooterFrame,
            text=f"DOWNLOAD DATA",
            fg_color="#171717",
            text_color="#1ed760",
            font=("Sitka Small", 12, "bold"),
            hover=False,
            command=showDownloadFrame,
        ).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # --------------------------------------------------------------------------------------------------

        # UserProfile Frame
        # --------------------------------------------------------------------------------------------------
        customtkinter.CTkOptionMenu(
            userFrame,
            fg_color="#171717",
            button_color="#111",
            button_hover_color="#404040",
            values=[
                "Logout",
                "Edit Profile",
                "Reset Password",
                "Delete Account",
                "Updates",
                "Settings",
            ],
            font=("Sitka Small", 14, "normal"),
            dropdown_font=("Sitka Small", 14, "normal"),
            dropdown_fg_color="#171717",
            command=Options,
        ).grid(row=0, column=0, pady=10, padx=(760, 10))
        maleGenderIcon = self.ImageObject("Data\\Images\\GUI\\man.png", 150, 150)
        femaleGenderIcon = self.ImageObject("Data\\Images\\GUI\\woman.png", 150, 150)
        othersGenderIcon = self.ImageObject("Data\\Images\\GUI\\question.png", 150, 150)
        if gender == "Male":
            genderIcon = maleGenderIcon
        elif gender == "Female":
            genderIcon = femaleGenderIcon
        else:
            genderIcon = othersGenderIcon
        profileHeaderFrame = customtkinter.CTkFrame(userFrame, fg_color="#252525")
        profileHeaderFrame.grid(row=1, column=0, sticky="n")
        genderLabel = customtkinter.CTkLabel(
            profileHeaderFrame, text="", image=genderIcon, fg_color="#252525"
        )
        genderLabel.grid(row=0, column=0, rowspan=2, sticky="nsew")
        customtkinter.CTkLabel(
            profileHeaderFrame,
            text="PROFILE",
            fg_color="#252525",
            text_color="#fff",
            font=("Cooper Black", 12, "bold"),
        ).grid(row=0, column=1, sticky="sw", padx=(15, 0))
        userNameLabel = customtkinter.CTkLabel(
            profileHeaderFrame,
            text=f"{userName}",
            fg_color="#252525",
            text_color="#fff",
            font=("Cooper Black", 50, "bold"),
        )
        userNameLabel.grid(row=1, column=1, sticky="nw", padx=(15, 0))
        profileMainFrame = customtkinter.CTkFrame(userFrame, fg_color="#252525")
        profileMainFrame.grid(row=2, column=0, sticky="n", pady=(60, 50))
        customtkinter.CTkLabel(
            profileMainFrame,
            text="Username",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 30))
        customtkinter.CTkLabel(
            profileMainFrame,
            text=f"{ID}",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 14, "bold"),
        ).grid(row=0, column=1, sticky="w")
        ttk.Separator(
            profileMainFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=2, column=0, columnspan=2, sticky="nsew")
        customtkinter.CTkLabel(
            profileMainFrame,
            text="Phone Number",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=3, column=0, sticky="w", padx=(0, 30))
        contactNumberLabel = customtkinter.CTkLabel(
            profileMainFrame,
            text=f"{contactNumber}",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 14, "bold"),
        )
        contactNumberLabel.grid(row=3, column=1, sticky="w")
        ttk.Separator(
            profileMainFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=4, column=0, columnspan=2, sticky="nsew")
        customtkinter.CTkLabel(
            profileMainFrame,
            text="Email",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=5, column=0, sticky="w", padx=(0, 30))
        customtkinter.CTkLabel(
            profileMainFrame,
            text=f"{gmail}",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 14, "bold"),
        ).grid(row=5, column=1, sticky="w")
        ttk.Separator(
            profileMainFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=6, column=0, columnspan=2, sticky="nsew")
        customtkinter.CTkLabel(
            profileMainFrame,
            text=f"Date",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=7, column=0, sticky="w", padx=(0, 30))
        DOB_Label = customtkinter.CTkLabel(
            profileMainFrame,
            text=f'{datetime.datetime.strftime(DOB, "%B %d, %Y")}',
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 14, "bold"),
        )
        DOB_Label.grid(row=7, column=1, sticky="w")
        ttk.Separator(
            profileMainFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=8, column=0, columnspan=2, sticky="nsew")

        customtkinter.CTkLabel(
            userFrame,
            text="Log out everywhere",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=3, column=0, sticky="w", padx=(200), pady=(10, 0))
        customtkinter.CTkLabel(
            userFrame,
            text="This logs you out of Mili everywhere you’re logged in, including the desktop.",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=4, column=0, sticky="w", padx=(200))
        profileFooterFrame = customtkinter.CTkFrame(
            userFrame,
            fg_color="#252525",
            corner_radius=5,
            border_width=2,
            border_color="#7f7f7f",
        )
        profileFooterFrame.grid(row=5, column=0, sticky="w", padx=200, pady=20)
        customtkinter.CTkLabel(
            profileFooterFrame,
            text="Note: It can take up to 1 hour for log out to take effect.",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=0, column=0, sticky="w", padx=(10, 130), pady=5)
        # ------------------------------------------------------------------------------------------------------

        # Edit Profile Frame
        # ------------------------------------------------------------------------------------------------------

        userNameVar = StringVar()
        userNameVar.set(userName)
        contactNumberVar = StringVar()
        contactNumberVar.set(contactNumber)
        genderVar = StringVar()
        genderVar.set(gender)
        dateVar = StringVar()
        dateVar.set(datetime.datetime.strftime(DOB, "%d"))
        monthVar = StringVar()
        monthVar.set(datetime.datetime.strftime(DOB, "%B"))
        yearVar = StringVar()
        yearVar.set(datetime.datetime.strftime(DOB, "%Y"))
        savingVar = StringVar()
        savingVar.set("Save Profile")

        customtkinter.CTkLabel(
            editProfileFrame,
            text="Edit Profile",
            fg_color="#252525",
            text_color="#fff",
            font=("Cooper Black", 25, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=60, pady=(20, 40))

        customtkinter.CTkLabel(
            editProfileFrame,
            text="Name",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=1, column=0, columnspan=3, sticky="w", padx=60)
        userNameEntry = customtkinter.CTkEntry(
            editProfileFrame,
            fg_color="#171717",
            corner_radius=7,
            height=40,
            width=700,
            border_width=1,
            border_color="#111",
            font=("Sitka Small", 14, "normal"),
        )
        userNameEntry.grid(row=2, column=0, columnspan=3, sticky="w", padx=60, pady=5)
        userNameEntry.insert(0, userNameVar.get())

        customtkinter.CTkLabel(
            editProfileFrame,
            text="Phone Number",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=3, column=0, sticky="w", padx=60, pady=(10, 0))
        contactNumberEntry = customtkinter.CTkEntry(
            editProfileFrame,
            fg_color="#171717",
            corner_radius=7,
            height=40,
            width=700,
            border_width=1,
            border_color="#111",
            font=("Sitka Small", 14, "normal"),
        )
        contactNumberEntry.grid(
            row=4, column=0, columnspan=3, sticky="w", padx=60, pady=5
        )
        contactNumberEntry.insert(0, contactNumberVar.get())

        customtkinter.CTkLabel(
            editProfileFrame,
            text="Gender",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=5, column=0, sticky="w", padx=60, pady=(10, 0))
        genderOption = customtkinter.CTkOptionMenu(
            editProfileFrame,
            values=["Prefer no to say", "Male", "Female", "Non-binary", "other"],
            width=700,
            height=40,
            font=("Sitka Small", 14, "normal"),
            fg_color="#171717",
            button_color="#111",
            button_hover_color="#202020",
            dropdown_font=("Sitka Small", 14, "normal"),
            variable=genderVar,
            dropdown_fg_color="#303030",
            dynamic_resizing=True,
        )
        genderOption.grid(row=6, column=0, columnspan=3, sticky="w", padx=60, pady=5)

        customtkinter.CTkLabel(
            editProfileFrame,
            text="Date Of Birth",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=7, column=0, sticky="w", padx=60, pady=(10, 0))
        dateEntry = customtkinter.CTkEntry(
            editProfileFrame,
            fg_color="#171717",
            corner_radius=7,
            height=40,
            width=200,
            border_width=1,
            border_color="#111",
            font=("Sitka Small", 14, "normal"),
        )
        dateEntry.grid(row=8, column=0, sticky="w", padx=(60, 0), pady=5)
        dateEntry.insert(0, dateVar.get())
        monthOption = customtkinter.CTkOptionMenu(
            editProfileFrame,
            values=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            width=200,
            height=40,
            font=("Sitka Small", 14, "normal"),
            fg_color="#171717",
            button_color="#111",
            button_hover_color="#202020",
            dropdown_font=("Sitka Small", 14, "normal"),
            variable=monthVar,
            dropdown_fg_color="#303030",
            dynamic_resizing=True,
        )
        monthOption.grid(row=8, column=1, sticky="w", pady=5)
        yearEntry = customtkinter.CTkEntry(
            editProfileFrame,
            fg_color="#171717",
            corner_radius=7,
            height=40,
            width=200,
            border_width=1,
            border_color="#111",
            font=("Sitka Small", 14, "normal"),
        )
        yearEntry.grid(row=8, column=2, sticky="w", pady=5)
        yearEntry.insert(0, yearVar.get())
        ttk.Separator(
            editProfileFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=9, column=0, columnspan=3, sticky="nsew", padx=60, pady=30)
        editProfileFooterFrame = customtkinter.CTkFrame(
            editProfileFrame, fg_color="#252525", border_width=0
        )
        editProfileFooterFrame.grid(row=10, column=0, columnspan=3, sticky="e", pady=30)
        customtkinter.CTkButton(
            editProfileFooterFrame,
            text="Cancel",
            fg_color="#252525",
            border_color="#fff",
            border_width=1,
            height=40,
            hover=False,
            text_color="#fff",
            corner_radius=20,
            font=("Sitka Small", 16, "bold"),
            command=lambda: self.showFrame(userFrame),
        ).grid(row=0, column=0)
        saveProfileButton = customtkinter.CTkButton(
            editProfileFooterFrame,
            height=45,
            textvariable=savingVar,
            fg_color="#1ed760",
            hover_color="#19b04f",
            font=("Sitka Small", 17, "bold"),
            corner_radius=10,
            text_color="#111",
            command=EditProfile().updateProfile,
        )
        saveProfileButton.grid(row=0, column=1, padx=(30, 50))
        # --------------------------------------------------------------------------------------------------

        # Delete Account Frame
        # --------------------------------------------------------------------------------------------------

        agreeCheckBoxVar = IntVar()
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text="Delete Account",
            fg_color="#252525",
            text_color="#fff",
            font=("Cooper Black", 25, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=60, pady=(25, 0))
        ttk.Separator(
            deleteAccountFrame, orient="horizontal", style="Line.TSeparator"
        ).grid(row=1, column=0, sticky="nsew", padx=60, pady=10)
        dtext_1 = "We're sorry to see you go. If you're sure that you want to delete your     \naccount, please follow the steps below. Keep in mind that deleting your  \naccount is permanent and cannot be undone. This means that all of your \ndata, including any saved information, will be removed from our system. "
        dtext_2 = 'After clicking the "Delete Account" button, you will be redirected to the\nlogin page. Your account will have been deleted from our system. You  \nwill no longer be able to access any of the features or services that you\npreviously had access to.                                                                       '
        dtext_3 = "If you change your mind and decide that you want to use our services\nagain in the future, you will need to create a new account.                  "
        dtext_4 = "Thank you for being a part of our community, and we wish you all the \nbest in your future endeavors.                                                              "
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text=dtext_1,
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=0, sticky="w", padx=60, pady=(10, 5))
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text=dtext_2,
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=3, column=0, sticky="w", padx=60, pady=5)
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text=dtext_3,
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=4, column=0, sticky="w", padx=60, pady=5)
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text=dtext_4,
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=5, column=0, sticky="w", padx=60, pady=5)
        customtkinter.CTkLabel(
            deleteAccountFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\shield.png", 300, 300),
            fg_color="#252525",
        ).grid(row=2, column=1, rowspan=5, sticky="n")
        passwordEntry = customtkinter.CTkEntry(
            deleteAccountFrame,
            fg_color="#171717",
            corner_radius=7,
            height=40,
            width=200,
            border_width=1,
            border_color="#111",
            font=("Sitka Small", 20, "bold"),
            show="\U00002022",
        )
        passwordEntry.grid(row=6, column=0, sticky="w", padx=60, pady=(70, 10))
        deleteAccountButton = customtkinter.CTkButton(
            deleteAccountFrame,
            width=200,
            text="Delete Account",
            height=40,
            border_width=0,
            corner_radius=5,
            font=("Sitka Small", 15, "bold"),
            bg_color="transparent",
            text_color="#111",
            fg_color="#1ed760",
            hover_color="#19b04f",
            command=DeleteAccount().passwordConfirmation,
        )
        deleteAccountButton.grid(row=7, column=0, sticky="w", padx=60, pady=(5, 15))
        dtext_5 = "     I understand that account deletion is a permanent action, and I am sure that I want to proceed with this\n     request. I have taken the necessary steps to ensure that I will no longer require access to this account."
        deleteAccountCheckBox = customtkinter.CTkCheckBox(
            deleteAccountFrame,
            fg_color="#1ed760",
            border_color="#1ed760",
            checkmark_color="#111",
            font=("Sitka Small", 12, "normal"),
            text=dtext_5,
            hover=False,
            variable=agreeCheckBoxVar,
        )
        deleteAccountCheckBox.grid(row=8, column=0, columnspan=2, sticky="w", padx=60)
        # --------------------------------------------------------------------------------------------------

        # Settings Frame
        # --------------------------------------------------------------------------------------------------

        explicitContentVar = IntVar()
        productEmailVar = IntVar()
        with open(
            application_directory + "\\Data\\Cache\\Mili Settings.settings", "rb"
        ) as file:
            settingsData = pickle.load(file)
            file.close()
        explicitContentVar.set(settingsData.get("Explicit content"))
        productEmailVar.set(settingsData.get("Product emails"))
        customtkinter.CTkLabel(
            settingsFrame,
            text="    Settings",
            image=self.ImageObject("Data\\Images\\GUI\\settings.png", 35, 35),
            fg_color="#252525",
            font=("Cooper Black", 25, "bold"),
            text_color="#fff",
            compound="left",
        ).grid(row=0, column=0, sticky="w", padx=60, pady=30)
        customtkinter.CTkLabel(
            settingsFrame,
            text="Explicit Content",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=60)
        customtkinter.CTkLabel(
            settingsFrame,
            text="Allow explicit-rated content",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=2, column=0, sticky="w", padx=60)
        explicitContentSwitch = customtkinter.CTkSwitch(
            settingsFrame,
            switch_width=50,
            switch_height=27,
            button_length=0,
            border_width=0,
            text="",
            progress_color="#1ed760",
            bg_color="#252525",
            fg_color="grey",
            button_color="#d4cbd0",
            button_hover_color="#d4cbd0",
            onvalue=1,
            offvalue=0,
            variable=explicitContentVar,
            command=SettingCommands().explicitCommandOption,
        )
        explicitContentSwitch.grid(row=2, column=1, sticky="ne")
        customtkinter.CTkLabel(
            settingsFrame,
            text="Product Emails",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=3, column=0, sticky="w", padx=60, pady=(15, 0))
        customtkinter.CTkLabel(
            settingsFrame,
            text="Get tips and resources about Mili.",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=4, column=0, sticky="w", padx=60)
        productEmailSwitch = customtkinter.CTkSwitch(
            settingsFrame,
            switch_width=50,
            switch_height=27,
            button_length=0,
            border_width=0,
            text="",
            progress_color="#1ed760",
            bg_color="#252525",
            fg_color="grey",
            button_color="#d4cbd0",
            button_hover_color="#d4cbd0",
            onvalue=1,
            offvalue=0,
            variable=productEmailVar,
            command=SettingCommands().productEmailCommand,
        )
        productEmailSwitch.grid(row=4, column=1, sticky="ne")
        customtkinter.CTkLabel(
            settingsFrame,
            text="Storage",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 16, "bold"),
        ).grid(row=5, column=0, sticky="w", padx=60, pady=(15, 0))
        cacheSizeFrame = customtkinter.CTkFrame(
            settingsFrame, border_width=0, fg_color="#252525"
        )
        cacheSizeFrame.grid(row=6, column=0, sticky="w", padx=60)
        customtkinter.CTkLabel(
            cacheSizeFrame,
            text="Cache Size :",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=0, column=0, sticky="w")
        cacheSizeLabel = customtkinter.CTkLabel(
            cacheSizeFrame,
            text=f"{Cache().cacheMemorySize()} KB",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        )
        cacheSizeLabel.grid(row=0, column=1, sticky="w", padx=5)
        customtkinter.CTkLabel(
            settingsFrame,
            text="This helps to reduce the time required to load data, improving the user experience.",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=7, column=0, sticky="w", padx=60)
        clearCacheButton = customtkinter.CTkButton(
            settingsFrame,
            height=35,
            width=160,
            text="Clear cache",
            font=("Sitka Small", 13, "bold"),
            border_width=0,
            corner_radius=20,
            fg_color="#1ed760",
            text_color="#111",
            hover_color="#19b04f",
            command=clearCacheMemory,
        )
        clearCacheButton.grid(row=7, column=1, sticky="ne")
        customtkinter.CTkLabel(
            settingsFrame,
            text="Location",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=8, column=0, sticky="w", padx=60)
        customtkinter.CTkLabel(
            settingsFrame,
            text=f"{application_directory}",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=9, column=0, sticky="w", padx=60)
        customtkinter.CTkLabel(
            settingsFrame,
            text="Application Size",
            fg_color="#252525",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=10, column=0, sticky="w", padx=60)
        customtkinter.CTkLabel(
            settingsFrame,
            text=f"{ApplicationSize().memory()} MB",
            fg_color="#252525",
            text_color="#7f7f7f",
            font=("Sitka Small", 13, "normal"),
        ).grid(row=11, column=0, sticky="w", padx=60)
        # --------------------------------------------------------------------------------------------------

        # Update Frame
        # --------------------------------------------------------------------------------------------------
        updateEmailVar = IntVar()
        updateEmailVar.set(0)
        updateMeterVar = IntVar()
        updateMeterVar.set(0)
        customtkinter.CTkLabel(
            updatesFrame,
            text="Mili Update",
            font=("Cooper Black", 25, "normal"),
            fg_color="#252525",
            text_color="#fff",
        ).pack(side=TOP, anchor="w", padx=40, pady=(35, 25))
        headerUpdateFrame = customtkinter.CTkFrame(
            updatesFrame, fg_color="#252525", corner_radius=0
        )
        headerUpdateFrame.pack(side=TOP, anchor="center", fill=X, pady=(30, 80))
        customtkinter.CTkLabel(
            headerUpdateFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\refresh.png", 100, 100),
            fg_color="#252525",
        ).pack(side=LEFT, anchor="w", padx=(30, 40))
        progressFrame = customtkinter.CTkFrame(
            headerUpdateFrame, fg_color="#252525", corner_radius=0, height=100
        )
        progressFrame.pack(side=LEFT, anchor="nw", fill=X)
        updateButton = customtkinter.CTkButton(
            headerUpdateFrame,
            height=35,
            width=140,
            text="Check for updates",
            font=("Sitka Small", 13, "bold"),
            border_width=0,
            corner_radius=5,
            fg_color="#1ed760",
            text_color="#111",
            hover_color="#19b04f",
            command=lambda: Thread(target=Updates().updateFiles).start(),
        )
        updateButton.pack(side=RIGHT, anchor="e", padx=(20, 40))
        progressLabel = customtkinter.CTkLabel(
            progressFrame,
            text="You are up to date",
            font=("Sitka Small", 16, "bold"),
            fg_color="#252525",
            text_color="#fff",
        )
        progressLabel.pack(side=TOP, anchor="nw", pady=(10, 5))
        progressBar = customtkinter.CTkProgressBar(
            progressFrame,
            height=5,
            width=550,
            mode="indeterminate",
            indeterminate_speed=1.5,
            fg_color="#252525",
            progress_color="#1ed760",
        )
        customtkinter.CTkLabel(
            updatesFrame,
            text="More Options",
            font=("Sitka Small", 16, "bold"),
            fg_color="#252525",
            text_color="#fff",
        ).pack(side=TOP, anchor="w", padx=70, pady=5)
        customtkinter.CTkButton(
            updatesFrame,
            height=70,
            width=800,
            image=self.ImageObject("Data\\Images\\GUI\\history.png", 50, 50),
            compound="left",
            anchor="w",
            text="Update History",
            text_color="#fff",
            fg_color="#181818",
            font=("Sitka Small", 13, "normal"),
            hover_color="#191919",
            command=lambda: Thread(target=updateHistory).start(),
        ).pack(side=TOP, anchor="center", pady=2)
        updateFooterFrame_1 = customtkinter.CTkFrame(
            updatesFrame, height=70, width=800, fg_color="#181818", corner_radius=5
        )
        updateFooterFrame_1.pack(side=TOP, anchor="center", pady=2)
        updateFooterFrame_2 = customtkinter.CTkFrame(
            updatesFrame, height=70, width=800, fg_color="#181818", corner_radius=5
        )
        updateFooterFrame_2.pack(side=TOP, anchor="center", pady=2)
        customtkinter.CTkLabel(
            updateFooterFrame_1,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\bell.png", 30, 30),
            fg_color="#181818",
            text_color="#fff",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)
        customtkinter.CTkLabel(
            updateFooterFrame_1,
            text="Notify me through mail regarding the latest updates                ",
            font=("Sitka Small", 13, "bold"),
            fg_color="#181818",
            text_color="#fff",
        ).grid(row=0, column=1, sticky="w", padx=(10, 150), pady=20)
        updateEmailSwitch = customtkinter.CTkSwitch(
            updateFooterFrame_1,
            switch_width=45,
            switch_height=25,
            button_length=0,
            border_width=0,
            text="",
            progress_color="#1ed760",
            bg_color="#181818",
            fg_color="grey",
            button_color="#d4cbd0",
            button_hover_color="#d4cbd0",
            onvalue=1,
            offvalue=0,
            variable=updateEmailVar,
        )
        updateEmailSwitch.grid(row=0, column=2, sticky="e", padx=(50, 0))

        customtkinter.CTkLabel(
            updateFooterFrame_2,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\gauge.png", 25, 25),
            fg_color="#181818",
            text_color="#fff",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)
        customtkinter.CTkLabel(
            updateFooterFrame_2,
            text="Download updates over metered connections                          ",
            font=("Sitka Small", 13, "bold"),
            fg_color="#181818",
            text_color="#fff",
        ).grid(row=0, column=1, sticky="w", padx=(10, 150), pady=20)
        updateMeterSwitch = customtkinter.CTkSwitch(
            updateFooterFrame_2,
            switch_width=45,
            switch_height=25,
            button_length=0,
            border_width=0,
            text="",
            progress_color="#1ed760",
            bg_color="#181818",
            fg_color="grey",
            button_color="#d4cbd0",
            button_hover_color="#d4cbd0",
            onvalue=1,
            offvalue=0,
            variable=updateMeterVar,
        )
        updateMeterSwitch.grid(row=0, column=2, sticky="e", padx=(70, 0))
        # --------------------------------------------------------------------------------------------------

        # Reset Password Frame
        # -------------------------------------------------------------------------------------------
        resetButtonVariable = StringVar()
        resetButtonVariable.set("Reset Password")

        customtkinter.CTkButton(
            resetPasswordFrame,
            text="🡸",
            font=("", 30, "normal"),
            text_color="black",
            fg_color="#FDB0C0",
            hover=False,
            command=lambda: self.showFrame(userFrame),
        ).pack(side=TOP, anchor="w", padx=30, pady=30)
        resetPasswordMainFrame = customtkinter.CTkFrame(
            resetPasswordFrame, fg_color="#fff", corner_radius=15
        )
        resetPasswordMainFrame.pack(side=TOP, anchor="center")
        customtkinter.CTkLabel(
            resetPasswordMainFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\lock.png", 100, 100),
            fg_color="#fff",
        ).pack(side=TOP, anchor="center", pady=15)
        customtkinter.CTkLabel(
            resetPasswordMainFrame,
            text="Reset Password",
            text_color="#111",
            fg_color="#fff",
            font=("Roboto", 25, "bold"),
        ).pack(side=TOP, anchor="center", pady=10)
        resetCurrentPasswordEntry = customtkinter.CTkEntry(
            resetPasswordMainFrame,
            fg_color="#fff",
            height=35,
            width=250,
            border_color="black",
            text_color="#111",
            placeholder_text="Current Password",
            placeholder_text_color="#393939",
            font=("Georgia", 15, "bold"),
            show="\U00002022",
        )
        resetCurrentPasswordEntry.pack(
            side=TOP, anchor="center", pady=(30, 10), padx=30
        )
        resetNewPasswordEntry = customtkinter.CTkEntry(
            resetPasswordMainFrame,
            fg_color="#fff",
            height=35,
            width=250,
            border_color="black",
            text_color="#111",
            placeholder_text="New Password",
            placeholder_text_color="#393939",
            font=("Georgia", 15, "bold"),
            show="\U00002022",
        )
        resetNewPasswordEntry.pack(side=TOP, anchor="center", padx=30)
        customtkinter.CTkButton(
            resetPasswordMainFrame,
            textvariable=resetButtonVariable,
            text_color="#111",
            fg_color="#1ed760",
            hover_color="#19b04f",
            font=("Georgia", 15, "bold"),
            height=35,
            width=250,
            command=lambda: Thread(target=ResetPasswordBackend().model).start(),
        ).pack(side=TOP, anchor="center", padx=30, pady=(20, 60))
        # -------------------------------------------------------------------------------------------

        # Reset Update Frame
        # -------------------------------------------------------------------------------------------

        resetUpdateMainFrame = customtkinter.CTkFrame(
            resetUpdateFrame, fg_color="#fff", corner_radius=15
        )
        resetUpdateMainFrame.pack(side=TOP, anchor="center", pady=100)
        customtkinter.CTkLabel(
            resetUpdateMainFrame,
            text="",
            image=self.ImageObject("Data\\Images\\GUI\\security shield.png", 150, 150),
            fg_color="#fff",
        ).pack(side=TOP, anchor="center", pady=25)
        customtkinter.CTkLabel(
            resetUpdateMainFrame,
            text="You password has been reset",
            text_color="#7f7f7f",
            fg_color="#fff",
            font=("Georgia", 17, "bold"),
        ).pack(side=TOP, anchor="center", padx=30)
        customtkinter.CTkLabel(
            resetUpdateMainFrame,
            text="Successfully",
            text_color="#111",
            fg_color="#fff",
            font=("Georgia", 21, "bold"),
        ).pack(side=TOP, anchor="center", padx=30)
        customtkinter.CTkButton(
            resetUpdateMainFrame,
            text="Continue",
            text_color="#111",
            fg_color="#1ed760",
            hover_color="#19b04f",
            font=("Georgia", 15, "bold"),
            height=35,
            width=250,
            command=lambda: self.showFrame(userFrame),
        ).pack(side=TOP, anchor="center", padx=30, pady=(40, 70))
        # -------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------
        self.showFrame(userFrame)
        self.showFrame(self.profileFrame)

    # -----------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------

    def Log(self):
        # Backend of login page
        # ---------------------------------------------------------------------------------------------------
        class UserLogin:
            def __init__(self):
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]

            def updateDataBase(self, email, data):
                try:
                    self.collection.update_one({"email": email}, {"$set": data})
                except:
                    messagebox.showerror("Mili", "Try Again!")

            def sendLogingMail(self, data):
                try:
                    MailToUser(data).loginWarning()
                except:
                    pass

            def createCacheCredentials(self, username, password):
                CredentialManager().write_credential(username, password)

            def dataCollection(self, email):
                currentDate = datetime.datetime.now()
                device = device_name()
                location = ip_based_location()
                ip = location.get("query")
                user = self.user(email)
                last_login_device_model = device_Model()
                last_login_coordinates = GPS.getLocation()
                last_login_location = reverseGeocoding(
                    last_login_coordinates[0], last_login_coordinates[1]
                )
                previousLoginDetails = user.get("login_dates")
                previousLoginDetails.append(
                    {
                        "time": currentDate,
                        "device": device,
                        "ip_address": ip,
                        "coordinates": {
                            "latitude": last_login_coordinates[0],
                            "longitude": last_login_coordinates[1],
                        },
                    }
                )

                data = {
                    "login_dates": previousLoginDetails,
                    "last_login_date": currentDate,
                    "last_login_device_model": last_login_device_model,
                    "last_login_coordinates": last_login_coordinates,
                    "last_login_location": last_login_location,
                    "last_login_ip": ip,
                }

                emailData = {
                    "sender": "yourvirtualmiliassistant@gmail.com",
                    "receiver": email,
                    "password": Encryption(
                        b"gAAAAABkc4Xc0EQcaqGSJDXLkaRr7hN0SR0fZhz1fobcxWG8GlJSb0fkTWHzWZrcfknDqkVgdr0gq2ASHVWUku-m6-R1rn3pP0wP9fF-bozeHvfIlUwtLXk="
                    ).decrypt_text(),
                    "location": f"{location.get('city')}, {location.get('regionName')}",
                    "device": device,
                }
                t1 = Thread(
                    target=self.updateDataBase,
                    args=(
                        email,
                        data,
                    ),
                )
                t2 = Thread(target=self.sendLogingMail, args=(emailData,))
                t3 = Thread(
                    target=self.createCacheCredentials,
                    args=(email, user.get("password")),
                )
                t1.start(), t2.start(), t3.start()
                t1.join(), t2.join(), t3.join()
                progress.stop()
                messagebox.showinfo("Mili", "You have logged in successfully")
                exit()

            @lru_cache(maxsize=10)
            def user(self, email):
                doc = self.collection.find_one({"email": email})
                if doc is None:
                    return None
                return doc

            def widgets(self):
                username = usernameLoginEntry.get().lower()
                password = usernameLoginPassword.get()
                if username == "":
                    messagebox.showwarning("Mili", "Please enter your email")
                elif password == "":
                    messagebox.showwarning("Mili", "Please enter your password")
                elif username.endswith("@gmail.com") is False:
                    messagebox.showwarning("Mili", "Please enter valid email")
                else:
                    userPassword = self.user(username)
                    if userPassword is None:
                        messagebox.showwarning("Mili", "User does not exist")
                    elif not Hash.verifyCredential(
                        userPassword.get("password"), password
                    ):
                        messagebox.showwarning("Mili", "Invalid password. Try again!")
                        return None
                    else:
                        progress.grid(row=0, column=0, sticky="nsew", columnspan=2)
                        progress.start()
                        thread = Thread(target=self.dataCollection, args=(username,))
                        thread.start()

        # ---------------------------------------------------------------------------------------------------

        # Forget Password backend
        # ---------------------------------------------------------------------------------------------------
        class ResetPassword:
            def __init__(self):
                self.email = None
                self.password = None
                self.hashed_pwd = None
                self.OTP = None
                self.codeVar = StringVar()
                self.codeVar.set("Resend new code")
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]
                self.resetPasswordFrame = customtkinter.CTkFrame(
                    frame5, corner_radius=20, fg_color="#171717"
                )
                self.resetPasswordFrame.pack(side=TOP, anchor=CENTER, pady=80)
                self.emailAddress = customtkinter.CTkLabel(
                    self.resetPasswordFrame,
                    text="",
                    font=("Georgia", 20, "bold"),
                    text_color="white",
                    anchor="center",
                    compound="center",
                )
                self.emailAddress.grid(
                    row=1, column=0, sticky="n", pady=(60, 0), padx=30
                )
                customtkinter.CTkLabel(
                    self.resetPasswordFrame,
                    text="We've sent the code to the gmail account\nEnter your OTP code here",
                    font=("Georgia", 15),
                    text_color="#787276",
                ).grid(row=2, column=0, sticky="n", pady=15, padx=30)
                self.codeEntry = customtkinter.CTkEntry(
                    self.resetPasswordFrame,
                    width=200,
                    height=50,
                    corner_radius=15,
                    border_width=0,
                    fg_color="black",
                    placeholder_text="Code",
                    placeholder_text_color="#787276",
                    font=("Georgia", 17, "bold"),
                    text_color="white",
                )
                self.codeEntry.grid(row=3, column=0, sticky="n", pady=(15, 5))
                customtkinter.CTkButton(
                    self.resetPasswordFrame,
                    text="Verify",
                    text_color="white",
                    width=200,
                    height=40,
                    corner_radius=15,
                    font=("Georgia", 13),
                    fg_color="#252525",
                    hover_color="#911d5a",
                    command=self.OTPVerification,
                ).grid(row=4, column=0, sticky="n", pady=5)
                customtkinter.CTkLabel(
                    self.resetPasswordFrame,
                    text="Didn't you receive any code?",
                    font=("Georgia", 13),
                    text_color="#787276",
                ).grid(row=5, column=0, sticky="n", pady=15)
                customtkinter.CTkButton(
                    self.resetPasswordFrame,
                    fg_color="#171717",
                    hover_color="#171717",
                    text_color="#911d5a",
                    font=("Georgia", 13),
                    textvariable=self.codeVar,
                    command=lambda: Thread(target=self.resendOTPBackend).start(),
                ).grid(row=6, column=0, sticky="n", pady=(0, 50))

            def showFrame(self, frame):
                frame.tkraise()

            @lru_cache(maxsize=5)
            def user(self, email):
                doc = self.collection.find_one({"email": email})
                if doc is None:
                    return None
                return doc

            def resendOTPBackend(self):
                self.OTP = randint(111111, 999999)
                self.codeVar.set("Sending Code")
                self.sendOTP()
                self.codeVar.set("Resend new code")

            def OTPVerification(self):
                enteredCode = int(self.codeEntry.get())
                generatedOTP = self.OTP
                if generatedOTP == enteredCode:
                    thread = Thread(target=self.updateDataBase)
                    thread.start()
                    thread.join()
                    messagebox.showinfo(
                        "Mili", "Your password has been changed successfully"
                    )
                    self.showFrame(signInFrame)
                else:
                    messagebox.showerror("Mili", "Invalid OTP Code")

            def sendOTP(self):
                data = {
                    "sender": "yourvirtualmiliassistant@gmail.com",
                    "receiver": self.email,
                    "password": Encryption(
                        b"gAAAAABkc4Xc0EQcaqGSJDXLkaRr7hN0SR0fZhz1fobcxWG8GlJSb0fkTWHzWZrcfknDqkVgdr0gq2ASHVWUku-m6-R1rn3pP0wP9fF-bozeHvfIlUwtLXk="
                    ).decrypt_text(),
                    "otp": self.OTP,
                }
                MailToUser(data).forgetPasswordOTP()

            def updateDataBase(self):
                try:
                    user = self.user(self.email)
                    current_password = user.get("password")
                    previous_passwords = user.get("previous_passwords")
                    previous_passwords.append(
                        {
                            "timestamp": datetime.datetime.timestamp(
                                datetime.datetime.now()
                            ),
                            "password": current_password,
                        }
                    )
                    self.collection.update_one(
                        {"email": self.email},
                        {
                            "$set": {
                                "password": self.hashed_pwd,
                                "previous_passwords": previous_passwords,
                            }
                        },
                    )
                except:
                    messagebox.showerror("Mili", "Try Again!")

            def widgets(self):
                self.email = usernameForgetEntry.get().lower()
                self.password = newPasswordEntry.get()
                if self.email == "":
                    messagebox.showwarning("Mili", "Please enter your email")
                elif self.password == "":
                    messagebox.showwarning("Mili", "Please enter your new password")
                elif self.email.endswith("@gmail.com") is False:
                    messagebox.showwarning("Mili", "Please enter valid email")
                else:
                    user = self.user(self.email)
                    if user is None:
                        messagebox.showwarning("Mili", "User does't exist")
                    else:
                        previous_passwords = user.get("previous_passwords")

                        self.hashed_pwd = Hash.generateHashedPassword(self.password)
                        passwords_list = []
                        for element in previous_passwords:
                            passwords_list.append(element.get("password"))
                        if Hash.verifyCredential(user.get("password"), self.password):
                            messagebox.showwarning(
                                "Mili", "You used this password previously"
                            )
                            return None
                        for pwd in passwords_list:
                            if Hash.verifyCredential(pwd, self.password):
                                messagebox.showwarning(
                                    "Mili", "You used this password previously"
                                )
                                return None
                        else:
                            forgetPasswordCodeButton.configure(text = "Sending OTP")
                            self.OTP = randint(111111, 999999)
                            self.emailAddress.configure(text=self.email)
                            thread = Thread(target=self.sendOTP())
                            thread.start()
                            self.showFrame(frame5)

        # ---------------------------------------------------------------------------------------------------

        # Backend for signup
        # ---------------------------------------------------------------------------------------------------
        class CreateAccoount:
            def __init__(self):
                self.email = None
                self.data = None
                self.OTP = None
                self.hashed_pwd = None
                self.codeVar = StringVar()
                self.codeVar.set("Resend new code")
                self.url = Encryption(
                    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
                ).decrypt_text()
                self.client = pymongo.MongoClient(self.url)
                self.db = self.client["Assistant"]
                self.collection = self.db["User Credentials"]
                self.signupVerificationFrame = customtkinter.CTkFrame(
                    frame6, corner_radius=20, fg_color="#171717"
                )
                self.signupVerificationFrame.pack(side=TOP, anchor=CENTER, pady=80)
                self.emailAddress = customtkinter.CTkLabel(
                    self.signupVerificationFrame,
                    text="",
                    font=("Georgia", 20, "bold"),
                    text_color="white",
                    anchor="center",
                    compound="center",
                )
                self.emailAddress.grid(
                    row=1, column=0, sticky="n", pady=(60, 0), padx=30
                )
                customtkinter.CTkLabel(
                    self.signupVerificationFrame,
                    text="We've sent the code to the gmail account\nEnter your OTP code here",
                    font=("Georgia", 15),
                    text_color="#787276",
                ).grid(row=2, column=0, sticky="n", pady=15, padx=30)
                self.codeEntry = customtkinter.CTkEntry(
                    self.signupVerificationFrame,
                    width=200,
                    height=50,
                    corner_radius=15,
                    border_width=0,
                    fg_color="black",
                    placeholder_text="Code",
                    placeholder_text_color="#787276",
                    font=("Georgia", 17, "bold"),
                    text_color="white",
                )
                self.codeEntry.grid(row=3, column=0, sticky="n", pady=(15, 5))
                customtkinter.CTkButton(
                    self.signupVerificationFrame,
                    text="Verify",
                    text_color="white",
                    width=200,
                    height=40,
                    corner_radius=15,
                    font=("Georgia", 13),
                    fg_color="#252525",
                    hover_color="#911d5a",
                    command=self.OTPVerification,
                ).grid(row=4, column=0, sticky="n", pady=5)
                customtkinter.CTkLabel(
                    self.signupVerificationFrame,
                    text="Didn't you receive any code?",
                    font=("Georgia", 13),
                    text_color="#787276",
                ).grid(row=5, column=0, sticky="n", pady=15)
                customtkinter.CTkButton(
                    self.signupVerificationFrame,
                    fg_color="#171717",
                    hover_color="#171717",
                    text_color="#911d5a",
                    font=("Georgia", 13),
                    textvariable=self.codeVar,
                    command=lambda: Thread(target=self.resendOTPBackend).start(),
                ).grid(row=6, column=0, sticky="n", pady=(0, 50))

            def showFrame(self, frame):
                frame.tkraise()

            def resendOTPBackend(self):
                self.OTP = randint(111111, 999999)
                self.codeVar.set("Sending Code")
                self.sendOTP()
                self.codeVar.set("Resend new code")

            def sendOTP(self):
                data = {
                    "sender": "yourvirtualmiliassistant@gmail.com",
                    "receiver": self.email,
                    "password": Encryption(
                        b"gAAAAABkc4Xc0EQcaqGSJDXLkaRr7hN0SR0fZhz1fobcxWG8GlJSb0fkTWHzWZrcfknDqkVgdr0gq2ASHVWUku-m6-R1rn3pP0wP9fF-bozeHvfIlUwtLXk="
                    ).decrypt_text(),
                    "otp": self.OTP,
                }
                MailToUser(data).sendOTP()

            @lru_cache(maxsize=5)
            def user(self, email):
                doc = self.collection.find_one({"email": email})
                if doc is None:
                    return None
                return doc

            def createUserData(self):
                now = datetime.datetime.now()
                device = device_name()
                last_login_device_model = device_Model()
                last_login_coordinates = GPS.getLocation()
                last_login_location = reverseGeocoding(
                    last_login_coordinates[0], last_login_coordinates[1]
                )
                ip = ip_based_location().get("query")
                login_dates = [
                    {
                        "time": now,
                        "device": device,
                        "ip_address": ip,
                        "coordinates": {
                            "latitude": last_login_coordinates[0],
                            "longitude": last_login_coordinates[1],
                        },
                    }
                ]
                self.data.update(
                    {
                        "login_dates": login_dates,
                        "ac_date": now,
                        "last_login_date": now,
                        "last_login_device_model": last_login_device_model,
                        "last_login_coordinates": last_login_coordinates,
                        "last_login_location": last_login_location,
                        "last_login_ip": ip,
                    }
                )

            def createCacheCredentials(self, username, password):
                CredentialManager().write_credential(username, password)

            def updateDataBase(self):
                try:
                    self.collection.insert_one(self.data)
                except:
                    messagebox.showerror("Mili", "Try Again!")

            def OTPVerification(self):
                enteredCode = int(self.codeEntry.get())
                generatedOTP = self.OTP
                if generatedOTP == enteredCode:
                    email_data = {
                        "name": self.data.get("name"),
                        "sender": "yourvirtualmiliassistant@gmail.com",
                        "receiver": self.data.get("email"),
                        "password": Encryption(
                            b"gAAAAABkc4Xc0EQcaqGSJDXLkaRr7hN0SR0fZhz1fobcxWG8GlJSb0fkTWHzWZrcfknDqkVgdr0gq2ASHVWUku-m6-R1rn3pP0wP9fF-bozeHvfIlUwtLXk="
                        ).decrypt_text(),
                    }
                    thread1 = Thread(target=self.updateDataBase)
                    thread2 = Thread(
                        target=self.createCacheCredentials,
                        args=(
                            self.data.get("email"),
                            self.data.get("password"),
                        ),
                    )
                    thread3 = Thread(target=greetEmail, args=(email_data,))
                    thread1.start(), thread2.start(), thread3.start()
                    thread1.join(), thread2.join(), thread3.join()
                    messagebox.showinfo(
                        "Mili", "Your account has been created successfully"
                    )
                    exit()
                else:
                    messagebox.showerror("Mili", "Invalid OTP Code")

            def widgets(self):
                full_name = usernameEntry.get().strip().title()
                self.email = useremailEntry.get().strip().lower()
                password = passwordEntry.get().strip()
                phone_number = contactNumberEntry.get().strip()
                userBirthDate = dateEntry.get().strip()
                userBirthMonth = userBirthMonthSignInVar.get()
                userBirthYear = yearEntry.get().strip()
                gender = userGender.get()
                try:
                    userDOB = datetime.datetime.strptime(
                        f"{userBirthDate} {userBirthMonth} {userBirthYear}", "%d %B %Y"
                    )
                except:
                    userDOB = None
                if full_name == "":
                    messagebox.showwarning("Mili", "Please enter your full name")
                elif self.email == "":
                    messagebox.showwarning("Mili", "Please enter your email")
                elif password == "":
                    messagebox.showwarning("Mili", "Please enter the password")
                elif phone_number == "":
                    messagebox.showwarning("Mili", "Please enter your contact number")
                elif gender is None or gender == "Gender":
                    messagebox.showwarning("Mili", "Please enter your Gender")
                elif userBirthDate == "":
                    messagebox.showwarning("Mili", "Please enter your day of birth")
                elif userBirthMonth == "" or userBirthMonth == "Month":
                    messagebox.showwarning("Mili", "Please select your month of birth")
                elif userBirthYear == "":
                    messagebox.showwarning("Mili", "Please select your year of birth")
                elif self.email.endswith("@gmail.com") is False:
                    messagebox.showwarning("Mili", "Invalid email")
                elif len(phone_number) != 10 or phone_number.isdigit() is False:
                    messagebox.showwarning("Mili", "Invalid phone number")
                elif userDOB is None:
                    messagebox.showwarning("Mili", "Please check your date of birth")
                else:
                    user = self.user(self.email)
                    if user is not None:
                        messagebox.showwarning("Mili", "User already exist")
                    else:
                        self.OTP = randint(111111, 999999)
                        self.emailAddress.configure(text=self.email)
                        thread = Thread(target=self.sendOTP())
                        thread.start()
                        self.hashed_pwd = Hash.generateHashedPassword(password)
                        self.showFrame(frame6)
                        self.data = {
                            "name": full_name,
                            "phone number": "9557657500",
                            "email": self.email,
                            "password": self.hashed_pwd,
                            "gender": gender,
                            "DOB": userDOB,
                            "previous_passwords": [],
                            "personal_info": {},
                        }
                        newThread = Thread(target=self.createUserData)
                        newThread.start()

        # ---------------------------------------------------------------------------------------------------

        def exit():
            self.quit()

        # All Frames
        # ---------------------------------------------------------------------------------------------------
        self.logFrame.rowconfigure(0, weight=1)
        self.logFrame.columnconfigure(0, weight=1)

        signInFrame = customtkinter.CTkFrame(
            self.logFrame, fg_color="#171717", corner_radius=0
        )
        signInFrame.grid(row=0, column=0, sticky="nsew")
        signUpFrame = customtkinter.CTkFrame(
            self.logFrame, fg_color="#171717", corner_radius=0
        )
        signUpFrame.grid(row=0, column=0, sticky="nsew")
        forgetPasswordFrame = customtkinter.CTkFrame(
            self.logFrame, fg_color="#171717", corner_radius=0
        )
        forgetPasswordFrame.grid(row=0, column=0, sticky="nsew")
        frame5 = customtkinter.CTkFrame(
            self.logFrame, fg_color="#252525", corner_radius=0
        )
        frame5.grid(row=0, column=0, sticky="nsew")
        frame6 = customtkinter.CTkFrame(
            self.logFrame, fg_color="#252525", corner_radius=0
        )
        frame6.grid(row=0, column=0, sticky="nsew")
        # ---------------------------------------------------------------------------------------------------

        # Signin Frame
        # ---------------------------------------------------------------------------------------------------
        customtkinter.CTkLabel(
            signInFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\background.jpg", 1120, 700),
            anchor="center",
        ).grid(row=0, column=0, sticky="nsew")
        loginFrame = customtkinter.CTkFrame(
            signInFrame,
            fg_color="#171717",
            corner_radius=0,
        )
        loginFrame.grid(row=0, column=0, sticky="n", pady=100)
        progress = customtkinter.CTkProgressBar(
            loginFrame,
            width=300,
            height=5,
            corner_radius=0,
            mode="indeterminant",
            progress_color="white",
            fg_color="#252525",
        )
        customtkinter.CTkLabel(
            loginFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\logo.png", 100, 100),
            text_color="white",
            anchor="center",
        ).grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(50, 70))
        usernameLoginEntry = customtkinter.CTkEntry(
            loginFrame,
            width=250,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Email",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        usernameLoginEntry.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=3, padx=30
        )
        usernameLoginPassword = customtkinter.CTkEntry(
            loginFrame,
            width=250,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Password",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        usernameLoginPassword.grid(
            row=3, column=0, columnspan=2, sticky="nsew", pady=3, padx=30
        )
        loginButton = customtkinter.CTkButton(
            loginFrame,
            text="Login",
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            hover_color="#911d5a",
            width=35,
            height=30,
            fg_color="#252525",
            text_color="white",
            command=UserLogin().widgets,
        )
        loginButton.grid(row=4, column=0, sticky="nsew", padx=(30, 3), pady=(20, 5))
        signUpButton = customtkinter.CTkButton(
            loginFrame,
            text="Sign Up",
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            hover_color="#911d5a",
            width=35,
            height=30,
            fg_color="#252525",
            text_color="white",
            command=lambda: self.showFrame(signUpFrame),
        )
        signUpButton.grid(row=4, column=1, sticky="nsew", padx=(3, 30), pady=(20, 5))
        forgetPasswordButton = customtkinter.CTkButton(
            loginFrame,
            text="Forget Password",
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            hover_color="#911d5a",
            width=35,
            height=30,
            fg_color="#252525",
            text_color="white",
            command=lambda: self.showFrame(forgetPasswordFrame),
        )
        forgetPasswordButton.grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=30, pady=(5, 50)
        )

        # SignUp Frame
        # ---------------------------------------------------------------------------------------------------
        customtkinter.CTkLabel(
            signUpFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\background.jpg", 1120, 700),
            anchor="center",
        ).grid(row=0, column=0, sticky="nsew")
        accountFrame = customtkinter.CTkFrame(
            signUpFrame,
            fg_color="#171717",
            corner_radius=0,
        )
        accountFrame.grid(row=0, column=0, sticky="n", pady=30)
        userBirthMonthSignInVar = StringVar()
        userBirthMonthSignInVar.set(value="Month")
        userGender = StringVar()
        userGender.set("Gender")
        customtkinter.CTkButton(
            accountFrame,
            text="Back",
            border_width=0,
            corner_radius=0,
            font=("Georgia", 15),
            width=25,
            height=20,
            fg_color="#171717",
            text_color="#911d5a",
            hover=False,
            command=lambda: self.showFrame(signInFrame),
        ).grid(row=0, column=0, columnspan=3, sticky="ne", padx=10, pady=10)
        customtkinter.CTkLabel(
            accountFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\logo.png", 100, 100),
            text_color="white",
            anchor="center",
        ).grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(50, 40))
        usernameEntry = customtkinter.CTkEntry(
            accountFrame,
            width=300,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Full Name",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        usernameEntry.grid(
            row=1, column=0, columnspan=3, sticky="nsew", pady=3, padx=30
        )
        useremailEntry = customtkinter.CTkEntry(
            accountFrame,
            width=300,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Email",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        useremailEntry.grid(
            row=2, column=0, columnspan=3, sticky="nsew", pady=3, padx=30
        )
        contactNumberEntry = customtkinter.CTkEntry(
            accountFrame,
            width=300,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Contact Number",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        contactNumberEntry.grid(
            row=3, column=0, sticky="nsew", columnspan=3, pady=3, padx=30
        )
        passwordEntry = customtkinter.CTkEntry(
            accountFrame,
            width=300,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Password",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        passwordEntry.grid(
            row=4, column=0, sticky="nsew", columnspan=3, pady=3, padx=30
        )
        genderEntry = customtkinter.CTkOptionMenu(
            accountFrame,
            width=300,
            height=40,
            corner_radius=5,
            font=("Georgia", 15),
            fg_color="black",
            button_color="#252525",
            button_hover_color="grey",
            dropdown_fg_color="black",
            dropdown_hover_color="#911d5a",
            text_color="white",
            values=["Prefer no to say", "Male", "Female", "Non-binary", "Other"],
            variable=userGender,
            dropdown_text_color="white",
        )
        genderEntry.grid(row=5, column=0, sticky="nsew", columnspan=3, pady=3, padx=30)
        dateEntry = customtkinter.CTkEntry(
            accountFrame,
            width=30,
            height=40,
            corner_radius=5,
            border_width=0,
            fg_color="black",
            placeholder_text="Date",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        dateEntry.grid(row=6, column=0, sticky="nsew", pady=3, padx=(30, 0))
        monthEntry = customtkinter.CTkComboBox(
            accountFrame,
            width=30,
            height=40,
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            fg_color="black",
            border_color="black",
            button_color="#252525",
            button_hover_color="grey",
            dropdown_fg_color="black",
            dropdown_hover_color="#911d5a",
            text_color="white",
            values=[
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ],
            variable=userBirthMonthSignInVar,
            dropdown_text_color="white",
        )
        monthEntry.grid(row=6, column=1, sticky="nsew", pady=3, padx=5)
        yearEntry = customtkinter.CTkEntry(
            accountFrame,
            width=30,
            height=40,
            corner_radius=5,
            border_width=0,
            fg_color="black",
            placeholder_text="Year",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        yearEntry.grid(row=6, column=2, sticky="nsew", pady=3, padx=(0, 30))
        signUpCommandButton = customtkinter.CTkButton(
            accountFrame,
            text="Continue",
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            hover_color="#911d5a",
            width=300,
            height=40,
            fg_color="#252525",
            text_color="white",
            command=CreateAccoount().widgets,
        )
        signUpCommandButton.grid(
            row=7, column=0, columnspan=3, sticky="nsew", padx=30, pady=(30, 60)
        )

        # ---------------------------------------------------------------------------------------------------

        # forget password Frame
        # ---------------------------------------------------------------------------------------------------
        customtkinter.CTkLabel(
            forgetPasswordFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\background.jpg", 1120, 700),
            anchor="center",
        ).grid(row=0, column=0, sticky="nsew")
        forgetFrame = customtkinter.CTkFrame(
            forgetPasswordFrame,
            fg_color="#171717",
            corner_radius=0,
        )
        forgetFrame.grid(row=0, column=0, sticky="n", pady=100)
        customtkinter.CTkButton(
            forgetFrame,
            text="Back",
            border_width=0,
            corner_radius=0,
            font=("Georgia", 15),
            width=25,
            height=20,
            fg_color="#171717",
            text_color="#911d5a",
            hover=False,
            command=lambda: self.showFrame(signInFrame),
        ).grid(row=0, column=0, sticky="ne", padx=10, pady=10)
        customtkinter.CTkLabel(
            forgetFrame,
            text="",
            image=self.ImageObject("Data\\Images\\Log\\logo.png", 100, 100),
            text_color="white",
            anchor="center",
        ).grid(row=1, column=0, sticky="n", pady=(30, 40))
        usernameForgetEntry = customtkinter.CTkEntry(
            forgetFrame,
            width=250,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="Email",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        usernameForgetEntry.grid(row=2, column=0, sticky="nsew", padx=30, pady=0)
        newPasswordEntry = customtkinter.CTkEntry(
            forgetFrame,
            width=250,
            height=40,
            corner_radius=10,
            border_width=0,
            fg_color="black",
            placeholder_text="New Password",
            placeholder_text_color="grey",
            font=("Georgia", 15),
            text_color="white",
        )
        newPasswordEntry.grid(row=3, column=0, sticky="nsew", pady=5, padx=30)
        forgetPasswordCodeButton = customtkinter.CTkButton(
            forgetFrame,
            text="Send OTP",
            border_width=0,
            corner_radius=5,
            font=("Georgia", 15),
            hover_color="#911d5a",
            width=35,
            height=40,
            fg_color="#252525",
            text_color="white",
            command=ResetPassword().widgets,
        )
        forgetPasswordCodeButton.grid(
            row=4, column=0, sticky="nsew", padx=30, pady=(30, 50)
        )
        # ---------------------------------------------------------------------------------------------------

        self.showFrame(signInFrame)
        self.showFrame(self.logFrame)

    # -----------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------

    def weatherGUI(self, city: str = None):
        def condition_to_url(condition):
            if condition.lower() == "partly cloudy":
                url = "Data\\Images\\Weather\\Partly cloudy.png"
            elif condition.lower() == "clear" or condition.lower() == "sunny":
                url = "Data\\Images\\Weather\\sun.png"
            elif condition.lower() == "cloudy":
                url = "Data\\Images\\Weather\\cloud.png"
            elif (
                condition.lower() == "patchy rain possible"
                or condition.lower() == "moderate rain at times"
                or condition.lower() == "light rain shower"
            ):
                url = "Data\\Images\\Weather\\Patchy rain possible.png"
            elif (
                condition.lower() == "heavy rain at times"
                or condition.lower() == "moderate or heavy rain shower"
            ):
                url = "Data\\Images\\Weather\Heavy rain at times.png"
            elif condition.lower() == "thundery outbreaks possible":
                url = "Data\\Images\\Weather\\Thundery outbreaks possible.png"
            elif condition.lower() == "patchy light rain with thunder":
                url = "Data\\Images\\Weather\\storm.png"
            else:
                url = "Data\\Images\\Weather\\sun.png"
            return url

        api_data = Weather(city).data_handling()

        # attributes of the frame
        # ---------------------------------------------------------------------------------------------------
        # current forecast----------------------------------
        current_temp = api_data.get("current_temp")
        feels_like_temp = api_data.get("feels_like_temp")
        humidity = api_data.get("humidity")
        visibility = api_data.get("visibility")
        weather_condition = api_data.get("condition")
        location = api_data.get("location")
        current_date = datetime.datetime.strftime(
            datetime.datetime.now(), "%d %B, %Y %I:%M %p"
        )
        wind_speed = api_data.get("wind_speed")
        pressure = api_data.get("pressure")
        uv_index = api_data.get("uv_index")
        min_temp = api_data.get("min_temp")
        max_temp = api_data.get("max_temp")
        precipation = api_data.get("precipation")
        rain_prediction = api_data.get("rain_prediction")
        sunrise = api_data.get("sunrise")
        sunset = api_data.get("sunset")
        # -------------------------------------------------

        # Hourly forecast-----------------------------------
        hourly_forecast = api_data.get("hourly_forecast")
        hr_1_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[0].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_1_condition = hourly_forecast[0].get("condition")
        hr_1_temp = hourly_forecast[0].get("temp")
        hr_2_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[1].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_2_condition = hourly_forecast[1].get("condition")
        hr_2_temp = hourly_forecast[1].get("temp")
        hr_3_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[2].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_3_condition = hourly_forecast[2].get("condition")
        hr_3_temp = hourly_forecast[2].get("temp")
        hr_4_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[3].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_4_condition = hourly_forecast[3].get("condition")
        hr_4_temp = hourly_forecast[3].get("temp")
        hr_5_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[4].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_5_condition = hourly_forecast[4].get("condition")
        hr_5_temp = hourly_forecast[4].get("temp")
        hr_6_time = datetime.datetime.strftime(
            datetime.datetime.strptime(
                hourly_forecast[5].get("time"), "%Y-%m-%d %H:%M"
            ),
            "%I:%M",
        )
        hr_6_condition = hourly_forecast[5].get("condition")
        hr_6_temp = hourly_forecast[5].get("temp")
        # -------------------------------------------------

        # ---------------------------------------------------------------------------------------------------

        line_style = ttk.Style()
        line_style.configure("Line.TSeparator", background="#696969")
        # current conditions frame
        # ---------------------------------------------------------------------------------------------------
        currentFrame = customtkinter.CTkFrame(
            self.weatherFrame, fg_color="#111", border_width=0, corner_radius=15
        )
        currentFrame.grid(row=0, column=0, sticky="nsew", padx=30, pady=(20, 10))
        customtkinter.CTkLabel(
            currentFrame,
            text="",
            image=self.ImageObject(condition_to_url(weather_condition), 110, 110),
            fg_color="#111",
        ).grid(row=0, column=0, padx=30, pady=(75, 5), sticky="w")
        customtkinter.CTkLabel(
            currentFrame,
            text=f"{current_temp}°C",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 40, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=30)
        customtkinter.CTkLabel(
            currentFrame,
            text=f"{weather_condition}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=0, sticky="w", padx=30)
        ttk.Separator(currentFrame, orient="horizontal", style="Line.TSeparator").grid(
            row=3, column=0, sticky="nsew", padx=(30, 100), pady=15
        )
        customtkinter.CTkLabel(
            currentFrame,
            image=self.ImageObject("Data\\Images\\Weather\\location.png", 15, 15),
            compound="left",
            text=f"   {location}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=4, column=0, sticky="w", padx=30)
        customtkinter.CTkLabel(
            currentFrame,
            image=self.ImageObject("Data\\Images\\Weather\\calendar.png", 15, 15),
            compound="left",
            text=f"   {current_date}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=5, column=0, sticky="w", padx=(30, 100), pady=(0, 20))
        # --------------------------------------------------------------------------------------------------

        # Forecast Frame code
        # --------------------------------------------------------------------------------------------------
        todayForecastFrame = customtkinter.CTkFrame(
            self.weatherFrame, fg_color="#111", border_width=0, corner_radius=15
        )
        todayForecastFrame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(10, 20))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"TODAY'S FORECAST",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=0, column=0, columnspan=11, sticky="w", padx=20, pady=(20, 10))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_1_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=0, sticky="n", padx=(30, 0))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_1_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=0, sticky="n", padx=(30, 0))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_1_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=0, sticky="n", padx=(30, 0), pady=(0, 25))
        ttk.Separator(
            todayForecastFrame, orient="vertical", style="Line.TSeparator"
        ).grid(row=1, column=1, rowspan=3, sticky="nsew", padx=30, pady=(5, 25))

        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_2_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=2, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_2_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=2, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_2_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=2, sticky="n", pady=(0, 25))
        ttk.Separator(
            todayForecastFrame, orient="vertical", style="Line.TSeparator"
        ).grid(row=1, column=3, rowspan=3, sticky="nsew", padx=30, pady=(5, 25))

        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_3_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=4, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_3_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=4, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_3_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=4, sticky="n", pady=(0, 25))
        ttk.Separator(
            todayForecastFrame, orient="vertical", style="Line.TSeparator"
        ).grid(row=1, column=5, rowspan=3, sticky="nsew", padx=30, pady=(5, 25))

        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_4_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=6, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_4_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=6, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_4_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=6, sticky="n", pady=(0, 25))
        ttk.Separator(
            todayForecastFrame, orient="vertical", style="Line.TSeparator"
        ).grid(row=1, column=7, rowspan=3, sticky="nsew", padx=30, pady=(5, 25))

        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_5_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=8, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_5_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=8, sticky="n")
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_5_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=8, sticky="n", pady=(0, 25))
        ttk.Separator(
            todayForecastFrame, orient="vertical", style="Line.TSeparator"
        ).grid(row=1, column=9, rowspan=3, sticky="nsew", padx=30, pady=(5, 25))

        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_6_time}",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=10, sticky="n", padx=(0, 30))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"",
            image=self.ImageObject(condition_to_url(hr_6_condition), 60, 60),
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=2, column=10, sticky="n", padx=(0, 30))
        customtkinter.CTkLabel(
            todayForecastFrame,
            text=f"{hr_6_temp}°C",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 17, "bold"),
        ).grid(row=3, column=10, sticky="n", padx=(0, 30), pady=(0, 25))
        # --------------------------------------------------------------------------------------------------

        # weatherConditions like humidity, pressure frame
        # --------------------------------------------------------------------------------------------------
        weatherAttributtesMainFrame = customtkinter.CTkFrame(
            self.weatherFrame, fg_color="#111", border_width=0, corner_radius=15
        )
        weatherAttributtesMainFrame.grid(
            row=0, column=1, rowspan=2, sticky="nsew", padx=(0, 40), pady=(20, 10)
        )
        weatherAttributtesFrame = customtkinter.CTkFrame(
            weatherAttributtesMainFrame,
            fg_color="#111",
            border_width=0,
            corner_radius=0,
        )
        weatherAttributtesFrame.pack(side=TOP, anchor=CENTER, padx=30)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"WEATHER CONDITIONS",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 14, "normal"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(30, 10))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\temperature.png", 20, 20),
            compound="left",
            text="   Feels Like",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(30, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{feels_like_temp}°C",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=2, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\wind.png", 20, 20),
            compound="left",
            text="   Wind",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=1, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{wind_speed} Km/h",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=2, column=1, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\drop.png", 20, 20),
            compound="left",
            text="   Humidity",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=3, column=0, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{humidity}%",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=4, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\visibility.png", 20, 20),
            compound="left",
            text="   Visibility",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=3, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{visibility} Km",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=4, column=1, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\drop.png", 20, 20),
            compound="left",
            text="   Pressure",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=5, column=0, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{pressure}",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=6, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\uv.png", 20, 20),
            compound="left",
            text="   UV Index",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=5, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{uv_index}",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=6, column=1, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\max-temp.png", 20, 20),
            compound="left",
            text="   Max Temp",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=7, column=0, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{max_temp}°C",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=8, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\min temp.png", 20, 20),
            compound="left",
            text="   Min Temp",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=7, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{min_temp}°C",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=8, column=1, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject(
                "Data\\Images\\Weather\\rain_prediction.png", 20, 20
            ),
            compound="left",
            text="   Rain Chance",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=9, column=0, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{rain_prediction}%",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=10, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\precipition.png", 20, 20),
            compound="left",
            text="   Precipition",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=9, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{precipation}%",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=10, column=1, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\sunrise.png", 20, 20),
            compound="left",
            text="   Sunrise",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=11, column=0, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{sunrise}",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=12, column=0, sticky="n", padx=20)
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            image=self.ImageObject("Data\\Images\\Weather\\sunset.png", 20, 20),
            compound="left",
            text="   Sunset",
            text_color="#d2d2d4",
            fg_color="#111",
            font=("Sitka Small", 12, "normal"),
        ).grid(row=11, column=1, sticky="w", padx=20, pady=(25, 0))
        customtkinter.CTkLabel(
            weatherAttributtesFrame,
            text=f"{sunset}",
            text_color="#fff",
            fg_color="#111",
            font=("Sitka Small", 15, "normal"),
        ).grid(row=12, column=1, sticky="n", padx=20)

        # --------------------------------------------------------------------------------------------------
        self.showFrame(self.weatherFrame)

    # --------------------------------------------------------------------------------------------------------------

    # Mili Games
    # --------------------------------------------------------------------------------------------------------------
    def Games(self):
        customtkinter.CTkLabel(
            self.gameConsoleFrame,
            text="  Games",
            font=("Cooper Black", 50, "normal"),
            image=self.ImageObject("Data\\Images\\Games\\gamepad.png", 50, 50),
            compound="left",
            anchor="center",
            text_color="aqua",
        ).pack(side=TOP, anchor=CENTER, pady=40)
        gameIconsFrame = customtkinter.CTkFrame(
            self.gameConsoleFrame,
            fg_color="#252525",
            border_width=0,
            corner_radius=15,
        )
        gameIconsFrame.pack(side=TOP, anchor=CENTER, pady=50)
        customtkinter.CTkButton(
            gameIconsFrame,
            text="Tic Tac Toe",
            font=("Sitka Small", 15, "bold"),
            height=150,
            image=self.ImageObject("Data\\Images\\Games\\tic-tac-toe.png", 80, 80),
            compound="top",
            border_width=1,
            corner_radius=10,
            border_color="#1ed760",
            anchor="center",
            fg_color="#252525",
            hover_color="#393939",
            text_color="#1ed760",
            command=self.tic_tac_toe,
        ).grid(row=0, column=0, sticky="nsew", padx=(40, 20), pady=40)
        customtkinter.CTkButton(
            gameIconsFrame,
            text="Quizard",
            font=("Sitka Small", 15, "bold"),
            height=150,
            image=self.ImageObject("Data\\Images\\Games\\quiz.png", 80, 80),
            compound="top",
            anchor="center",
            border_width=1,
            corner_radius=10,
            border_color="#1ed760",
            fg_color="#252525",
            hover_color="#393939",
            text_color="#1ed760",
            command=self.quiz_game,
        ).grid(row=0, column=1, sticky="nsew", padx=20, pady=40)
        customtkinter.CTkButton(
            gameIconsFrame,
            text="Hangman",
            font=("Sitka Small", 15, "bold"),
            height=150,
            image=self.ImageObject("Data\\Images\\Games\\quiz.png", 80, 80),
            compound="top",
            anchor="center",
            border_width=1,
            corner_radius=10,
            border_color="#1ed760",
            fg_color="#252525",
            hover_color="#393939",
            text_color="#1ed760",
        ).grid(row=0, column=2, sticky="nsew", padx=(20, 40), pady=40)

        self.showFrame(self.gameConsoleFrame)

    # Quiz Game
    # ---------------------------------------------------------------------------------------------------------------
    def quiz_game(self):
        # Retreiving quiz data from opendtb api
        # -------------------------------------------------------------------------------------------------
        def api_call(url):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showwarning("Mili", "Please check your internet connection")
                start_btn.configure(command=lambda: Thread(target=load_game).start())
                return None

        # -------------------------------------------------------------------------------------------------

        # Parsing and customizing the data
        # -------------------------------------------------------------------------------------------------
        def parse_data(data: dict) -> list:
            response = data.get("results")
            parsed_data = []
            progress = 0.5
            for result in response:
                question = str(result.get("question"))
                question = question.replace("&#039;", "'")
                question = question.replace("&quot;", '"')
                correct_answer = result.get("correct_answer")
                incorrect_answers = list(result.get("incorrect_answers"))
                incorrect_answers.append(correct_answer)
                options = incorrect_answers.copy()
                # Shuffling the options of answers
                random.shuffle(options)
                data = {
                    "question": question,
                    "correct_answer": correct_answer,
                    "options": options,
                }
                parsed_data.append(data)
                progress += 0.05
                progress_bar.set(progress)
            return parsed_data

        # -------------------------------------------------------------------------------------------------

        # Result of the quiz
        # -------------------------------------------------------------------------------------------------
        def result():
            resultFrame = customtkinter.CTkFrame(self, fg_color="#252525")
            resultFrame.grid(row=0, column=0, sticky="nsew")
            customtkinter.CTkLabel(
                resultFrame,
                text="",
                image=self.ImageObject("Data\\Images\\Games\\trophy.png", 300, 300),
                fg_color="#252525",
            ).pack(side=TOP, anchor=CENTER, pady=50)
            customtkinter.CTkLabel(
                resultFrame,
                text=f"Congrats You Earn {score.get()} Points",
                text_color="#fff",
                font=("Sitka Small", 20, "bold"),
            ).pack(side=TOP, anchor="center", pady=15)
            customtkinter.CTkButton(
                resultFrame,
                text="Close",
                text_color="#111",
                fg_color="#1ed760",
                hover_color="#19b04f",
                font=("Sitka Small", 15, "bold"),
                height=40,
                width=130,
                command=lambda: self.quit(),
            ).pack(side=TOP, anchor=CENTER)
            self.showFrame(resultFrame)

        # This function updates the questions and their options
        # -------------------------------------------------------------------------------------------------
        def _quiz(data: dict):
            def check_answer(predicted_ans, correct_ans, index):
                if predicted_ans == correct_ans:
                    if index == 3:
                        optionbtn0.configure(text_color="#1ed760", hover=False)
                    elif index == 2:
                        optionbtn1.configure(text_color="#1ed760", hover=False)
                    elif index == 1:
                        optionbtn2.configure(text_color="#1ed760", hover=False)
                    elif index == 0:
                        optionbtn3.configure(text_color="#1ed760", hover=False)
                    optionbtn0.configure(command=None)
                    optionbtn1.configure(command=None)
                    optionbtn2.configure(command=None)
                    optionbtn3.configure(command=None)
                    marks = score.get()
                    marks += 1
                    score.set(marks)
                else:
                    if index == 3:
                        optionbtn0.configure(
                            text_color="red", hover=False, command=None
                        )
                    elif index == 2:
                        optionbtn1.configure(
                            text_color="red", hover=False, command=None
                        )
                    elif index == 1:
                        optionbtn2.configure(
                            text_color="red", hover=False, command=None
                        )
                    elif index == 0:
                        optionbtn3.configure(
                            text_color="red", hover=False, command=None
                        )
                    optionbtn0.configure(command=None)
                    optionbtn1.configure(command=None)
                    optionbtn2.configure(command=None)
                    optionbtn3.configure(command=None)

                q = questionNo.get()
                q += 1
                questionNo.set(q)

            question = data.get("question")
            options = data.get("options")
            correct_answer = data.get("correct_answer")
            customtkinter.CTkLabel(
                quizFrame,
                text="",
                image=self.ImageObject("Data\\Images\\Games\\thinking.png", 150, 150),
                fg_color="#252525",
            ).grid(row=1, column=0, sticky="n")
            qna_frame = customtkinter.CTkScrollableFrame(
                quizFrame,
                fg_color="#252525",
                corner_radius=0,
                height=400,
                width=890,
                scrollbar_button_hover_color="#252525",
                scrollbar_fg_color="#252525",
                scrollbar_button_color="#252525",
            )
            qna_frame.grid(row=1, column=0, sticky="nsew", padx=100, pady=(140, 0))
            question_Frame = customtkinter.CTkFrame(
                qna_frame,
                height=80,
                border_color="black",
                corner_radius=10,
                fg_color="#111",
            )
            question_Frame.pack(side=TOP, anchor=CENTER, fill=X, padx=20, pady=(0, 30))
            customtkinter.CTkLabel(
                question_Frame,
                text=f"Q{questionNo.get()} {question}",
                text_color="#fff",
                font=("Sitka Small", 14, "normal"),
                wraplength=790,
            ).pack(side=TOP, anchor="nw", pady=30, padx=30)
            optionbtn0 = customtkinter.CTkButton(
                qna_frame,
                text=f"  D. {options[3]}",
                fg_color="#191919",
                anchor="w",
                hover_color="#111",
                height=50,
                font=("Sitka Small", 14, "normal"),
                text_color="#fff",
                command=lambda: check_answer(options[3], correct_answer, 3),
            )
            optionbtn0.pack(side=BOTTOM, anchor=CENTER, padx=20, pady=2, fill=X)
            optionbtn1 = customtkinter.CTkButton(
                qna_frame,
                text=f"  C. {options[2]}",
                fg_color="#191919",
                anchor="w",
                hover_color="#111",
                height=50,
                font=("Sitka Small", 14, "normal"),
                text_color="#fff",
                command=lambda: check_answer(options[2], correct_answer, 2),
            )
            optionbtn1.pack(side=BOTTOM, anchor=CENTER, padx=20, pady=2, fill=X)
            optionbtn2 = customtkinter.CTkButton(
                qna_frame,
                text=f"  B. {options[1]}",
                fg_color="#191919",
                anchor="w",
                hover_color="#111",
                height=50,
                font=("Sitka Small", 14, "normal"),
                text_color="#fff",
                command=lambda: check_answer(options[1], correct_answer, 1),
            )
            optionbtn2.pack(side=BOTTOM, anchor=CENTER, padx=20, pady=2, fill=X)
            optionbtn3 = customtkinter.CTkButton(
                qna_frame,
                text=f"  A. {options[0]}",
                fg_color="#191919",
                anchor="w",
                hover_color="#111",
                height=50,
                font=("Sitka Small", 14, "normal"),
                text_color="#fff",
                command=lambda: check_answer(options[0], correct_answer, 0),
            )
            optionbtn3.pack(side=BOTTOM, anchor=CENTER, padx=20, pady=2, fill=X)
            qna_frame.update()
            self.showFrame(qna_frame)

        # -------------------------------------------------------------------------------------------------

        # Loading the game
        # Here the game starts
        # -------------------------------------------------------------------------------------------------
        def load_game():
            def next_question(data):
                question = questionNo.get()
                if question == 11:
                    result()
                else:
                    _quiz(data[question - 1])
                score_label.configure(text=f"Score {score.get()}/10")

            mode = difficulty_mode.get()
            if mode == "" or mode == "Mode" or mode is None:
                messagebox.showwarning(
                    "Mili", "Please select your preferred difficulty level"
                )
            else:
                start_btn.configure(command=None)
                if mode == "Easy":
                    url = "https://opentdb.com/api.php?amount=10&difficulty=easy&type=multiple"
                elif mode == "Medium":
                    url = "https://opentdb.com/api.php?amount=10&difficulty=medium&type=multiple"
                else:
                    url = "https://opentdb.com/api.php?amount=10&difficulty=hard&type=multiple"

                progress_bar.pack(side=TOP, anchor=CENTER, pady=(10, 3))
                progress_bar.set(0)
                quiz_data = api_call(url)
                if quiz_data is not None:
                    progress_bar.set(0.5)
                    parsed_data = parse_data(quiz_data)
                    score_label = customtkinter.CTkLabel(
                        quizFrame,
                        text=f"Score {score.get()}/10",
                        text_color="#fff",
                        font=("Sitka Small", 18, "bold"),
                    )
                    score_label.grid(
                        row=0, column=0, sticky="nw", pady=(15, 0), padx=30
                    )
                    next_btn = customtkinter.CTkButton(
                        quizFrame,
                        text="Next",
                        text_color="#111",
                        fg_color="#1ed760",
                        hover_color="#19b04f",
                        font=("Sitka Small", 15, "normal"),
                        height=40,
                        width=130,
                        command=lambda: next_question(parsed_data),
                    )
                    next_btn.grid(row=2, column=0, sticky="se", pady=0, padx=30)
                    _quiz(parsed_data[0])
                    self.showFrame(quizFrame)

        # -------------------------------------------------------------------------------------------------

        difficulty_mode = StringVar()
        difficulty_mode.set("Mode")
        questionNo = IntVar()
        questionNo.set(1)
        score = IntVar()
        score.set(0)

        loadFrame = customtkinter.CTkFrame(self, fg_color="#252525", corner_radius=0)
        loadFrame.grid(row=0, column=0, sticky="nsew")
        quizFrame = customtkinter.CTkFrame(self, fg_color="#252525", corner_radius=0)
        quizFrame.grid(row=0, column=0, sticky="nsew")
        customtkinter.CTkLabel(
            loadFrame,
            text="Quizard",
            text_color="#fff",
            font=("Cooper Black", 60, "normal"),
        ).pack(side=TOP, anchor="center", pady=(70, 0))
        customtkinter.CTkLabel(
            loadFrame,
            text="Get ready to test your knowledge and challenge your wits in our thrilling quiz game,\nwhere every question brings excitement and a chance to become the ultimate champion!",
            text_color="#fff",
            font=("Sitka Small", 13, "normal"),
        ).pack(side=TOP, anchor="center", pady=15)
        customtkinter.CTkOptionMenu(
            loadFrame,
            height=40,
            width=130,
            fg_color="#111",
            button_color="#111",
            dropdown_fg_color="#202020",
            button_hover_color="#191919",
            text_color="#fff",
            variable=difficulty_mode,
            font=("Sitka Small", 15, "normal"),
            dropdown_font=("Sitka Small", 13, "normal"),
            dropdown_hover_color="#393939",
            values=["Easy", "Medium", "Hard"],
        ).pack(side=TOP, anchor="center", pady=(20, 10))
        start_btn = customtkinter.CTkButton(
            loadFrame,
            text="Start Game",
            text_color="#111",
            fg_color="#1ed760",
            hover_color="#19b04f",
            font=("Sitka Small", 15, "normal"),
            height=40,
            width=130,
            command=lambda: Thread(target=load_game).start(),
        )
        start_btn.pack(side=TOP, anchor="center", pady=10)
        progress_bar = customtkinter.CTkProgressBar(
            loadFrame,
            width=300,
            height=10,
            orientation="horizontal",
            mode="determinate",
            fg_color="#111",
            progress_color="#1ed760",
        )
        self.showFrame(loadFrame)

    # --------------------------------------------------------------------------------------------------------------

    # Tic Tac Toe Game
    # --------------------------------------------------------------------------------------------------------------
    def tic_tac_toe(self):
        def resetGame():
            lock.acquire()
            winnerLabel.configure(text="")

            for i in range(9):
                board[i] = -1

            b0.configure(
                text="",
                command=lambda: Thread(target=move, args=(0,)).start(),
            )
            b1.configure(
                text="",
                command=lambda: Thread(target=move, args=(1,)).start(),
            )
            b2.configure(
                text="",
                command=lambda: Thread(target=move, args=(2,)).start(),
            )
            b3.configure(
                text="",
                command=lambda: Thread(target=move, args=(3,)).start(),
            )
            b4.configure(
                text="",
                command=lambda: Thread(target=move, args=(4,)).start(),
            )
            b5.configure(
                text="",
                command=lambda: Thread(target=move, args=(5,)).start(),
            )
            b6.configure(
                text="",
                command=lambda: Thread(target=move, args=(6,)).start(),
            )
            b7.configure(
                text="",
                command=lambda: Thread(target=move, args=(7,)).start(),
            )
            b8.configure(
                text="",
                command=lambda: Thread(target=move, args=(8,)).start(),
            )
            lock.release()

        def winnerEvent():
            buttons = [b0, b1, b2, b3, b4, b5, b6, b7, b8]
            remainingPositions = [x for x, value in enumerate(board) if value == -1]
            for postion in remainingPositions:
                buttons[postion].configure(command=None)

        def move(index):
            lock.acquire()
            buttons = [b0, b1, b2, b3, b4, b5, b6, b7, b8]
            if isBoardFull():
                winnerLabel.configure(text="Draw!")
                winnerEvent()
            else:
                buttons[index].configure(text="O", text_color="#fff", command=None)
                board[index] = 0
                if isWinner(board, 0):
                    winnerLabel.configure(text="O wins the game")
                    winnerEvent()
                else:
                    if isBoardFull():
                        winnerLabel.configure(text="Draw!")
                        winnerEvent()
                    else:
                        time.sleep(0.4)
                        computerTurn = computerMove()
                        buttons[computerTurn].configure(
                            text="X", text_color="aqua", command=None
                        )
                        board[computerTurn] = 1
                        if isWinner(board, 1):
                            winnerLabel.configure(text="X wins the game")
                            winnerEvent()
            lock.release()

        def isWinner(boardCopy, value):
            if (
                (
                    boardCopy[0] == value
                    and boardCopy[1] == value
                    and boardCopy[2] == value
                )
                or (
                    boardCopy[3] == value
                    and boardCopy[4] == value
                    and boardCopy[5] == value
                )
                or (
                    boardCopy[6] == value
                    and boardCopy[7] == value
                    and boardCopy[8] == value
                )
                or (
                    boardCopy[0] == value
                    and boardCopy[4] == value
                    and boardCopy[8] == value
                )
                or (
                    boardCopy[2] == value
                    and boardCopy[4] == value
                    and boardCopy[6] == value
                )
                or (
                    boardCopy[0] == value
                    and boardCopy[3] == value
                    and boardCopy[6] == value
                )
                or (
                    boardCopy[1] == value
                    and boardCopy[4] == value
                    and boardCopy[7] == value
                )
                or (
                    boardCopy[2] == value
                    and boardCopy[5] == value
                    and boardCopy[8] == value
                )
            ):
                return True
            else:
                return False

        def isBoardFull():
            if board.count(-1) > 0:
                return False
            else:
                return True

        def computerMove():
            # list containing all values -1
            possibleMoves = [x for x, letter in enumerate(board) if letter == -1]
            turn = 0
            for let in [1, 0]:
                for i in possibleMoves:
                    boardCopy = board.copy()
                    boardCopy[i] = let
                    if isWinner(boardCopy, let):
                        turn = i
                        return turn
            edgesMoves = []
            for i in possibleMoves:
                if i in (1, 3, 5, 7):
                    edgesMoves.append(i)

            if len(edgesMoves) > 0:
                turn = randomMove(edgesMoves)
                return turn

            if 4 in possibleMoves:
                turn = 5
                return turn

            cornerMoves = []
            for i in possibleMoves:
                if i in (0, 2, 6, 8):
                    cornerMoves.append(i)

            if len(cornerMoves) > 0:
                turn = randomMove(cornerMoves)
                return turn

        def randomMove(li):
            import random

            r = random.randrange(0, len(li))
            return li[r]

        lock = Lock()
        board = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        line_style = ttk.Style()
        line_style.configure("Line.TSeparator", background="#1ed760")
        mainFrame = customtkinter.CTkFrame(self, fg_color="#252525", corner_radius=0)
        mainFrame.grid(row=0, column=0, sticky="nsew")

        customtkinter.CTkLabel(
            mainFrame,
            text="Tic Tac Toe",
            fg_color="#252525",
            text_color="aqua",
            font=("Cooper Black", 50, "normal"),
        ).pack(side=TOP, anchor=CENTER, pady=30)
        tableFrame = customtkinter.CTkFrame(
            mainFrame, fg_color="#191919", corner_radius=10
        )
        tableFrame.pack(side=TOP, anchor="center")
        b0 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(0,)).start(),
        )
        b0.grid(row=0, column=0, padx=(70, 0), pady=(70, 0))
        ttk.Separator(tableFrame, orient="horizontal", style="Line.TSeparator").grid(
            row=1, column=0, columnspan=5, sticky="nsew", padx=90
        )
        ttk.Separator(tableFrame, orient="vertical", style="Line.TSeparator").grid(
            row=0, column=1, rowspan=5, sticky="nsew", pady=90
        )
        b1 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(1,)).start(),
        )
        b1.grid(row=0, column=2, pady=(70, 0))
        b2 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(2,)).start(),
        )
        b2.grid(row=0, column=4, padx=(0, 70), pady=(70, 0))
        b3 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(3,)).start(),
        )
        b3.grid(row=2, column=0, padx=(70, 0))
        b4 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(4,)).start(),
        )
        b4.grid(row=2, column=2)
        b5 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(5,)).start(),
        )
        b5.grid(row=2, column=4, padx=(0, 70))
        ttk.Separator(tableFrame, orient="horizontal", style="Line.TSeparator").grid(
            row=3, column=0, columnspan=5, sticky="nsew", padx=90
        )
        ttk.Separator(tableFrame, orient="vertical", style="Line.TSeparator").grid(
            row=0, column=3, rowspan=5, sticky="nsew", pady=90
        )
        b6 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(6,)).start(),
        )
        b6.grid(row=4, column=0, padx=(70, 0), pady=(0, 70))
        b7 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(7,)).start(),
        )
        b7.grid(row=4, column=2, pady=(0, 70))
        b8 = customtkinter.CTkButton(
            tableFrame,
            fg_color="#191919",
            height=70,
            width=70,
            corner_radius=0,
            hover=False,
            text="",
            font=("Cooper Black", 50, "normal"),
            command=lambda: Thread(target=move, args=(8,)).start(),
        )
        b8.grid(row=4, column=4, padx=(0, 70), pady=(0, 70))
        customtkinter.CTkButton(
            mainFrame,
            text="Reset",
            font=("Sitka Small", 16, "bold"),
            text_color="#111",
            fg_color="#1ed760",
            hover_color="#19b04f",
            height=40,
            width=130,
            command=lambda: Thread(target=resetGame).start(),
        ).pack(side=BOTTOM, anchor=CENTER, pady=(0, 40))
        winnerLabel = customtkinter.CTkLabel(
            mainFrame, text="", font=("Sitka Small", 25, "bold")
        )
        winnerLabel.pack(side=BOTTOM, anchor="center", pady=20)
        self.showFrame(mainFrame)


if __name__ == "__main__":
    app = GUI()
    app.Profile()

    # app.Log()
    # app.weatherGUI()
    # app.Games()
    app.mainloop()
