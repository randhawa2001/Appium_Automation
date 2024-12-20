from appium import webdriver
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.options.ios import xcuitest
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randrange
import random
import sys
import requests
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

device = sys.argv[1]
#mongo db collection for logs for script while runnning!!

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["device_db"]
except Exception as e: 
    print(f"Error connecting to Mongodb:  {str(e)}")
    sys.exit(1)


script_logs_collection = db["script_logs"]

def log_to_mongo_and_console(message, level="INFO"):
    """Logs messages to MongoDB and displays them on the console."""
    log_entry = {
        "device_id": device,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "message": message,
    }
    script_logs_collection.insert_one(log_entry)
    print(f"{log_entry['timestamp']} [{level}] {message}")

def crane(container):
    log_to_mongo_and_console("Crane Running....")
    try:
        driver.terminate_app('com.spotify.client')
        # time.sleep(5)
        log_to_mongo_and_console("Terminated Spotify app.")
    except:
        log_to_mongo_and_console(f"Failed to terminate Spotify app: {str(e)}", "ERROR")
    for i in range(1):
            try:
                driver.execute_script("mobile: pressButton", {"name": "home"})
                time.sleep(1.5)
                log_to_mongo_and_console("Pressed Home button.")
            except Exception as e:
                time.sleep(0.5)
                log_to_mongo_and_console(f"Home button error: {str(e)}", "ERROR")
                
    try:
        driver.page_source  # Trigger accessibility snapshot
        log_to_mongo_and_console("Forced accessibility tree refresh.")
    except Exception as e:
        log_to_mongo_and_console(f"Error refreshing accessibility tree: {str(e)}", "ERROR")

    # try:
    #     active_app = driver.execute_script("mobile: getCurrentApp")
    #     log_to_mongo_and_console(f"Current active app: {active_app}")
    #     if active_app.get("bundleId") != "com.apple.springboard":
    #         raise Exception("Home screen not detected.")
    # except Exception as e:
    #     log_to_mongo_and_console(f"Error checking active app: {str(e)}", "ERROR")    
    while True:
        try:
            
            spotify_icon = driver.find_element(By.XPATH, '//*[@label="Spotify"]')
            # instagram = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Spotify")
        #     spotify_icon = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Spotify"))
        # )
            # spotify_icon = driver.find_element(AppiumBy.IOS_PREDICATE, 'label == "Spotify"')
            action = TouchAction(driver)
            action.long_press(spotify_icon).release().perform()
            driver.refresh
            log_to_mongo_and_console("Long pressed on Spotify.")
            
            
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[contains(@label,"Container")]').click()
            log_to_mongo_and_console("Clicked on Container.")
            
            break
        except Exception as e:
            log_to_mongo_and_console(f"Error interacting with Spotify : {str(e)}", "ERROR")
            
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@label="' + str(container) + '"]').click()
            time.sleep(1.5)
            log_to_mongo_and_console(f"Clicked on container: {container}.")
            break
        except Exception as e:
            log_to_mongo_and_console(f"Container '{container}' not found: {str(e)}", "ERROR")
            time.sleep(0.5)
    try:
        rotateIP()
        log_to_mongo_and_console("IP rotated successfully.")
        
        time.sleep(0.5)
    except Exception as e:
        log_to_mongo_and_console(f"IP rotation failed: {str(e)}", "ERROR")

    try:
        driver.activate_app("com.spotify.client")
        log_to_mongo_and_console("Spotify app activated.")
       
        time.sleep(1)
    except Exception as e:
        log_to_mongo_and_console(f"Failed to activate Spotify app: {str(e)}", "ERROR")

    return

