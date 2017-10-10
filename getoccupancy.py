import redis
import requests
import time
#import httplib2 as http
import json

def getOccupancy ():


        headers = {
                'Accept': 'application/json',
                'x-api-key': '3ade3cfa332cf4ef283e2386eafe1195'
        }

        response = requests.get('https://api.streetsoncloud.com/pl1/multi-lot-info', headers= headers)

        json_data = json.loads(response.text)

        print json_data

        occupancy = json_data[0][0]['occupancy']

        print occupancy

        return occupancy

def postToAppIoT (occupancy):

        timestamp = int(time.time()) * 1000

        headers = {

                'Authorization': 'SharedAccessSignature sr=https%3a%2f%2feappiotsens.servicebus.windows.net%2fdatacollectoroutbox%2fpublishers%2fedaeeb3c-574e-4738-976e-b91d639d8dd3%2fmessages&sig=x3RiOlrb4dOQIOkjxUVXLwdj6SFleYRL9V6mBajsqvY%3d&se=4662226702&skn=SendAccessPolicy',

                'DataCollectorId' : 'edaeeb3c-574e-4738-976e-b91d639d8dd3',
                'Content-Type': 'application/json',

                'PayloadType': 'Measurements',

                'Timestamp': ('%s' % timestamp),

                'Cache-Control': 'no-cache',

        }


        data =  [{"id":"4d761d81-1bcb-4459-8ff4-741fc349835d","v":[{"m":[occupancy],"t":('%s' % timestamp)}]}]



        response = requests.post('https://eappiotsens.servicebus.windows.net:443/datacollectoroutbox/publishers/edaeeb3c-574e-4738-976e-b91d639d8dd3/messages', json=data , headers=headers)

        #json_data = json.loads(response.text)

        #print json_data

        return



polling_interval = 3.60 # (100 requests in 3600 seconds)
running= True
while running:
    start= time.clock()
    occupancy=getOccupancy()
    postToAppIoT(occupancy)
    #anything_else_that_seems_important()
    work_duration = time.clock() - start
    time.sleep( polling_interval - work_duration )
