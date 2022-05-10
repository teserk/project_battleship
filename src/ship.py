class Ship:
    def __init__(self, size, x, y, orientation="V", status="OK"):  # status может быть "OK", "wounded", "dead"
        self.size = size
        self.x = x
        self.y = y
        self.orientation = orientation
        self.status = status
