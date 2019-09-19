from app import app
from easysnmp import Session
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
import json
import sys
from flask import Response
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
do_logs = config['LOG']['Enabled']
if do_logs:
    import logging
    from datetime import date
    logging.basicConfig(filename=f'logs/{date.today()}.log', filemode='a', level=logging.INFO)

raspberry_ip = config['IP_ADDRESS']['RaspberryPi']
printer_ip = config['IP_ADDRESS']['KonicaMinolta']

session = Session(hostname = printer_ip, community='public', version=2)
init_nums = []

@app.route('/count')
def count():
    global init_nums
    init_nums = new_get_values()
    def event_stream():
        global init_nums
        notif_Receiver()        #Start notif_Receiver
        new_nums = new_get_values()
        delta_values = delta_from_list(init_nums,new_nums)
        init_nums = new_nums
        values = deltas_2_values(delta_values)      #Calculate final numbers from raw values
        message = constr_message(values)            #Construct the values into message
        if do_logs: logging.info(f'{delta_values} | {values}')
        return message
    return Response(event_stream(), mimetype="text/event-stream")

codes = (".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.1", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.1.1",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.1.2", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.1.2",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.1", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.2.1",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.5.2.2", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.2.1.7.2.2",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.3.1.5.1", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.3.1.6.1",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.3.0", ".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.10.0",\
         ".1.3.6.1.4.1.18334.1.1.1.5.7.2.1.8.0")

def constr_message(alist):
    data = {str(ide) : line for ide, line in enumerate(alist)}
    jsn_str = json.dumps(data)
    message = "data: {jsdata}\n\n".format(jsdata = jsn_str)
    message += "retry: 500\n"
    return message

def notif_Receiver():
    def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
        transportDispatcher.jobFinished(1)
        return
    transportDispatcher = AsynsockDispatcher()
    transportDispatcher.registerRecvCbFun(cbFun)
    transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openServerMode((raspberry_ip, 1162)))
    transportDispatcher.jobStarted(1)
    try:
        transportDispatcher.runDispatcher()
    except:
        transportDispatcher.closeDispatcher()
        raise
    return

def new_get_values():
    global codes
    values = []
    try:
        for snmp_code in codes:
            values.append(int(session.get(snmp_code).value))
        return values
    except:
        return init_nums

def deltas_2_values(delta):
    values = [0] * 7
    A3 = delta[1] + delta[3] + delta[5] + delta[7]
    A4 = (delta[0] + delta[2] + delta[4] + delta[6]) - (2 * A3)
    values[0] = (delta[0] + delta[2]) - (2 * (delta[1] + delta[3]))
    values[1] = delta[1] + delta[3]
    values[4] = (delta[8] if delta[9] == 0 else delta[9])
    if A4 > 0:
        values[2] = delta[4] + delta[6]
        if delta[10] > 0:
            values[5]= delta[10] - (values[2] // 2 + values[2] % 2)
            values[0] = (A4 - 2 * values[5]) + (delta[12] - delta[11])
        elif delta[0] > 0 and delta[12] != delta[11]:
            values[0] = delta[12] % delta[11]
            values[5] = delta[11] - values[0]
        elif delta[2] != delta[12]:
            values[0] += (delta[12] - delta[11])
    elif A3 > 0:
        values[3] = delta[5] + delta[7]
        if delta[10] > 0:
            values[6]= delta[10] - (values[3] // 2 + values[3] % 2)
            values[1] = (A3 - 2 * values[6]) + (delta[12] - delta[11])
        elif delta[0] > 0 and delta[12] != delta[11]:
            values[1] = delta[12] % delta[11]
            values[6] = delta[11] - values[1]
        elif delta[2] != delta[12]:
            values[1] += (delta[12] - delta[11])
    else:
        values[0] = (delta[12] - delta[11])
    return values

def delta_from_list(list1, list2):
    delta_list = []
    for item1, item2 in zip(list1,list2):
         delta_list.append(item2 - item1)
    return delta_list
