"""
    CLASS:
        POI

    ATTRIBUTES:
        Tuple Coordinate : (X,Y) position of the POI.
        String Type : Type of POI (mission, viewpoint, collection site, etc.)
        String Name : Name of the POI.
        String Note : Description of POI.

    METHODS:
        __init__ : Constructor for the class.
        Getters : Returns the value of the attribute.
        Setters : Changes the value of the attribute.
        __str__ : Returns a string of the object.
"""
class POI:
    """
    Name: __init__ (CONSTRUCTOR)
    
    INPUT: 
        coordinate: coordinate location on the grid of the POI. Coordinates will be 
                    verified before the POI is created.
        type : type of POI (mission, viewpoint, collection site, etc.).
        String Name : Name of the POI.
        String Note : Description of POI.
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will instantiate a POI object.
    """
    def __init__(self, coordinates, type, name, note):
        self.coordinates = coordinates # tuple
        self.type = type # string
        self.name = name # string
        self.note = note # string

    # getters and setters:
    """
    Name: getCoordinates
    
    INPUT: 
       N/A
    
    RETURN: 
        tuple:  tuple of x and y coordinates
    
    DESCRIPTION:
       gets the cooridnate tuple for the POI.
    """
    def getCoordinates(self):
        return self.coordinates
    
    """
    Name: setCoordinates
    
    INPUT: 
       tuple:  tuple of x and y coordinates
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update POI coordinates.
    """
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    """
    Name: getType
    
    INPUT: 
       N/A
    
    RETURN: 
        string: classiffication of the POI (rock, crater, etc)
    
    DESCRIPTION:
       getting the classification of the POI (rock, crater, etc) 
    """
    def getType(self):
        return self.type

    """
    Name: setType
    
    INPUT: 
       string: classiffication of the POI (rock, crater, etc)
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update classification of the POI.
    """ 
    def setType(self, type):
        self.type = type

    """
    Name: getName
    
    INPUT: 
       N/A
    
    RETURN: 
        string: the name given to the POI
    
    DESCRIPTION:
       getting the name of the POI
    """
    def getName(self):
        return self.name
    
    """
    Name: setName
    
    INPUT: 
       string: the name being given to the POI
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update name of the POI.
    """ 
    def setName(self, name):
        self.name = name

    """
    Name: getNote
    
    INPUT: 
       N/A
    
    RETURN: 
        string: additional description of the POI
    
    DESCRIPTION:
       getting any additional description the user woould like to add as 
       details of the POI
    """
    def getNote(self):
        return self.note
    
    """
    Name: setNote
    
    INPUT: 
       string: additional description of the POI
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update description of the POI.
    """
    def setNote(self, note):
        self.note = note
        
    """
    Name: __str__
    
    INPUT: 
       N/A
    
    RETURN: 
        String
    
    DESCRIPTION:
        This Method will begin convert the object to a string and return.
    """
    def __str__(self):
        return f"Coordinates: {self.coordinates}, Type: {self.type}, Name: {self.name}, Notes: {self.note}"
