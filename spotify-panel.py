import subprocess
import flask
import json
from flask import Flask, request, render_template, url_for, flash, jsonify
from appium.webdriver.appium_service import AppiumService
import os
import threading
import random
from pymongo import MongoClient
import datetime
import re
import sys
# from datetime import datetime 
from datetime import time as t
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["device_db"]  # Create or connect to 'device_db' database
except Exception as e:
    print(f"Error connecting to Mongodb:  {str(e)}")
    sys.exit(1)

device_status_collection = db["device_status"]
settings_collection = db["settings"]
logs_collection = db["device_logs"]

app = Flask(__name__, template_folder="")
app.secret_key = b"secretkey23hr397fh3tf234r5hx0"
directory = os.path.dirname(os.path.realpath(__file__))

#to check if the device is in sleep schedule!
def is_in_sleep_schedule(sleep_schedule):
    now = datetime.datetime.now().time()
    start_time = datetime.datetime.strptime(sleep_schedule["start"], "%H:%M").time()
    end_time = datetime.datetime.strptime(sleep_schedule["end"], "%H:%M").time()

    # Handle overnight sleep schedules (e.g., 01:00 to 07:00)
    if start_time < end_time:
        return start_time <= now <= end_time
    else:
        return now >= start_time or now <= end_time

lock = threading.Lock()
def update_device_status(device_id, new_status, pid=0):
    with lock:
        device_status_collection.update_one(
            {"device": device_id},
            {
                "$set": {
                    "status": new_status,
                    "pid": pid,
                    "last_updated": datetime.datetime.now(datetime.timezone.utc),
                }
            },
        )

def log_event(device_id, event_type, message):
    """
    Logs an event to the 'device_logs' collection.
    :param device_id: ID of the device associated with the log
    :param event_type: Type of event (e.g., "INFO", "ERROR", "WARNING")
    :param message: Description of the event
    """
    log_entry = {
        "device": device_id,
        "event_type": event_type,
        "message": message,
        "timestamp": datetime.datetime.now(datetime.timezone.utc)
    }
    logs_collection.insert_one(log_entry)

def fetch_device_status():
    devices = list(device_status_collection.find({}, {"_id": 0}))
    return devices

