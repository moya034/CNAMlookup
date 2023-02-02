from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests
import mysql.connector
import re

hostName = "192.168.X.X"
serverPort = 8080
AnveoAPIkey = 'insert_API_key_here'

def GetAnveo(AnveoNumLookup):
    AnveoURL = f"https://www.anveo.com/api/v1.asp?apikey={AnveoAPIkey}&action=cnam&e164={AnveoNumLookup}"
    AnveoResponse=requests.get(AnveoURL)
    return AnveoResponse.text

def GetLocalCNAM(CHANlookup, dbCursor):
    selectSQL = f"SELECT Name FROM view_CallerID WHERE Number = '{CHANlookup}' LIMIT 1;"
    dbCursor.execute(selectSQL)
    return dbCursor.fetchone()

def GetCNAM(SearchNumber):
    CNAMresult = None
    SearchNumber = re.sub("[^0-9]", "", SearchNumber)
    if len(SearchNumber) == 11:
        dbConnection = mysql.connector.connect(host='192.168.X.X', database='CallerID', user='user', password='password')
        dbCursor = dbConnection.cursor()
        localCNAMresult = GetLocalCNAM(SearchNumber, dbCursor)
        if isinstance(localCNAMresult, tuple):        
            CNAMresult = localCNAMresult[0]
        else:
            AnveoResult = GetAnveo(SearchNumber)
            if 'Unavailable' in AnveoResult  or AnveoResult in SearchNumber:
                CNAMresult = 'NO ANVEO CNAM'
            else:
                CNAMresult = AnveoResult
            insertSQL = f"INSERT INTO tblAnveoSearch (Name,Number) VALUES('{CNAMresult}','{SearchNumber}');"
            dbCursor.execute(insertSQL)
            dbConnection.commit()
        dbConnection.close()
    else:
        CNAMresult = 'DATA ERROR'
    print(CNAMresult)
    return CNAMresult

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        phoneNumber = (self.path).replace('/','')
        self.wfile.write(bytes(GetCNAM(phoneNumber), "utf-8"))

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
