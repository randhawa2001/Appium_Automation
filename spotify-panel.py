import subprocess
import flask
import json
from flask import Flask, request, render_template, url_for, flash
from appium.webdriver.appium_service import AppiumService
import os
import threading
import random
app = Flask(__name__, template_folder='')
app.secret_key = b'secretkey23hr397fh3tf234r5hx0'
directory = os.path.dirname(os.path.realpath(__file__))
class NewThreadedTask(threading.Thread):
     def __init__(self):
         super(NewThreadedTask, self).__init__()
try:
    status=[]
    devicelist=subprocess.check_output(['ios-deploy', '-c'])
    devicelist=str(devicelist).replace('b"', '')
    devicelist=devicelist.split("[....]")
    for line in devicelist:
        if line.__contains__(' Found'):
            line=line.split('Found')[1]
            line=line.split(" ")[1]
            status.append({'device':line,'status':'ready','pid':0})
    print(status)
except Exception as e:
    print(str(e))

@app.route('/panel')
def panel():
    form = "<input type='submit' value='Start'><input name='stop' type='submit' value='Stop'><br>Container list:<br><textarea id='clones' name='clones' rows='3' cols='50' onkeyup='saveValue(this);'></textarea><br>Playlist/Album/Links:<br><textarea id='ip' name='ip' rows='3' cols='50' onkeyup='saveValue(this);'></textarea><br>Type:<select name='inputType' id='inputType'><option name='Albums' id='Albums' value='Albums'>Albums</option><option name='Playlists' id='Playlists' value='Playlists'>Playlists</option><option name='Links' id='Links' value='Links'>Links</option></select><br>Song listen time from:<br><textarea id='songtimefrom' name='songtimefrom' rows='1' cols='5' onkeyup='saveValue(this);'></textarea><br>Song listen time to:<br><textarea id='songtimeto' name='songtimeto' rows='1' cols='5' onkeyup='saveValue(this);'></textarea><br>Total listen time from:<br><textarea id='timefrom' name='timefrom' rows='1' cols='5' onkeyup='saveValue(this);'></textarea><br>Total listen time to:<br><textarea id='timeto' name='timeto' rows='1' cols='5' onkeyup='saveValue(this);'></textarea>"
    table = "<table><tr><th>Device</th><th>Status</th></tr>"
    devicedroplist = "<label for='device'>Device:</label><select name='device' id='device'>"
    for x in status:
        table += "<tr><td>"+x['device']+"</td><td>"+x['status']+"</td></tr>"
        devicedroplist += "<option name='"+x['device']+"'value='"+x['device']+"' onchange='change'>"+x['device']+"</option>"
    table += "</table>"
    devicedroplist += "</select>"
    return "<form action='/start' method='get'>"+table+devicedroplist+form+"</form>"+render_template('spot.html')
@app.route('/complete')
def complete():
    device=request.args.get('device')
    for x in status:
        if x["device"]==device and x["status"]!='ready':
            x["status"]='ready'
    return x["status"]

@app.route('/start')
def cmd():
    stop=request.args.get('stop')
    device=request.args.get('device')
    clones=request.args.get('clones')
    timefrom=request.args.get('timefrom')
    timeto=request.args.get('timeto')
    ip=request.args.get('ip')
    inputType=request.args.get('inputType')
    songtimefrom=request.args.get('songtimefrom')
    songtimeto=request.args.get('songtimeto')
    """if inputType=='Playlists':
        inputType=1
    elif inputType=='Albums':
        inputType=2"""
    print("Input type: "+str(inputType))
    try:
        clones=clones.replace("\r\n",",")
        ip=ip.replace("\r\n",",")
    except Exception as e:
        print("Variable: "+str(e))
    print(str(clones))
    print(device)
    for x in status:
        print(status)
        if x["device"]==device and x["status"]=='ready' and stop == None:
            p = subprocess.Popen(['python3', 'sp.py', device, timefrom, timeto,clones,ip,str(inputType),songtimefrom,songtimeto])
            pid = p.pid
            x["pid"]=pid
            print(pid)
            x["status"]="View botting"
            return flask.redirect(url_for('panel'))
        elif stop=='Stop' and x["device"]==device:
            try:
                os.kill(x['pid'], 9)
                flash("Killed task on "+device)
                x["status"]='ready'
                return flask.redirect(url_for('panel'))
            except Exception as e:
                print(str(e))
                return flask.redirect(url_for('panel'))
        elif x["device"]==device and x["status"]!='ready' and stop == None:
            flash("Device "+device+" is already running a task!")
            return flask.redirect(url_for('panel'))
app.run(threaded=True, host='0.0.0.0', port=1200)