class NewThreadedTask(threading.Thread):
    def __init__(
        self, 
        device, 
        timefrom, 
        timeto, 
        clones, 
        ip, 
        inputType, 
        songtimefrom, 
        songtimeto, 
        wda_port, 
        sleep_schedule,
        skip_after_seconds, 
        pause_chance, 
        pause_min_duration, 
        pause_max_duration
    ):
        super(NewThreadedTask, self).__init__()
        # super().__init__()
        self.device = device
        self.timefrom = timefrom
        self.timeto = timeto
        self.clones = clones
        self.ip = ip
        self.inputType = inputType
        self.songtimefrom = songtimefrom
        self.songtimeto = songtimeto
        self.wda_port = wda_port
        self.sleep_schedule = sleep_schedule
        self.skip_after_seconds = skip_after_seconds
        self.pause_chance = pause_chance
        self.pause_min_duration = pause_min_duration
        self.pause_max_duration = pause_max_duration
        self.pid = None

    def run(self):
        try:
            # Check sleep schedule
            # if is_in_sleep_schedule(self.sleep_schedule):
            #     log_event(self.device, "INFO", "Task skipped due to sleep schedule.")
            #     update_device_status(self.device, "Sleeping", 0)
            #     return

            #Code sinnpet from cmd() function to check similarity!!
            # task = NewThreadedTask(
            #     device,
            #     timefrom,
            #     timeto,
            #     clones,
            #     ip,
            #     inputType,
            #     songtimefrom,
            #     songtimeto,
            #     wda_port,
            #     sleep_schedule,
            #     skip_after_seconds,
            #     pause_chance,
            #     pause_min_duration,
            #     pause_max_duration,
            # )

            # Start the task as a subprocess
            try:
                # print(f"Starting subprocess.....")
                # p = subprocess.Popen(
                #     [
                #         "python3",
                #         "sp.py",
                #         self.device,
                #         self.timefrom,
                #         self.timeto,
                #         self.clones,
                #         self.ip,
                #         str(self.inputType),
                #         self.songtimefrom,
                #         self.songtimeto,
                #         str(self.wda_port),
                #         # str(self.sleep_schedule),
                #         self.sleep_schedule["start"],
                #         self.sleep_schedule["end"],
                #         str(self.skip_after_seconds),
                #         str(self.pause_chance),
                #         str(self.pause_min_duration),
                #         str(self.pause_max_duration),

                #     ]
                # )
                args = [
                        "python3",
                        "sp.py",
                        self.device,
                        self.timefrom,
                        self.timeto,
                        self.clones,
                        self.ip,
                        str(self.inputType),
                        self.songtimefrom,
                        self.songtimeto,
                        str(self.wda_port),
                        # str(self.sleep_schedule),
                        self.sleep_schedule["start"],
                        self.sleep_schedule["end"],
                        str(self.skip_after_seconds),
                        str(self.pause_chance),
                        str(self.pause_min_duration),
                        str(self.pause_max_duration),

                    ]
                
                print(f"Starting subprocess with arguments: {args}")
                p = subprocess.Popen(args , stdout = subprocess.PIPE , stderr = subprocess.PIPE)
                stdout, stderr = p.communicate()
                update_device_status(self.device, "running", self.pid)
                log_event(self.device, "INFO" , f"Task started with PID {self.pid}.")
                print(f"Subprocess stdout: {stdout.decode()}")
                print(f"Subprocess stderr: {stderr.decode()}")


                self.pid = p.pid
                print("passed8")
                update_device_status(self.device, "running", self.pid)
            except Exception as e:
                print(f"Error is : {str(e)}")

            # Pause and skip logic
            total_elapsed_time = 0
            while p.poll() is None:
                if random.randint(0, 100) < self.pause_chance:
                    pause_duration = random.randint(self.pause_min_duration, self.pause_max_duration)
                    log_event(self.device, "INFO", f"Pausing for {pause_duration} seconds.")
                    update_device_status(self.device, "Paused", self.pid)
                    t.sleep(pause_duration)
                    update_device_status(self.device, "View botting", self.pid)

                total_elapsed_time += 1
                if total_elapsed_time >= self.skip_after_seconds:
                    log_event(self.device, "INFO", "Skipping song due to elapsed time.")
                    p.terminate()
                    break

                t.sleep(1)

        except Exception as e:
            log_event(self.device, "ERROR", f"Error in thread run: {str(e)}")
            update_device_status(self.device, "Error", 0)


try:
    device_status_collection.delete_many({})
    status = fetch_device_status()

    # code for testing on mock devices!
    # device_clone_list = subprocess.check_output(["xcrun", "simctl" ,"list"], text=True)
    # booted_devices = [
    #     line for line in device_clone_list.splitlines() if '(Booted)' in line
    # ]

    devicelist = subprocess.check_output(["ios-deploy", "-c"])
    devicelist = str(devicelist).replace('b"', "").split("[....]")

    # device_clone_list = subprocess.check_output(["xcrun", "simctl" ,"list", "|" ,"egrep" ,"'(Booted)'"])
    # device_clone_list = str(device_clone_list).replace('b"', "").split("[....]")
    print(devicelist)

    # for line in booted_devices:
    #     try:
    #         # Strip whitespace and confirm the line contains "(Booted)"
    #         line = line.strip()
    #         if "(Booted)" in line and len(status) < 12:
    #             # Extract the device ID using a regular expression
    #             match = re.search(r"\(([\w-]+)\)", line)
    #             if match:
    #                 device_id = match.group(1)  # Extract the content inside parentheses

    #                 # Prepare the device entry
    #                 device_entry = {
    #                     "device": device_id,
    #                     "status": "ready",
    #                     "pid": 0,
    #                     "last_updated": datetime.datetime.now(datetime.timezone.utc),
    #                 }
    #                 status.append(device_entry)

    #                 # Insert or update device status in MongoDB
    #                 device_status_collection.update_one(
    #                     {"device": device_id}, {"$set": device_entry}, upsert=True
    #                 )

    #                 # Log the event
    #                 log_event(device_id, "INFO", "Device detected and status updated!")
    #     except Exception as e:
    #         # Log unexpected errors for debugging
    #         log_event("Unknown Device", "ERROR", f"Error processing line: {line}, Error: {str(e)}")

    # Print the final device status
    # print("Device Status:", status)

    for line in devicelist:
        try:
            if "Found" in line and len(status) < 12:
                device_id = line.split("Found")[1].split(" ")[1]
                device_entry = {
                    "device": device_id,
                    "status": "ready",
                    "pid": 0,
                    "last_updated": datetime.datetime.now(datetime.timezone.utc),
                }
                status.append(device_entry)

                # Insert or update device status in MongoDB
                device_status_collection.update_one(
                    {"device": device_id}, {"$set": device_entry}, upsert=True
                )
                log_event(device_id, "INFO", "Device detected and status updated!")
        except Exception as e:
            log_event("Unknown Device", "ERROR", f"Error processing line: {line}, Error: {str(e)}")
    print("Device Status:", status)

