from appium import webdriver
import time
from appium.webdriver.common.touch_action import TouchAction
from appium.options.ios import xcuitest
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.webelement import WebElement
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randrange
import random
import sys
import requests

def crane(container):
    print("Crane")
    try:
        driver.terminate_app('com.spotify.client')
    except:
        pass
    for i in range(2):
        try:
            driver.execute_script("mobile: pressButton", {"name": "home"})
            time.sleep(1.5)
        except:
            time.sleep(0.5)
            print("Home button error")
    while True:
        try:
            instagram = driver.find_element(By.XPATH, '//*[@label="Spotify"]')
            action = TouchAction(driver)
            action.long_press(instagram).release().perform()
            driver.refresh
            print("Long pressed on Spotify")
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[contains(@label,"Container")]').click()
            time.sleep(1)
            break
        except Exception as e:
            print("1: " + str(e))
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@label="' + str(container) + '"]').click()
            time.sleep(1.5)
            break
        except:
            time.sleep(0.5)
            print("Container not found")
    rotateIP()
    driver.activate_app("com.spotify.client")
    return

def rotateIP():
    catchIssue = 0
    print("Rotating IP...")
    while True:
        try:
            driver.activate_app("com.apple.shortcuts")
            break
        except:
            time.sleep(0.5)
    while True:
        try:
            driver.find_element(By.XPATH, '//*[@name="IP"]').click()
            time.sleep(2)
            print("IP rotated!")
            break
        except:
            time.sleep(0.5)
    while True:
        try:
            driver.terminate_app("com.apple.shortcuts")
            return
        except:
            time.sleep(0.5)

desired_caps = {
    "xcodeOrgId": "H5V48Z48DY",
    "xcodeSigningId": "iPhone Developer",
    "platformName": "iOS",
    "automationName": "XCUITest",
    "udid": sys.argv[1],
    "deviceName": "iPhone",
    "bundleId": "com.spotify.client",
    "updatedWDABundleID": "BotiPhone.BotiPhone.WebDriverAgentRunner",
    "showXcodeLog": True,
    "newCommandTimeout": "1000",
    "useNewWDA": True,
    "noReset": True
}

while True:
    try:
        driver = webdriver.Remote("http://localhost:1111/wd/hub", desired_caps)
        print("Started")
        break
    except Exception as e:
        print("Driver not executed; try restarting the Appium Server and make sure your device's JB is still running.")
        print(str(e))
        time.sleep(0.5)

timeFrom = int(sys.argv[2])
timeTo = int(sys.argv[3])
cloneList = sys.argv[4].split(",")
playlists = sys.argv[5].split(",")
inputType = sys.argv[6]
songTimeFrom = int(sys.argv[7])
songTimeTo = int(sys.argv[8])
print("Clones: " + str(cloneList))

