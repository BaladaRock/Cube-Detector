class ColorRanges:
    # Predefined HSV intervals for Rubik's Cube colors.
    # We will use this in case the interactive UI color detection has failed

    @staticmethod
    def get_range(color):
        ranges = {
            "red": {
                "lower1": [0, 120, 70],
                "upper1": [10, 255, 255],
                "lower2": [170, 120, 70],
                "upper2": [180, 255, 255]
            },
            "orange": {
                "lower1": [11, 120, 100],
                "upper1": [20, 255, 255],
                "lower2": [0, 0, 0],  # Unused
                "upper2": [0, 0, 0]
            },
            "yellow": {
                "lower1": [21, 120, 100],
                "upper1": [32, 255, 255],
                "lower2": [0, 0, 0],
                "upper2": [0, 0, 0]
            },
            "green": {
                "lower1": [40, 100, 70],
                "upper1": [85, 255, 255],
                "lower2": [0, 0, 0],
                "upper2": [0, 0, 0]
            },
            "blue": {
                "lower1": [90, 120, 70],
                "upper1": [130, 255, 255],
                "lower2": [0, 0, 0],
                "upper2": [0, 0, 0]
            },
            "white": {
                "lower1": [0, 0, 200],
                "upper1": [180, 50, 255],
                "lower2": [0, 0, 0],
                "upper2": [0, 0, 0]
            }
        }

        # If color is not found, return a fully black mask
        return ranges.get(color, {
            "lower1": [0, 0, 0],
            "upper1": [0, 0, 0],
            "lower2": [0, 0, 0],
            "upper2": [0, 0, 0]
        })
