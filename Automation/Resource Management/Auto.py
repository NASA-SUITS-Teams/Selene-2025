from Resource import Resource

from Log import LogData
from command2 import Command

if __name__ == "__main__":

    command = Command()
    resource = Resource()
    log = LogData()
    IPAdress = input("Please enter IP address: ")
    command.setIPAdress(IPAdress)


    while True:
        command.getData()
        resource.loadJson()
        resource.processData()
        resource.monitorData()
        log.loadJson()
        log._log_values()
        log.saveJson("User_Interface/UI_Main/client/src/telemetry_json/")