while True:
    for clone in cloneList:
        try:
            crane(clone)
        except Exception as e:
            print("Crane error: " + str(e))
        for playlist in playlists:
            report = 0
            while True:
                randomTime = random.randint(timeFrom, timeTo)
                if report == 5:
                    while True:
                        try:
                            driver.terminate_app('com.spotify.client')
                            time.sleep(2)
                            break
                        except:
                            time.sleep(0.5)
                            print("App not terminated")
                    while True:
                        try:
                            driver.activate_app("com.spotify.client")
                            time.sleep(2)
                            break
                        except:
                            time.sleep(0.5)
                            print("App not activated")
                try:
                    driver.find_element(By.XPATH, '//*[@name="tabbar-item-find"]').click()
                    time.sleep(1.5)
                    break
                except:
                    time.sleep(0.5)
                    print("Find button not found")
                try:
                    driver.find_element(By.XPATH, '//*[@label="OK"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[contains(@name,"close")]').click()
                    time.sleep(1.5)
                except:
                    time.sleep(0.5)
                    print("Find button not found")
                report += 1

            tries = 0
            while True:
                if tries == 5:
                    try:
                        with open("error.txt", "w") as f:
                            f.write(str(driver.page_source))
                            f.close()
                            print("Error file created")
                    except:
                        print("Error file not created")
                tries += 1
                try:
                    driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@name="SearchHeaderFind.SearchBar"]').click()
                    time.sleep(1.5)
                except:
                    time.sleep(0.5)
                    print("Search btn")
                try:
                    driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').send_keys(str(playlist))
                    time.sleep(2)
                except:
                    time.sleep(0.5)
                    print("Search Field not found")
                    driver.refresh
                try:
                    searchField = str(driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').text)
                    print("Search field: " + str(searchField))
                    if searchField == str(playlist):
                        print("Search field filled")
                        break
                except:
                    time.sleep(0.5)
                    print("Search field not filled")
                try:
                    driver.find_element(By.XPATH, '//XCUIElementTypeSearchField').clear()
                    print("Search field cleared")
                    time.sleep(1)
                except:
                    time.sleep(0.5)
                    print("Search Field not found")
            while True:
                try:
                    driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@name="Search"]').click()
                    print("Clicked on search")
                    time.sleep(5)
                    break
                except:
                    time.sleep(0.5)
                    print("Search button not found")
            if inputType != "Links":
                while True:
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="' + str(inputType) + '"]').click()
                        print("Clicked on " + str(inputType))
                        time.sleep(3)
                        break
                    except:
                        time.sleep(0.5)
                        print("Input type not found")
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Music"]').click()
                        time.sleep(1)
                        print("Clicked on music")
                    except:
                        time.sleep(0.5)
                        print("Music not found")
                while True:
                    if inputType == "Albums":
                        playlist = playlist.replace(" -", ",")
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '(//*[contains(@label, "' + str(playlist) + '")])[1]').click()
                        print("Clicked on media")
                        time.sleep(3)
                        break
                    except:
                        time.sleep(0.5)
                        print("Media: " + str(playlist) + " not found")
                    try:
                        print("Scrolling a bit")
                        action = TouchAction(driver)
                        action.long_press(None, 170, 556).move_to(None, 170, 120).release().perform()
                        time.sleep(1)
                    except:
                        print("Scrolling error")
            start_time = time.time()
            playlist_start_time = time.time()
            songTime = random.randint(songTimeFrom, songTimeTo)
            while True:
                try:
                    driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                    time.sleep(1.5)
                except:
                    pass
                try:
                    driver.find_element(By.XPATH, '//*[@name="header-play-button"]').click()
                    time.sleep(2)
                    print("Playing playlist for: " + str(randomTime) + " seconds")
                except:
                    time.sleep(0.5)
                try:
                    driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
                    print("Clicked on Now Playing")
                    time.sleep(1.5)
                except:
                    time.sleep(0.5)
                    print("Now Playing not found")
                while True:
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Not Now"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="Dismiss"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    try:
                        driver.find_element(By.XPATH, '//*[@label="DISMISS"]').click()
                        time.sleep(1.5)
                    except:
                        pass
                    current_time = time.time()
                    playlist_elapsed_time = current_time - playlist_start_time
                    elapsed_time = current_time - start_time
                    print("Playing song for: " + str(songTime) + " seconds")
                    print(str(clone), " playlist/album elapsed time: {:.2f} seconds".format(playlist_elapsed_time), end='\r')
                    if elapsed_time > songTime:
                        print("We have played the song for: " + str(songTime) + " seconds")
                        try:
                            driver.find_element(By.XPATH, '//*[contains(@label,"Next")]').click()
                            print("Next song")
                            songTime = random.randint(songTimeFrom, songTimeTo)
                            print(f"Next song will play for {songTime} seconds")
                            start_time = time.time()  # Reset start_time for the next song
                            break
                        except:
                            time.sleep(0.5)
                            print("Next song not found")
                            try:
                                driver.find_element(By.XPATH, '(//*[contains(@name,"NowPlaying")])[1]').click()
                                print("Clicked on Now Playing")
                                time.sleep(1.5)
                            except:
                                time.sleep(0.5)
                                print("Now Playing not found")
                    if playlist_elapsed_time > randomTime:
                        print("We have played the playlist for: " + str(randomTime) + " seconds")
                        break
                    time.sleep(0.5)
                    try:
                        driver.find_element(By.XPATH, '//*[@name="header-play-button"]')
                    except:
                        time.sleep(0.5)
                if playlist_elapsed_time > randomTime:
                    break
            print("Finished")