def rotateIP():
    catchIssue = 0
    
    log_to_mongo_and_console("Rotating IP...")
    while True:
        try:
            driver.activate_app("com.apple.shortcuts")
            log_to_mongo_and_console("Activated Shortcuts app.")
            break
        except Exception as e:
            log_to_mongo_and_console(f"Failed to activate Shortcuts app: {str(e)}", "ERROR")
            time.sleep(1)

    while True:
        try:
            driver.find_element(By.XPATH, '//*[@name="IP"]').click()
            time.sleep(2)
            
            log_to_mongo_and_console("IP rotated successfully!")
            break
        except Exception as e:
            log_to_mongo_and_console(f"Failed to rotate IP: {str(e)}", "ERROR")
            time.sleep(1)

    """
            loop to terminate apple shortcuts
    """
    while True:
        try:
            driver.terminate_app("com.apple.shortcuts")
            log_to_mongo_and_console("Shortcuts app terminated.")
            return
        except Exception as e:
            log_to_mongo_and_console(f"Failed to terminate Shortcuts app: {str(e)}", "ERROR")
            time.sleep(1)



desired_caps = {
    "xcodeOrgId": "",
    "xcodeSigningId": "",
    "platformName": "",
    "automationName": "",
    "udid": sys.argv[1],
    "deviceName": "iPhone",
    "bundleId": "com.spotify.client",
    "updatedWDABundleID": "",
    "showXcodeLog": True,
    "newCommandTimeout": "1000",
    "useNewWDA": True,
    "wdaLocalPort":sys.argv[9],
    "noReset": True,
    "resetOnSessionStartOnly": False,
}


while True:
    try:
        log_to_mongo_and_console("Attempting to start the Appium driver...")
        driver = webdriver.Remote("http://localhost:1111/wd/hub", desired_caps)
        log_to_mongo_and_console("Appium driver started successfully.")
        
        break
    except Exception as e:
        error_message = (
            "Driver initialization failed. Ensure the Appium server is running and "
            "your device's JB is still active. Error details: " + str(e)
        )
        log_to_mongo_and_console(error_message, "ERROR")
        time.sleep(0.5)

# Check if the bot is in the configured sleep schedule
def is_in_sleep_schedule(start_time, end_time):
    """Check if the current time is within the defined sleep schedule."""
    try:
        now = time.localtime()
        current_time = time.strftime("%H:%M", now)
        in_schedule = start_time <= current_time <= end_time
        log_to_mongo_and_console(
            f"Current time: {current_time}. Sleep schedule: {start_time} to {end_time}. In schedule: {in_schedule}"
        )
        return in_schedule
    except Exception as e:
        log_to_mongo_and_console(f"Error checking sleep schedule: {str(e)}", "ERROR")
        return False
try:
    
    timeFrom = int(sys.argv[2])
    timeTo = int(sys.argv[3])
    cloneList = sys.argv[4].split(",")
    playlists = sys.argv[5].split(",")
    inputType = sys.argv[6]
    songTimeFrom = int(sys.argv[7])
    songTimeTo = int(sys.argv[8])
    wdaLocalPort = int(sys.argv[9])  #to help run two different devices for threading!
    sleep_schedule_start = sys.argv[10]  # Sleep schedule start 
    sleep_schedule_end = sys.argv[11]  # Sleep schedule end
    pause_chance = int(sys.argv[12])  # Chance to pause a song in percentage
    pause_min_duration = int(sys.argv[13])  # Minimum pause duration in seconds
    pause_max_duration = int(sys.argv[14])  # Maximum pause duration in seconds
    skip_after_seconds = int(sys.argv[15])  # Force skip after this many seconds
    

    log_to_mongo_and_console(
    f"Inputs parsed successfully: timeFrom={timeFrom}, timeTo={timeTo}, "
    f"cloneList={cloneList}, playlists={playlists}, inputType={inputType}, "
    f"songTimeFrom={songTimeFrom}, songTimeTo={songTimeTo}, wdaLocalPort={wdaLocalPort}, "
    f"sleep_schedule_start={sleep_schedule_start}, sleep_schedule_end={sleep_schedule_end}, "
    f"pause_chance={pause_chance}%, pause_min_duration={pause_min_duration}s, "
    f"pause_max_duration={pause_max_duration}s, skip_after_seconds={skip_after_seconds}s."
    )

except Exception as e:
    log_to_mongo_and_console(f"Error parsing input arguments: {str(e)}", "ERROR")
    sys.exit(1)

