"""
    CLASS:
        Hazard

    ATTRIBUTES:
        Tuple Coordinate : (X,Y) position of the hazard. Coordinates will be
                            verified before the hazard is created.
        Float Size : Total area of the hazard.
        String Type : Type of hazard (rock, crater, cliff, etc.)
        String Name : Name of the hazard.

    METHODS:
        __init__ : Constructor for the class.
        Getters : Returns the value of the attribute.
        Setters : Changes the value of the attribute.
        __str__ : Returns a string of the object.
"""
class Hazard:
    """
    Name: __init__ (CONSTRUCTOR)
    
    INPUT: 
       coordinate: coordinate location on the grid of the hazard.
       size : total size (area) of the hazard.
       type : type of hazard (rock, crater, cliff, etc.).
       name : name of hazard.
    
    RETURN: 
        N/A
    
    DESCRIPTION:
        This Method will instantiate a hazard object.
    """
    def __init__(self, coordinate, size, type, name):
        self.coordinate = tuple(coordinate) # tuple
        self.size = size # float
        self.type = type # string
        self.name = name # string

    """
    Name: getCoordinates
    
    INPUT: 
       N/A
    
    RETURN: 
        tuple:  tuple of x and y coordinates
    
    DESCRIPTION:
       gets the cooridnate tuple for the hazard.
    """
    def getCoordinates(self):
        return self.coordinate
    
    """
    Name: setCoordinates
    
    INPUT: 
       tuple:  tuple of x and y coordinates
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update hazard coordinates.
    """ 
    def setCoordinates(self, coordinate:tuple[int,int]):
        self.coordinate = coordinate

    """
    Name: getSize
    
    INPUT: 
       N/A
    
    RETURN: 
        float: size of hazad 
    
    DESCRIPTION:
       getting the size of the hazard 
    """
    def getSize(self):
        return self.size
    
    """
    Name: setSize
    
    INPUT: 
       float:   the size of the hazard 
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update size of the hazard.
    """ 
    def setSize(self, size):
        self.size = size

    """
    Name: getType
    
    INPUT: 
       N/A
    
    RETURN: 
        string: classiffication of the hazard (rock, crater, etc)
    
    DESCRIPTION:
       getting the classification of the hazard (rock, crater, etc) 
    """
    def getType(self):
        return self.type

    """
    Name: setType
    
    INPUT: 
       string: classiffication of the hazard (rock, crater, etc)
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update classification of the hazard.
    """ 
    def setType(self, type):
        self.type = type

    """
    Name: getName
    
    INPUT: 
       N/A
    
    RETURN: 
        string: the name given to the hazard
    
    DESCRIPTION:
       getting the name of the hazard
    """
    def getName(self):
        return self.name
    
    """
    Name: setName
    
    INPUT: 
       string: the name being given to the hazard
    
    RETURN: 
        N/A
    
    DESCRIPTION:
       update name of the hazard.
    """ 
    def setName(self, name):
        self.name = name
    
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
        return f"Coordinate: {self.coordinate}, Size: {self.size}, Type: {self.type}, Name: {self.name}"