except Exception as e:
    log_event(device_id=None, event_type="ERROR", message=f"Device detection error: {str(e)}")

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Fetch logs from the database.
    """
    device_id = request.args.get("device")
    query = {"device": device_id} if device_id else {}
    logs = list(logs_collection.find(query, {"_id": 0}))
    return jsonify(logs)

@app.route('/devices', methods=['GET'])
def get_devices():
    """
    Fetch a list of all devices with logs.
    """
    devices = device_status_collection.distinct("device")  # Fetch unique device IDs from the logs
    return jsonify(devices)
@app.route("/settings-form", methods=["GET"])
def settings_form():
    """
    Serve the settings form, pre-filled with existing values.
    """
    existing_settings = settings_collection.find_one({}, {"_id": 0})
    return render_template("settings.html", settings=existing_settings or {})
# Route to fetch settings from MongoDB!!!
# @app.route('/get-settings', methods=['GET'])
# def get_settings():
#     """
#     Fetch settings from the database.
#     """
#     settings = settings_collection.find_one({}, {"_id": 0})
#     if not settings:
#         # Provide default values if no settings exist
#         settings = {
#             "ip": "",
#             "timefrom": "",
#             "timeto": "",
#             "clones":"",
#             "songtimefrom": "",
#             "songtimeto": "",
#             "inputType": "",
#             "skip_after_seconds": 0,
#             "pause_chance": 0,
#             "pause_min_duration": 0,
#             "pause_max_duration": 0,
#             "sleep_schedule": {"start": "", "end": ""},
            
#         }
#     return jsonify(settings)
# # Route to save settings to MongoDB!!!
# @app.route("/save-settings", methods=["POST"])
# def save_settings():
#     """
#     Save settings to the database.
#     """
#     settings = request.json
#     settings["last_updated"] = datetime.datetime.now(datetime.timezone.utc)
#     if "skip_after_seconds" in settings:
#         settings["skip_after_seconds"] = max(0, int(settings["skip_after_seconds"]))

#     if "pause_chance" in settings:
#         settings["pause_chance"] = max(0, min(100, int(settings["pause_chance"])))  # Limit to 0-100%

#     if "pause_min_duration" in settings and "pause_max_duration" in settings:
#         settings["pause_min_duration"] = max(0, int(settings["pause_min_duration"]))
#         settings["pause_max_duration"] = max(settings["pause_min_duration"], int(settings["pause_max_duration"]))

#     # if "pause_frequency" in settings:
#     #     settings["pause_frequency"] = max(0, int(settings["pause_frequency"]))

#     if "sleep_schedule" in settings:
#         sleep_start = settings["sleep_schedule"].get("start")
#         sleep_end = settings["sleep_schedule"].get("end")
#         settings["sleep_schedule"] = {"start": sleep_start, "end": sleep_end}
#     settings_collection.update_one({}, {"$set": settings}, upsert=True)
#     return jsonify({"message": "Settings saved successfully!"})

