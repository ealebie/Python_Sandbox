import random
import requests
import datetime
import json
import time
#from datetime import timedelta, datetime, tzinfo
#import datetime
from datetime import timedelta


def login():

        head = {'Content-type':'application/json',
             'Accept':'application/json'}

        loginurl = 'http://52.235.46.243/RESTAPI/api/metranetaccountlogin/LoginMetraNet'
        loginpayload = {"$type":"MetraTech.Core.RESTAPI.Models.LoginRequest, MetraTech.Core.RESTAPI",
                        "Username":"MIF@HACK",
                        "Namespace":"system_user",
                        "Password":"123",
                        "TicketLifespanMins":99,
                        "PasswordExpirationDays":"null",
                        "Ticket":"null",
                        "SessionContext":"null"}

        payld = json.dumps(loginpayload)
        ret = requests.post(loginurl,headers=head,data=payld)
        ret.status_code

        json_data = json.loads(ret.text)

        print json_data,"\n"

        ticket  = json_data['Ticket']

        return ticket


def getOccupancy ():


        headers = {
                'Accept': 'application/json',
                'x-api-key': '3ade3cfa332cf4ef283e2386eafe1195'
        }

        response = requests.get('https://api.streetsoncloud.com/pl1/multi-lot-info', headers= headers)

        json_data = json.loads(response.text)

        #print json_data

        occupancy = json_data[0][0]['occupancy']

        #print occupancy

        return occupancy


def postoccupancyurl( plate, occupancylevel, entry, exit, token):

        postoccupancyurl = 'http://52.235.46.243/ecbRestAPI/api/ParkingPurchase/PostParkingByOccupancy'

        head = {'Content-type':'application/json',
             'X-MetraNet-Ticket': token}

        occupancypayload = {"$type": "ecbRestAPI.Models.ParkingByOccupancy, ECB.RESTAPI",
                        "Plate": "%s" % (plate),
                        "OccupancyLevel": "%s" % (occupancylevel),
                        "EntryTime": "%s" % (entry),
                        "ExitTime": "%s" % (exit)
                        }

        payld = json.dumps(occupancypayload)
        ret = requests.post(postoccupancyurl,headers=head,data=payld)

        json_data = json.loads(ret.text)

        print json_data,'\n'


        return

plates = ['123ABC','789GHI', 'ABC123', 'DEF456', 'GHI789', '246JKL', '357MNO', '999ZZZ', '888YYY', '777XXX','666WWW','555VVV','444UUU','333TTT', '222SSS']
token=login()
polling_interval = 36.0 # (100 requests in 3600 seconds)
running= True
while running:
    exittime = datetime.datetime.now().replace(microsecond=0).isoformat()
    entrytime = (datetime.datetime.now() - datetime.timedelta(minutes=(random.randint(15,480)))).replace(microsecond=0).isoformat()
    start= time.clock()
    occupancy=getOccupancy()
    plate=random.choice(plates)
    print "plate: ", plate, "\n"
    print "entry time: ", entrytime, "\n"
    print "exit time: ", exittime, "\n"
    postoccupancyurl(plate, occupancy, entrytime, exittime, token)
    work_duration = time.clock() - start
    time.sleep( polling_interval - work_duration )
