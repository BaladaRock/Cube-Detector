class ColorRanges:
    # Stores HSV ranges for different colors used in detection.

    RED = {
        "lower1": [170, 120, 70],
        "upper1": [180, 255, 255],
        "lower2": [0, 120, 70],
        "upper2": [10, 255, 255]
    }

    @staticmethod
    def get_range(color_name):
        """ Returns the HSV range for a given color. """
        ranges = {
            "red": ColorRanges.RED,
            # TO DO: Add colors for the other faces
        }
        return ranges.get(color_name, None)