# Route to fetch settings from MongoDB!!!
# @app.route('/get-settings', methods=['GET'])
# def get_settings():
#     """
#     Fetch settings from the database.
#     """
#     settings = settings_collection.find_one({}, {"_id": 0})
#     if not settings:
#         # Provide default values if no settings exist
#         settings = {
#             "ip": "",
#             "timefrom": "",
#             "timeto": "",
#             "clones":"",
#             "songtimefrom": "",
#             "songtimeto": "",
#             "inputType": "",
#             "skip_after_seconds": 0,
#             "pause_chance": 0,
#             "pause_min_duration": 0,
#             "pause_max_duration": 0,
#             "sleep_schedule": {"start": "", "end": ""},
            
#         }
#     return jsonify(settings)

@app.route('/get-settings', methods=['GET'])
def get_settings():
    """
    Fetch settings from the database or return defaults if none exist.
    """
    device_id = request.args.get("device")
    if not device_id:
        return jsonify({"error":"Device ID is required."}) , 400
    try:
        print("Fetching settings from MongoDB....")
        settings = settings_collection.find_one({"device_id":device_id},{"_id":0})
        if not settings:
            # Provide default values if no settings exist
            print("No settings found in the database!")
            settings = {
                "device_id":device_id,
                "ip": "",
                "timefrom": "",
                "timeto": "",
                "clones": "",
                "songtimefrom": "",
                "songtimeto": "",
                "inputType": "",
                "skip_after_seconds": 0,
                "pause_chance": 0,
                "pause_min_duration": 0,
                "pause_max_duration": 0,
                "sleep_schedule": {"start": "", "end": ""},
            }
        print("Settings fetched successfully:" , settings)
        return jsonify(settings)
    except Exception as e:
        print(f"Erro fetching settings: {str(e)}")
        return jsonify({"error": "Failed to fetch settings.", "details": str(e)}), 500


@app.route("/save-settings", methods=["POST"])
def save_settings():
    """
    Save settings to the database.
    """
    try:
        settings = request.json
        # device_id =settings.get("device_id")
        # if not device_id:
        #     return jsonify({"error" : "Device ID is required."}) , 400
        # print("Received settings to save: " , settings)

        # Ensure required fields exist
        # if not isinstance(settings, dict):
        #     return jsonify({"error": "Invalid input format. Expected JSON object."}), 400

        # # Validate and sanitize fields
        # settings["last_updated"] = datetime.datetime.now(datetime.timezone.utc)

        # if "skip_after_seconds" in settings:
        #     settings["skip_after_seconds"] = max(0, int(settings["skip_after_seconds"]))

        # if "pause_chance" in settings:
        #     settings["pause_chance"] = max(0, min(100, int(settings["pause_chance"])))  # Limit to 0-100%

        # if "pause_min_duration" in settings and "pause_max_duration" in settings:
        #     settings["pause_min_duration"] = max(0, int(settings["pause_min_duration"]))
        #     settings["pause_max_duration"] = max(settings["pause_min_duration"], int(settings["pause_max_duration"]))

        # if "sleep_schedule" in settings:
        #     sleep_schedule = settings["sleep_schedule"]
        #     sleep_start = sleep_schedule.get("start", "")
        #     sleep_end = sleep_schedule.get("end", "")

        #     # Ensure valid time format (HH:MM) if provided
        #     if sleep_start and not validate_time_format(sleep_start):
        #         return jsonify({"error": f"Invalid sleep start time format: {sleep_start}"}), 400
        #     if sleep_end and not validate_time_format(sleep_end):
        #         return jsonify({"error": f"Invalid sleep end time format: {sleep_end}"}), 400

        #     settings["sleep_schedule"] = {"start": sleep_start, "end": sleep_end}

        # Save to database
        # settings_collection.update_one({}, {"$set": settings}, upsert=True)
        settings["last_updated"] = datetime.datetime.now(datetime.timezone.utc)
        settings_collection.update_one(
            {"device_id": device_id},
            {"$set": settings},
            upsert = True
        )

        print("Settings saved successfully!")
        return jsonify({"message": "Settings saved successfully!"})
    except ValueError as e:
        return jsonify({"error": "Invalid data format.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to save settings.", "details": str(e)}), 500


