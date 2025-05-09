# all the classes 
from autoMove import AutoMove
from Dstar import DstarKinda
from Grid import Grid
from manualMoveclass import manualMove
from Map import Map
from POI import POI
from Hazard import Hazard
import os

"""
    Name: clearTerminal
    
    INPUT: 
       N/A
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       clearing the terminal 
    """ 
def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

"""
    Name: askForhazards
    
    INPUT: 
       Grid:   Grid object created to represent the map
    
    RETURN: 
        list:  list of tuples 
    
    DESCRIPTION:
       asking the user for the number of hazards they would like to add to map 
       and does boundary checking to ensure all the hazards are in bounds in 
       respect to the grid. Returns the list to later be placed on the map
    """  
def askForhazards(Grid:Grid):
    result = []
    n = int(input("Please enter the number of Hazards you would like to add: "))
    clearTerminal()
    for hazard in range(n):
        coords = input("Please enter coordinates (x y): ")
        clearTerminal()
        x,y = map(int,coords.split())
        while Grid.isOutofBoundsunconverted((x,y)):
            coords = input("Please re-enter coordinates sir: ")
            clearTerminal()
            x,y = map(int,coords.split())
        temp = Hazard(Grid.convertCoords((x,y)),"size","type","name")
        result.append(temp)    
    return result


#initializing all Grid and Map
finalGrid = Grid(110,70,-5450,-6550,-9750,-10450)
theMap = Map(finalGrid)

# Creating the POIs
POI1 = POI(finalGrid.convertCoords((-5855,-10168)),"N/A","POI_ 1","N/A")
POI2 = POI(finalGrid.convertCoords((-5868,-10016)),"N/A","POI_ 2","N/A")
POI3 = POI(finalGrid.convertCoords((-5745,-9977)),"N/A","POI_ 2","N/A")
clearTerminal()
# obtaining Server IP address
ipAddress = input("Please enter IP Address: ")
clearTerminal()

# initializing Autonomous Movement class
autoMover = AutoMove(finalGrid,ipAddress)

# getting start point
#tssStartpoint = (autoMover.receiveCommand(133),autoMover.receiveCommand(134))
tssStartpoint = (-6550,-10450)
startPoint = finalGrid.convertCoords(tssStartpoint)

#picking end point using the POIs
print("Enter the number associated with the POI you would like to use as the End Point of your Journey")
print("1. POI1 (-5855,-10168)")
print("2. POI2 (-5868,-10016)")
print("3. POI3 (-5745,-9977)")
endPointpicker = int(input("Please enter approipriate integer: "))
clearTerminal()
while endPointpicker != 1 and endPointpicker != 2 and endPointpicker != 3:
    print("INVALID INPUT!")
    print("1. POI1 (-5855,-10168)")
    print("2. POI2 (-5868,-10016)")
    print("3. POI3 (-5745,-9977)")
    endPointpicker = int(input("Please re - enter approipriate integer (1,2,3): "))
    clearTerminal()
if endPointpicker == 1:
    endPoint = POI1.getCoordinates()
elif endPointpicker == 2:
    endPoint = POI2.getCoordinates()
else:
    endPoint = POI3.getCoordinates()

# Getting Hazards and adding to map
hazardList = askForhazards(finalGrid)
if len(hazardList) == 1:
    theMap.updateHazardlist(hazardList[0])
    theMap.addHazards()
elif len(hazardList) > 1: 
    theMap.updateHazardlistMultiple(hazardList)
    theMap.addHazards()


# Generate Path
theMap.generatePath(startPoint,endPoint)


# picking Movement Mode
movementMode = input("Enter 'A' to enter Autonomous Movement Mode or 'M' Manual Movement Mode: ")
clearTerminal()
while movementMode != 'A' and movementMode != 'M' and movementMode != 'a' and movementMode != 'm':
    movementMode = input("INVALID INPUT!! Please re-enter valid input (A or M): ")
    clearTerminal()

# Entering Autonomous Movement
if movementMode == 'A' or movementMode == 'a':
    autoMover.generateMovepattern(theMap.getPath())
    autoMover.moveThroughPattern()

# Entering Manual Movement 
else:
    manualMover = manualMove(ipAddress)
    manualMover.Modes()

