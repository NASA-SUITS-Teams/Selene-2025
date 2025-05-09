# Necessay Packages

from Grid import Grid               #importing the Grid class

from Hazard import Hazard           #importing the Hazard Class

from POI import POI                 #importing the POI class 
 
from Dstar import DstarKinda      #importing the Dstar class

"""
Class: Map

ATTRIBUTES: 
    Grid Grid:                  The grid that will function as our maps environment 
    list hazards:               list of Hazard objects
    list poiList:               list of POI objects 
    DstarKinda PathPlanner:   Dstar object to generate path
    list Path:                  the final path generated

METHODS:
    __init__                   Constructor 
    getPath()                  return the generated path
    generatePath()             create the path
    getGrid()                  return the current state of the Grid
    addHazard()                marks the hazards on the map
    updateHazardlist()         adds a single hazard to the hazard list
    updateHazardlistMultiple():adds a list of hazards to hazards list
    
PACKAGES:

    from Grid import Grid           importing the Grid class 
    from Hazard import Hazard       import the Hazard class
    from POI import POI             import the POI class
    from Dstar import D_star-kinda  import the Dstar class 
 

DESCRIPTION:

    The functionality of the map needs to be discussed so I this description is a work in progress 
   

"""
class Map:
    """
    Name: __init__ ()
    
    INPUT: 
        GridRow:  Size of rows
        GridCol:  Size of columns 
        XMax:     maximum x value
        XMin:     minimum x value
        YMax:     maximum y value
        YMin:     minimum y value
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        Constructor that creates the map enviroment and all its functionality   
    """
    def __init__(self,theGrid:Grid):
        # The grid
        self.Grid = theGrid
        
        # List of Hazards
        self.hazards: list[Hazard] = []
        
        # List of POIs
        self.poiList: list[POI] = []
        
        # The path generator
        self.PathPlanner = DstarKinda(self.Grid)
        
        # where the path will be stored 
        self.Path = []
        
    """
    Name: generatePath()
    
    INPUT: 
        tuple start:    the path starting location
        tuple end:      the path ending location
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        generate the path the rover is expecting to travel and save that path  
    """
    def generatePath(self,start:tuple[int,int],end:tuple[int,int]):
        # generate the path 
        self.PathPlanner.generatePath(start,end)
        
        # clean the path
        self.Path = self.PathPlanner.cleanPath(start)
        
    """
    Name: getGrid()
    
    INPUT: 
        N/A
    
    RETURN: 
        Grid Grid:      return the numpy array grid 
    
    DESCRIPTION:
        returning the grid and all its data 
    """
    def getGrid(self):
        return self.Grid.getMatrix()
    """
    Name: addHazards()
    
    INPUT: 
        N/A
    
    RETURN: 
       N/A
    
    DESCRIPTION:
        mark the hazard coordinates on the map
    """
    def addHazards(self):
        for hazards in self.hazards:
            self.PathPlanner.addSinglehazard(hazards.getCoordinates())
    """
    Name: updateHazardlist()
    
    INPUT: 
        N/A
    
    RETURN: 
       N/A
    
    DESCRIPTION:
        adds a single hazard object to the list of hazards
    """
    def updateHazardlist(self, Hazard: Hazard):
        self.hazards.append(Hazard)
    """
    Name: updateHazardlistMultiple()
    
    INPUT: 
        N/A
    
    RETURN: 
       N/A
    
    DESCRIPTION:
        adds a multiple hazard object to the list of hazards
    """
    def updateHazardlistMultiple(self,Hazards: list[Hazard]):
        for hazard in Hazards:
            self.hazards.append(hazard)
    """
    Name: getHazardlist()
    
    INPUT: 
        N/A
    
    RETURN: 
       list hazard: list of Hazard objects
    
    DESCRIPTION:
        return the list of hazard objects
    """
    def getHazardlist(self):
        return self.hazards
    """
    Name: getPath()
    
    INPUT: 
        N/A
    
    RETURN: 
       list Path: the generated path 
    
    DESCRIPTION:
        return the generated path 
    """        
    def getPath(self):
        return self.Path
        
    
# Main Driver

#finalGrid = Grid(110,70,-5450,-6550,-9750,-10450)
#theMap = Map(finalGrid)
#start = (-5664, -10080.1005859375)
#tartPoint = finalGrid.convertCoords(start)
#x,y = -5868.10, -10016.10
#temp = (x,y)
#endPoint = finalGrid.convertCoords(temp)
#theMap.generatePath(startPoint,endPoint)
#print(theMap.getPath())
    
    
    
        
        
        