def validate_time_format(time_str):
    """
    Validate if a given string matches the HH:MM time format.
    """
    try:
        datetime.datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
@app.route("/panel")
def panel():
    # device_clone_list = subprocess.check_output(["xcrun", "simctl" ,"list"], text=True)
    # booted_devices = [
    #     line for line in device_clone_list.splitlines() if '(Booted)' in line
    # ]
    # # device_clone_list = str(device_clone_list).replace('b"', "").split("[....]")
    # print(booted_devices)
    # settings = settings_collection.find_one({}, {"_id": 0})
    # if not settings:
    #     flash("Settings are missing. Please configure settings first.")
    #     return flask.redirect(url_for("settings_form"))
    devices = fetch_device_status()  # Get devices from MongoDB
    settings = settings_collection.find_one({}, {"_id": 0})

    if not devices:
        flash("No devices detected.")
        return flask.redirect(url_for("settings_form"))
    devicelist = subprocess.check_output(["ios-deploy", "-c"])
    devicelist = str(devicelist).replace('b"', "").split("[....]")
    status = fetch_device_status()
    # for line in devicelist:
    #     try:
    #         # Strip whitespace and confirm the line contains "(Booted)"
    #         line = line.strip()
    #         if "(Booted)" in line and len(status) < 12:
    #             # Extract the device ID using a regular expression
    #             match = re.search(r"\(([\w-]+)\)", line)
    #             if match:
    #                 device_id = match.group(1)  # Extract the content inside parentheses

    #                 # Prepare the device entry
    #                 device_entry = {
    #                     "device": device_id,
    #                     "status": "ready",
    #                     "pid": 0,
    #                     "last_updated": datetime.datetime.now(datetime.timezone.utc),
    #                 }
    #                 status.append(device_entry)

    #                 # Insert or update device status in MongoDB
    #                 device_status_collection.update_one(
    #                     {"device": device_id}, {"$set": device_entry}, upsert=True
    #                 )

    #                 # Log the event
    #                 log_event(device_id, "INFO", "Device detected and status updated!")
    #     except Exception as e:
    #         # Log unexpected errors for debugging
    #         log_event("Unknown Device", "ERROR", f"Error processing line: {line}, Error: {str(e)}")

    for line in devicelist:
        try:
            if "Found" in line and len(status) < 12:
                device_id = line.split("Found")[1].split(" ")[1]
                device_entry = {
                    "device": device_id,
                    "status": "ready",
                    "pid": 0,
                    "last_updated": datetime.datetime.now(datetime.timezone.utc),
                }
                status.append(device_entry)

                # Insert or update device status in MongoDB
                device_status_collection.update_one(
                    {"device": device_id}, {"$set": device_entry}, upsert=True
                )
                log_event(device_id, "INFO", "Device detected and status updated!")
        except Exception as e:
            log_event("Unknown Device", "ERROR", f"Error processing line: {line}, Error: {str(e)}")
    print("Device Status:", status)

    status = fetch_device_status()

    form = "<input type='submit' value='Start'><input name='stop' type='submit' value='Stop'><br>Container list:<br><textarea id='clones' name='clones' rows='3' cols='50' ></textarea><br>Playlist/Album/Links:<br><textarea id='ip' name='ip' rows='3' cols='50' ></textarea><br>Type:<select name='inputType' id='inputType'><option name='Albums' id='Albums' value='Albums'>Albums</option><option name='Playlists' id='Playlists' value='Playlists'>Playlists</option><option name='Links' id='Links' value='Links'>Links</option></select><br>Song listen time from:<br><textarea id='songtimefrom' name='songtimefrom' rows='1' cols='5' ></textarea><br>Song listen time to:<br><textarea id='songtimeto' name='songtimeto' rows='1' cols='5' ></textarea><br>Total listen time from:<br><textarea id='timefrom' name='timefrom' rows='1' cols='5' ></textarea><br>Total listen time to:<br><textarea id='timeto' name='timeto' rows='1' cols='5' ></textarea>"
    table = "<table><tr><th>Device</th><th>Status</th></tr>"
    # devicedroplist = (
    #     "<label for='device'>Device:</label><select name='device' id='device'>"
    # )
    devicedroplist = (
    "<label for='device'>Device:</label><select name='device' id='device' onchange='handleDeviceChange(this.value)'>"
)


    for x in status:
        table += f"<tr><td>{x['device']}</td><td>{x['status']}</td><td>"
        table += (
            f"<form action='/stop' method='post' style='display:inline;'>"
            f"<input type='hidden' name='device' value='{x['device']}'>"
            f"<input type='submit' value='Stop'></form>"
        )
        table += "</td></tr>"

        devicedroplist += (
            f"<option name='{x['device']}' value='{x['device']}'>please choose devuce</option><option name='{x['device']}' value='{x['device']}'>{x['device']}</option>"
        )

    device_links = [
        f"<tr><td>{device['device']}</td>"
        f"<td>{device['status']}</td>"
        f"<td><a href='/settings-form?device_id={device['device']}'>Edit Settings</a></td></tr>"  #?device_id={device['device']}
        for device in status
    ]

    table_device_settings = "<table border='1'><tr><th>Device ID</th><th>Status</th><th>Actions</th></tr>" + "".join(device_links) + "</table>"

    table += "</table>"
    devicedroplist += "</select>"

    return (
        f"<form id= 'startForm' action='/start' method='get'>"
        f"{table}{devicedroplist}{form}</form>"
        f"""<html><head><title>Device Panel</title></head><body> <h1>Device Management Panel</h1>{table_device_settings}</body></html>"""
        + render_template("spot.html" , devices = devices , settings =settings)
    )
    # for x in status:
    #     table += "<tr><td>" + x["device"] + "</td><td>" + x["status"] + "</td></tr>"
    #     devicedroplist += (
    #             "<option name='"
    #             + x["device"]
    #             + "'value='"
    #             + x["device"]
    #             + "' onchange='change'>"
    #             + x["device"]
    #             + "</option>"
    #     )
    # table += "</table>"
    # devicedroplist += "</select>"
    # return (
    #         "<form action='/start' method='get'>"
    #         + table
    #         + devicedroplist
    #         + form
    #         + "</form>"
    #         # + "<h2>Fetch Logs</h2>"
    #         # + '<label for="deviceId">Device ID:</label>'
    #         # + '<input type="text" id="deviceId" placeholder="Enter device ID" />'
    #         # + '<button onclick="fetchLogs(document.getElementById('deviceId').value)">View Logs</button>'
    #         + render_template("spot.html")
    # )


