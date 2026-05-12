class DifferenceRegion:
    """
    Represents one hidden difference region in the image.
    Stores position, size, and found state.
    """

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.found = False

    def get_bbox(self):
        """
        Return the bounding box as (x1, y1, x2, y2).
        """
        return self.x, self.y, self.x + self.width, self.y + self.height

    def get_rect(self):
        """
        Return the rectangle as (x, y, w, h).
        Useful for OpenCV strategies.
        """
        return self.x, self.y, self.width, self.height

    def contains_point(self, x, y, tolerance=10):
        """
        Return True if a point falls inside the region, including tolerance.
        """
        return (
            self.x - tolerance <= x <= self.x + self.width + tolerance
            and self.y - tolerance <= y <= self.y + self.height + tolerance
        )

    def overlaps(self, other):
        """
        Return True if this region overlaps another region.
        """
        return not (
            self.x + self.width <= other.x
            or other.x + other.width <= self.x
            or self.y + self.height <= other.y
            or other.y + other.height <= self.y
        )

    def mark_found(self):
        """
        Mark this region as found.
        """
        self.found = True

    def is_found(self):
        """
        Return True if the region has already been found.
        """
        return self.found

    def reset(self):
        """
        Reset the region to not found.
        """
        self.found = False