# LOGGING CLONES FOR VERIFICATION PURPOSES!!!
log_to_mongo_and_console(f"Clones: {cloneList}")

while True:
    for clone in cloneList:
        try:
            crane(clone)
            log_to_mongo_and_console("Crane execution completed!")
            
        except Exception as e:
            log_to_mongo_and_console(f"Crane execution has an error : {str(e)}")
            
        for playlist in playlists:
            report = 0
            while True:
                randomTime = random.randint(timeFrom, timeTo)

                #This loop is run when fail to find element!
                if report == 5:
                    while True:
                        try:
                            log_to_mongo_and_console("Spotify is being restarted....")
                            driver.terminate_app('com.spotify.client')
                            log_to_mongo_and_console("Spotify Terminated.")
                            time.sleep(2)
                            break
                        except:
                            time.sleep(0.5)
                            log_to_mongo_and_console("Spotify Termination Error.")
                         
                    while True:
                        try:
                            driver.activate_app("com.spotify.client")
                            log_to_mongo_and_console("Spotify Activated Again!")
                            time.sleep(2)
                            break
                        except:
                            time.sleep(0.5)
                            log_to_mongo_and_console("")
                         
                try:
                    #Xpath is for Search Icon
                    driver.find_element(By.XPATH, '//*[@name="tabbar-item-find"]').click()
                    log_to_mongo_and_console("Clicked on Search Button.")
                    
                    time.sleep(1.5)
                    break
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console("Failed to click on Search Button.")
               
               
                report += 1

            tries = 0
            while True:
                time.sleep(3)
                log_to_mongo_and_console("Moved to Second Page..")
                
                try: #Xpath is for searchbar!
                    driver.find_element(By.XPATH, '//*[@name="SearchHeaderFind.SearchBar"]').click()
                    log_to_mongo_and_console("Clicked on Search Bar...")
                   
                    time.sleep(1.5)
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console("Failed to click on Search Bar...")
                    
                    driver.refresh

                try:#Xpath is for search field to type!
                    driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').send_keys(str(playlist))
                    log_to_mongo_and_console("Entered playlist name in Search Bar!")
                    
                    time.sleep(2)
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console("Failed to enter playlist name in searchbar field!")
                   
                    driver.refresh

                try:# To check whether the tab is filled or not!
                    searchField = str(driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').text)
                    # print("Search field: " + str(searchField))
                   
                    if searchField == str(playlist):
                        log_to_mongo_and_console(f"Succesfully Entered Playlist name : {searchField}")
                        
                        break
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console(f"Unsuccesfully Entered Playlist name : {searchField}")
                   


                # try:
                #     driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').clear()
                #     print("Search field cleared")
                #     time.sleep(1)
                # except:
                #     time.sleep(0.5)
                #     print("Search Field not found")
            while True:
            #     try:
            #         driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
            #         time.sleep(1.5)
            #     except:
            #         pass
            #     try:
            #         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
            #         time.sleep(1.5)
            #     except:
            #         pass
            #     try:
            #         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
            #         time.sleep(1.5)
            #     except:
            #         pass
                try:
                    driver.find_element(By.XPATH, '//*[@name="Search"]').click()
                    log_to_mongo_and_console(f"Succesfully Clicked on Search Button!")
                    
                    time.sleep(5)
                    
                    
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console(f"Didnt click on Search Button!")
                    
                try: 
                    driver.find_element(By.XPATH, '//XCUIElementTypeOther[@name="search.results"]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView/XCUIElementTypeCell[1]/XCUIElementTypeOther/XCUIElementTypeOther').click()
                    log_to_mongo_and_console(f"Succesfully Clicked on Playlist 1")
                    break
                except:
                    log_to_mongo_and_console(f"Failed to click on Playlist 1")
            
                # while True:
                #     #This condition only edits the playlists names accordingly!
                #     if inputType == "Albums":
                #         playlist = playlist.replace(" -", ",")

                #     # try:
                #     #     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                #     #     time.sleep(1.5)
                #     # except:
                #     #     pass
                #     # try:
                #     #     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
                #     #     time.sleep(1.5)
                #     # except:
                #     #     pass
                #     # try:
                #     #     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
                #     #     time.sleep(1.5)
                #     # except:
                #     #     pass
                    
                    
                #     try:
                #         driver.find_element(By.XPATH, '(//*[contains(@label, "' + str(playlist) + '")])[1]').click()
                #         log_to_mongo_and_console(f"Clicked on the Playlist: {str(playlist)}")
                #         print("Clicked on Playlist!")
                #         time.sleep(3)
                #         break
                        
                #     except:
                #         time.sleep(0.5)
                #         print("Playlist: " + str(playlist) + " not found")
                #         log_to_mongo_and_console(f"Playlist Not Found: {str(playlist)}")

                #     try:
                #         print("Scrolling a bit")
                #         action = TouchAction(driver)
                #         action.long_press(None, 170, 556).move_to(None, 170, 120).release().perform()
                #         log_to_mongo_and_console(f"Scrolling playlist section...")
                #         time.sleep(1)
                #     except:
                #         print("Scrolling error")
                #         log_to_mongo_and_console(f"Scrolling Error!!")
            start_time = songTimeFrom
            playlist_start_time = songTimeTo
            songTime = random.randint(songTimeFrom, songTimeTo)
            while True:
                # try:
                #     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                #     time.sleep(1.5)
                # except:
                #     pass
                # try:
                #     driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                #     time.sleep(1.5)
                # except:
                #     pass
                # try:
                #     driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                #     time.sleep(1.5)
                # except:
                #     pass
                try:
                    ##Below Xpath is for the Main Play button of playlist!
                    time.sleep(4)
                    driver.find_element(By.XPATH, '//*[@name="header-play-button"]').click()
                    log_to_mongo_and_console("Clicked on Playlist Main play button!")
                    time.sleep(2)
                    
                    log_to_mongo_and_console("Playing playlist for: " + str(randomTime) + " seconds")
                except:
                    log_to_mongo_and_console("Error Clicking on Play button of Playlist!")
                    time.sleep(0.5)

                try: #SPTNowPlayingBar
                    # driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
                    driver.find_element(By.XPATH, '//*[@name="SPTNowPlayingBar"]').click()
                    
                    log_to_mongo_and_console("Clicked on current playing song bar!")
                    time.sleep(1.5)
                except:
                    time.sleep(0.5)
                    log_to_mongo_and_console("Error clicking on playing song bar!")
                    

                while True:
                    # try:
                    #     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                    #     time.sleep(1.5)
                    # except:
                    #     pass
                    # try:
                    #     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
                    #     time.sleep(1.5)
                    # except:
                    #     pass
                    # try:
                    #     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
                    #     time.sleep(1.5)
                    # except:
                    #     pass
                    current_time = time.time()
                    playlist_elapsed_time = current_time - playlist_start_time
                    elapsed_time = current_time - start_time
                   
                    log_to_mongo_and_console("Playing song for: " + str(songTime) + " seconds")
                    log_to_mongo_and_console(f"{str(clone)} playlist/album elapsed time: {playlist_elapsed_time} seconds")
                    if elapsed_time > songTime:
                        # print("We have played the song for: " + str(songTime) + " seconds")
                        log_to_mongo_and_console("We have played the song for: " + str(songTime) + " seconds")
                        try:
                            driver.find_element(By.XPATH, '//*[contains(@label,"Next")]').click()
                            log_to_mongo_and_console("Clicked on Next Song!")
                            songTime = random.randint(songTimeFrom, songTimeTo)
                            log_to_mongo_and_console(f"Next song will play for {songTime} seconds")
                            start_time = time.time()  # Reset start_time for the next song
                            break
                        except:
                            time.sleep(0.5)
                            # print("Next song not found")
                            log_to_mongo_and_console("Next Song not Found!")
                            try:
                                driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
                                log_to_mongo_and_console("Clicked on Now Playing")
                                time.sleep(1.5)
                            except:
                                time.sleep(0.5)
                                log_to_mongo_and_console("Now Playing not found")
                    if playlist_elapsed_time > randomTime:
                        log_to_mongo_and_console("We have played the playlist for: " + str(randomTime) + " seconds")
                        break
                    time.sleep(0.5)
                    try:
                        driver.find_element(By.XPATH, '//*[@name="header-play-button"]')
                    except:
                        time.sleep(0.5)
                if playlist_elapsed_time > randomTime:
                    break
            log_to_mongo_and_console("Finished")



















"""

    PREVIOUS WORKING CODE BELOW!!!

"""



# from appium import webdriver
# import time
# from appium.webdriver.common.touch_action import TouchAction
# from appium.options.ios import xcuitest
# from appium.webdriver.common.mobileby import MobileBy
# from appium.webdriver.common.appiumby import AppiumBy
# from appium.webdriver.common.touch_action import TouchAction
# from appium.webdriver.common.multi_action import MultiAction
# from appium.webdriver.webelement import WebElement
# from appium.webdriver.common.touch_action import TouchAction
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from random import randrange
# import random
# import sys
# import requests




# def crane(container):
#     print("Crane")
#     # try:
#     #     driver.terminate_app('com.spotify.client')
#     # except:
#     #     pass
#     for i in range(2):
#         try:
#             driver.execute_script("mobile: pressButton", {"name": "home"})
#             time.sleep(1.5)
#         except:
#             time.sleep(0.5)
#             print("Home button error")
#     while True:
#         try:
#             spotify = driver.find_element(By.XPATH, '//*[@label="Spotify"]')
#             action = TouchAction(driver)
#             action.long_press(spotify).release().perform()
#             driver.refresh
#             print("Long pressed on Spotify")
#             time.sleep(5)
#             driver.find_element(By.XPATH, '//*[contains(@label,"Container")]').click()
#             time.sleep(1)
#             break
#         except Exception as e:
#             print("1: " + str(e))
#     while True:
#         try:
#             driver.find_element(By.XPATH, '//*[@label="' + str(container) + '"]').click()
#             time.sleep(1.5)
#             break
#         except:
#             time.sleep(0.5)
#             print("Container not found")
#     rotateIP()
#     driver.activate_app("com.spotify.client")
#     return

# def rotateIP():
#     catchIssue = 0
#     print("Rotating IP...")
#     while True:
#         try:
#             driver.activate_app("com.apple.shortcuts")
#             break
#         except:
#             time.sleep(0.5)
#     while True:
#         try:
#             driver.find_element(By.XPATH, '//*[@name="IP"]').click()
#             time.sleep(2)
#             print("IP rotated!")
#             break
#         except:
#             time.sleep(0.5)
#     while True:
#         try:
#             driver.terminate_app("com.apple.shortcuts")
#             return
#         except:
#             time.sleep(0.5)

# desired_caps = {
#     "xcodeOrgId": "52AUC7UKFT",
#     "xcodeSigningId": "iPhone Developer",
#     "platformName": "iOS",
#     "automationName": "XCUITest",
#     "udid": sys.argv[1],
#     "deviceName": "iPhone",
#     "bundleId": "com.spotify.client",
#     "updatedWDABundleID": "shanavarspotify.shanavarspotify.WebDriverAgentRunner",
#     "showXcodeLog": True,
#     "newCommandTimeout": "1000",
#     "useNewWDA": True,
#     "wdaLocalPort":sys.argv[9],
#     "noReset": True
# }

# while True:
#     try:
#         driver = webdriver.Remote("http://localhost:1111/wd/hub", desired_caps)
#         print("Started")
#         break
#     except Exception as e:
#         print("Driver not executed; try restarting the Appium Server and make sure your device's JB is still running.")
#         print(str(e))
#         time.sleep(0.5)

# # Check if the bot is in the configured sleep schedule
# def is_in_sleep_schedule(start_time, end_time):
#     now = time.localtime()
#     current_time = time.strftime("%H:%M", now)
#     return start_time <= current_time <= end_time


# timeFrom = int(sys.argv[2])
# timeTo = int(sys.argv[3])
# cloneList = sys.argv[4].split(",")
# playlists = sys.argv[5].split(",")
# inputType = sys.argv[6]
# songTimeFrom = int(sys.argv[7])
# songTimeTo = int(sys.argv[8])
# wdaLocalPort = int(sys.argv[9])  #to help run two different devices for threading!
# sleep_schedule_start = sys.argv[10]  # Sleep schedule start 
# sleep_schedule_end = sys.argv[11]  # Sleep schedule end
# pause_chance = int(sys.argv[12])  # Chance to pause a song in percentage
# pause_min_duration = int(sys.argv[13])  # Minimum pause duration in seconds
# pause_max_duration = int(sys.argv[14])  # Maximum pause duration in seconds
# skip_after_seconds = int(sys.argv[15])  # Force skip after this many seconds
# print("Clones: " + str(cloneList))

# while True:
#     for clone in cloneList:
#         try:
#             crane(clone)
#         except Exception as e:
#             print("Crane error: " + str(e))
#         for playlist in playlists:
#             report = 0
#             while True:
#                 randomTime = random.randint(timeFrom, timeTo)
#                 #if reports more than 5 it terminates application here!
#                 if report == 5:
#                     while True:
#                         try:
#                             driver.terminate_app('com.spotify.client')
#                             time.sleep(2)
#                             break
#                         except:
#                             time.sleep(0.5)
#                             print("App not terminated")
#                     # while True:
#                     #     try:
#                     #         driver.activate_app("com.spotify.client")
#                     #         time.sleep(2)
#                     #         break
#                     #     except:
#                     #         time.sleep(0.5)
#                     #         print("App not activated")
#                 #if reports not five than it goes here!
#                 try:

#                     driver.find_element(By.XPATH, '//*[@name="tabbar-item-find"]').click()
#                     time.sleep(1.5)
#                     break
#                 except:
#                     time.sleep(0.5)
#                     print("Find button not found")
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="OK"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[contains(@name,"close")]').click()
#                     time.sleep(1.5)
#                 except:
#                     time.sleep(0.5)
#                     print("Find button not found")
#                 report += 1

#             tries = 0
#             while True:
#                 if tries == 5:
#                     try:
#                         with open("error.txt", "w") as f:
#                             f.write(str(driver.page_source))
#                             f.close()
#                             print("Error file created")
#                     except:
#                         print("Error file not created")
#                 tries += 1
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[@name="SearchHeaderFind.SearchBar"]').click()
#                     time.sleep(1.5)
#                 except:
#                     time.sleep(0.5)
#                     print("Search btn")
#                 try:
#                     driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').send_keys(str(playlist))
#                     time.sleep(2)
#                 except:
#                     time.sleep(0.5)
#                     print("Search Field not found")
#                     driver.refresh
#                 try:
#                     searchField = str(driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').text)
#                     print("Search field: " + str(searchField))
#                     if searchField == str(playlist):
#                         print("Search field filled")
#                         break
#                 except:
#                     time.sleep(0.5)
#                     print("Search field not filled")
#                 try:
#                     driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').clear()
#                     print("Search field cleared")
#                     time.sleep(1)
#                 except:
#                     time.sleep(0.5)
#                     print("Search Field not found")
#             while True:
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[@name="Search"]').click()
#                     print("Clicked on search")
#                     time.sleep(5)
#                     break
#                 except:
#                     time.sleep(0.5)
#                     print("Search button not found")
#             if inputType != "Links":
#                 while True:
#                     try:
#                         driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[@label="' + str(inputType) + '"]').click()
#                         print("Clicked on " + str(inputType))
#                         time.sleep(3)
#                         break
#                     except:
#                         time.sleep(0.5)
#                         print("Input type not found")
#                     try:
#                         driver.find_element(By.XPATH, '//*[@label="Music"]').click()
#                         time.sleep(1)
#                         print("Clicked on music")
#                     except:
#                         time.sleep(0.5)
#                         print("Music not found")
                
#                 #if inputtype is Albums!
#                 while True:
#                     if inputType == "Albums":
#                         playlist = playlist.replace(" -", ",")
#                     try:
#                         driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass


#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '(//*[contains(@label, "' + str(playlist) + '")])[1]').click()
#                         print("Clicked on media")
#                         time.sleep(3)
#                         break
#                     except:
#                         time.sleep(0.5)
#                         print("Media: " + str(playlist) + " not found")
#                     try:
#                         print("Scrolling a bit")
#                         action = TouchAction(driver)
#                         action.long_press(None, 170, 556).move_to(None, 170, 120).release().perform()
#                         time.sleep(1)
#                     except:
#                         print("Scrolling error")
#             start_time = time.time()
#             playlist_start_time = time.time()
#             songTime = random.randint(songTimeFrom, songTimeTo)
#             while True:
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 #Logic for pause and skip!
#                 if random.randint(1, 100) <= pause_chance:
#                     pause_duration = random.randint(pause_min_duration, pause_max_duration)
#                     print(f"Pausing playback for {pause_duration} seconds.")

#                     #Have to fix the Xpath to make this logic work perfectly!
#                     driver.execute_script("mobile: pressButton", {"name": "pause"})  # Simulate pause
#                     time.sleep(pause_duration)
#                     driver.execute_script("mobile: pressButton", {"name": "play"})  # Resume playback

#                 current_time = time.time()
#                 elapsed_time = current_time - start_time

#                 if elapsed_time > skip_after_seconds:
#                     print("Forcing skip due to timeout.")
#                     try:
#                         driver.find_element(By.XPATH, '//*[contains(@label,"Next")]').click()
#                         start_time = time.time()  # Reset start_time for the next song
#                         break
#                     except:
#                         print("Failed to skip.")
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
#                     time.sleep(1.5)
#                 except:
#                     pass
#                 try:
#                     driver.find_element(By.XPATH, '//*[@name="header-play-button"]').click()
#                     time.sleep(2)
#                     print("Playing playlist for: " + str(randomTime) + " seconds")
#                 except:
#                     time.sleep(0.5)
#                 try:
#                     driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
#                     print("Clicked on Now Playing")
#                     time.sleep(1.5)
#                 except:
#                     time.sleep(0.5)
#                     print("Now Playing not found")
#                 while True:
#                     try:
#                         driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="dismiss"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     try:
#                         driver.find_element(By.XPATH, '//*[translate(@label, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="close"]').click()
#                         time.sleep(1.5)
#                     except:
#                         pass
#                     current_time = time.time()
#                     playlist_elapsed_time = current_time - playlist_start_time
#                     elapsed_time = current_time - start_time
#                     print("Playing song for: " + str(songTime) + " seconds")
#                     print(str(clone), " playlist/album elapsed time: {:.2f} seconds".format(playlist_elapsed_time), end='\r')
#                     if elapsed_time > songTime:
#                         print("We have played the song for: " + str(songTime) + " seconds")
#                         try:
#                             driver.find_element(By.XPATH, '//*[contains(@label,"Next")]').click()
#                             print("Next song")
#                             songTime = random.randint(songTimeFrom, songTimeTo)
#                             print(f"Next song will play for {songTime} seconds")
#                             start_time = time.time()  # Reset start_time for the next song
#                             break
#                         except:
#                             time.sleep(0.5)
#                             print("Next song not found")
#                             try:
#                                 driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
#                                 print("Clicked on Now Playing")
#                                 time.sleep(1.5)
#                             except:
#                                 time.sleep(0.5)
#                                 print("Now Playing not found")
#                     if playlist_elapsed_time > randomTime:
#                         print("We have played the playlist for: " + str(randomTime) + " seconds")
#                         break
#                     time.sleep(0.5)
#                     try:
#                         driver.find_element(By.XPATH, '//*[@name="header-play-button"]')
#                     except:
#                         time.sleep(0.5)
#                 if playlist_elapsed_time > randomTime:
#                     break
#             print("Finished")