@app.route("/stop", methods=["POST"])
def stop_task():
    device = request.form.get("device")
    if not device:
        flash("Device ID is missing.")
        return flask.redirect(url_for("panel"))

    device_entry = device_status_collection.find_one({"device": device})
    if not device_entry or device_entry["status"] != "running":
        flash(f"No running task found for device {device}.")
        return flask.redirect(url_for("panel"))

    pid = device_entry["pid"]
    try:
        os.kill(pid, 9)  # Terminate the subprocess
        update_device_status(device, "ready", 0)
        log_event(device, "INFO", f"Task with PID {pid} stopped successfully.")
        flash(f"Task on device {device} stopped successfully.")
    except Exception as e:
        log_event(device, "ERROR", f"Failed to stop task: {str(e)}")
        flash(f"Failed to stop task on device {device}. Error: {str(e)}")
    return flask.redirect(url_for("panel"))


@app.route("/complete")
def complete():
    device = request.args.get("device")
    for x in status:
        if x["device"] == device and x["status"] != "ready":
            x["status"] = "ready"
            update_device_status(device, "ready", 0)
    return x["status"]
@app.route("/start")
def cmd():
    # print("Request args: " , request.args)
    #Implementation of sleeping schedule!!
    """
            Start Time : 01:00 for 1:00 am
                         13:30 for 1:30 pm

            End Time :  07:00 for 7:00 am
                        23:00 for 11:00 pm

    # """
    device = request.args.get("device")
    print("device",device)
    settings = settings_collection.find_one({"device_id" : device}, {"_id": 0})
    if not settings:
        flash(f"No settings found for device {device}. Please configure settings first.")
        return flask.redirect(url_for("settings_form"))

    sleep_schedule = settings.get("sleep_schedule", {"start": "00:00", "end": "00:00"})
    if is_in_sleep_schedule(sleep_schedule):
        flash("Bot is sleeping based on the configured sleep schedule.")
        print("Bot is sleeping due to sleep schedule!")
        return flask.redirect(url_for("panel"))
    stop = request.args.get("stop","").lower()
    
    clones = request.args.get("clones")
    timefrom = request.args.get("timefrom")
    timeto = request.args.get("timeto")
    ip = request.args.get("ip")
    inputType = request.args.get("inputType", "Albums")
    songtimefrom = request.args.get("songtimefrom")
    songtimeto = request.args.get("songtimeto")

    skip_after_seconds = settings.get("skip_after_seconds", 0)
    pause_chance = settings.get("pause_chance", 0)
    pause_min_duration = settings.get("pause_min_duration", 0)
    pause_max_duration = settings.get("pause_max_duration", 0)

    base_port = 8100
    device_index = [x["device"] for x in fetch_device_status()].index(device)
    wda_port = base_port + device_index

    print("Extracted parameters: " , {
            "device":device , 
            "clones":clones,
            "ip":ip,
            "inputType": inputType,
            "timefrom": timefrom ,
            "timeto":timeto,
            "songtimefrom":songtimefrom,
            "songtimeto": songtimeto

    })

    if not device:
        flash("Device ID is missing. Please select a valid device.")
        return flask.redirect(url_for("panel"))
    try:
        clones = clones.replace("\r\n", ",") if clones else ""
        ip = ip.replace("\r\n", ",") if ip else ""
    except Exception as e:
        print("Variable formatting error:", str(e))
    # if clones:
    #     clones = clones.replace("\r\n", ",")
    # if ip:
    #     ip = ip.replace("\r\n" , ",")

    device_entry = device_status_collection.find_one({"device": device})
    print("passed2")


    if device_entry and device_entry.get("status", "ready"):
        current_status = device_entry.get("status", "ready")
        pid = device_entry.get("pid",0)


        print("passed3")

        # Only proceed if the device is "ready" and stop command is not triggered
        if current_status == "ready" and stop == "":
            # Start the task in a new thread
            print("passed4")

            task = NewThreadedTask(
                device,
                timefrom,
                timeto,
                clones,
                ip,
                inputType,
                songtimefrom,
                songtimeto,
                wda_port,
                sleep_schedule,
                skip_after_seconds,
                pause_chance,
                pause_min_duration,
                pause_max_duration,
            )
            print("passed5")
            task.start()  # This starts the thread and calls `run` method in NewThreadedTask
            log_event(device, "INFO", "Task started successfully!")
            flash(f"Task started on device {device} with WDA port {wda_port}")
            return flask.redirect(url_for("panel"))


        # elif stop == "Stop":
        #     # If stop is called, terminate the device's process and reset status
        #     try:
        #         if pid:
        #             os.kill(device_entry["pid"], 9)
                    
        #             log_event(device, "INFO", "Task stopped successfully!")
        #             update_device_status(
        #                 device, "ready", 0
        #             )  # Reset the device status in MongoDB
        #             flash(f"Task stopped on device {device}")
        #     except Exception as e:
        #         print("Error stopping task:", str(e))
        #         log_event(device, "INFO", f"Error stopping task: {str(e)}")
        #     return flask.redirect(url_for("panel"))

        # else:
        #     # If the device is already running a task
        #     flash(f"Device {device} is already running a task!")
        #     return flask.redirect(url_for("panel"))
    else:
        flash("Device not found in database!")
        return flask.redirect(url_for("panel"))


app.run(threaded=True, host="0.0.0.0", port=1200, debug=True)
