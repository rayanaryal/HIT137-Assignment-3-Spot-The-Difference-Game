class DifferenceRegion:
    '''
    Represents a single difference region in the image. 
    Stores the position, size, alteration type, and whether it has been found.
    '''

    def __init__(self, x, y, width, height, alteration_type): # Position and size of the difference region
        self.x=x
        self.y=y
        self.width = width
        self.height = height
        self.alteration_type = alteration_type # alteration will be applied e.g., blur, color shift, brightness change)
        self.found = False  # tracks whethe the user has already found this region

    @property
    def region(self):
        return (self.x, self.y, self.width, self.height) #returns the region as a tuple (x,y, width, height). Useful for drawing or debugging.
    
    def contains_point(self, click_x, click_y, tolerance=10): #Check if a user's click(x,y) is inside this region. A tolerance helps clicking easier
        return (
            self.x-tolerance <= click_x<=self.x + self.width +tolerance and self.y - tolerance <= click_y <= self.y + self.height + tolerance
        )

    def mark_found(self): # Mark this region as found
        self.found = True

    def is_found(self): #return true if the region has already been found
        return self.found
    
    def __repr__(self): # Returb a developer-friendly string representation of the region; useful for debugging and loggin
        return(
            f"DifferenceRegion(x={self.x}, y={self.y}," 
            f"width={self.width}", height ={self.height}, found={self.found}
            )"
        
        




