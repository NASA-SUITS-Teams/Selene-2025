"""
This file contains the Grid class.
The Grid class is used as part of the Map class in order to determine
where certain coordinated are located on the map. The map class shall
have one Grid object as an attribute
"""

import numpy as np
class Grid:

    '''
    Paramaterized constructor for the Grid class.
    May be default later, but left paramaterized for now for testing
    GridRow is the number of rows in the grid
    GridCol is the number of columns in the
    GridSize nultiplies GridRow & GridCol to make the size of the grid
    XMax and XMin are the maximum and minimum values for the x coordinates
    YMax and YMin are the maximum and minimum values for the y coordinates
    squareSizeX is the range of possible values per section 
    squareSizeY is the range of possible values per section
    '''
    def __init__(self, GridRow, GridCol, XMax, XMin, YMax, YMin):

        self.GridRow = GridRow
        self.GridCol = GridCol
        self.GridSize = GridRow * GridCol
        self.XMax = XMax
        self.XMin = XMin
        self.YMax = YMax
        self.YMin = YMin
        self.squareSizeX = (XMax - XMin) / GridRow
        self.squareSizeY = (YMax - YMin) / GridCol
        self.matrix = np.zeros((GridRow, GridCol), dtype=float)

    """
    Name: verifyCoords
    Purpose: To verify that the coordinates are within the range of the grid
    Parameters: self, coord (tuple)
    Returns: Bool (True if the coordinates are within the range, False otherwise
    """
    def verifyCoords(self, coord):
        print()
        if coord[0] < self.XMin or coord[0] > self.XMax:
            return False
        if coord[1] < self.YMin or coord[1] > self.YMax:
            return False
        return True
    
    """
       Name: coordInputUser
    Purpose: Prompts user to input coordinates and verifies that they are within the range
    Parameters: self
    Returns: Tuple (if valid coordinates are entered) or None (if user quits)
    
    def coordInputUser(self):
        while True:
            # Prompt user for coordinates
            coord = input("Enter coordinates in the form of x, y or enter 'q' to quit: ").strip()

            # Check if the user wants to quit
            if coord.lower() == "q":
                return None

            try:
                # Parse the input into a tuple of integers
                x, y = map(int, coord.split(","))
                coordPair = (x, y)

                # Verify the coordinates
                if self.verifyCoords(coordPair):
                    return coordPair
                else:
                    print("Invalid coordinates. Please enter values within the grid range.")
            except ValueError:
                print("Invalid input format. Please enter coordinates in the form of x, y.")
    """
    """
    Name: searchGridRow
    Purpose: To determine which section of the grid a y coordinate is in
    Parameters: self, coord
    Returns: int (the section of the grid the coordinate is in)
    """  
    def searchGridRow(self, coord):
             
        #creating the boundaries for binary search
        #high is -1 because our size count starts at 0
        low = 0
        high = self.GridRow - 1
        while low <= high:
                #make the midpoint the avg of low and high values
                mid = (low + high) // 2
                #determine the start and end of the midpoint section
                #so, if our Ymin is -50, the squareSizeY is 20, and the mid is 2
                #we'd get a start value of -10 for the section
                #and an end value of 10 for the section
                start = self.YMin + mid * self.squareSizeY
                end = start + self.squareSizeY
    
                #return the section if coordinate is within its range
                if start <= coord < end:
                    return mid
                #if the coordinate is less than the start, move the high boundary
                elif coord < start:
                    high = mid - 1
                # return middle if it's equal to low
                elif low == mid:
                    return mid 
                #if the coordinate is greater than the end, move the low boundary
                else:
                    low = mid + 1

    """
    Name: searchGridCol
    Purpose: To determine which section of the grid an x coordinate is in
    Parameters: self, coord
    Returns: int (the section of the grid the coordinate is in)
    """  
    def searchGridCol(self, coord):           
        #creating the boundaries for binary search
        #high is -1 because our size count starts at 0
        low = 0
        high = self.GridRow - 1
        while low <= high:
                #make the midpoint the avg of low and high values
                mid = (low + high) // 2
                #determine the start and end of the midpoint section
                #so, if our Xmin is -50, the squareSizeX is 20, and the mid is 2
                #we'd get a start value of -10 for the section
                #and an end value of 10 for the section
                start = self.XMin + mid * self.squareSizeX
                end = start + self.squareSizeX

                #return the section if coordinate is within its range
                if start <= coord < end:
                    return mid
                #if the coordinate is less than the start, move the high boundary
                elif coord < start:
                    high = mid - 1
                # return middle if it's equal to low
                elif low == mid:
                    return mid
                #if the coordinate is greater than the end, move the low boundary
                else:
                    low = mid + 1
        
    """
    Name: convertCoords
    Purpose: convert a coordinates tuple to ints to figure out which section it's in
    Parameters: self, coordPair
    Returns: Tuple (with the section of the grid the coordinate is in)
    """  
    def convertCoords(self, coordPair):
        #get the tuple values by themselves
        x = coordPair[0]
        y = coordPair[1]
        
        #make sure we're working with valid coordinates
        if self.verifyCoords(coordPair) == False:
            print("Coordinates out of bounds.")
            return None

        else:
        #call searchGrid for each value
            x = self.searchGridCol(x)
            y = self.searchGridRow(y)

        #make a new tuple for the grid section
            GridSection=(x, y)
            return GridSection
     
    """
    Name: isOutofBound()
    
    INPUT: 
      points:   tuple being checked if the coordinates are out of bound
    
    RETURN: 
      Bool:     True or False based on if the point is out of bound
    
    DESCRIPTION:
        checking the X and Y values to the dimensions of the grid to determine if the 
        point is within bounds 
    """    
    def isOutofBounds(self,points: tuple):
        
        if points[0] >= self.GridRow or points[0] < 0:
            return True
        else:
            if points[1] >= self.GridCol or points[1] < 0:
                return True
            else:
                return False
    """
    Name: isOutofBoundsunconverted()
    
    INPUT: 
      points:   tuple being checked if the coordinates are out of bound
    
    RETURN: 
      Bool:     True or False based on if the point is out of bound
    
    DESCRIPTION:
        checking the X and Y values to the dimensions of the grid to determine if the 
        point is within bounds un converted values (Max X anf Y from NASA map)
    """  
    def isOutofBoundsunconverted(self,points: tuple):
        
        if points[0] >= self.XMax or points[0] < self.XMin:
            return True
        else:
            if points[1] >= self.YMax or points[1] < self.YMin:
                return True
            else:
                return False
    """
    Name: getMatrix()
    
    INPUT: 
        N/A
    
    RETURN: 
      numpy.array:    the numpy array used to represent the grid
    
    DESCRIPTION:
        used to get the current state of the grid/map including all weights and 
        hazards
    """     
    def getMatrix(self):
        return self.matrix

#test code for inputting coordinates starts here
#test= Grid(110, 70, -5450, -6550, -9750, -10450)
#print(test.getMatrix())
#someCoords = test.coordInputUser()
#print ("Coordinates: ", someCoords)
#test code for inputting coordinates ends here

#test code for converting coordinates starts here
#demo = Grid(110, 70, -5450, -6550, -9750, -10450)
#print(demo.convertCoords((-5664, -10080.1005859375)))
#test code for converting coordinates ends here