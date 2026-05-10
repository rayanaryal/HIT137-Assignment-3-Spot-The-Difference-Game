import cv2
import numpy as np
from .base import AlterationStrategy

class BrightnessChange(AlterationStrategy):
    """
    Adjusts the brightness of a selected region of the image.
    """

    def __init__(self, beta=30):
        self.beta = beta

    def apply(self, image, region):
        """
        Apply brightness adjustment to the specified region and return the modified image.
        """
        # Use the API from DifferenceRegion
        x, y, w, h = region.get_rect()

        roi = image[y:y+h, x:x+w].copy()
        if roi.size == 0:
            return image

        # alpha=1.0 keeps contrast, beta shifts brightness
        adjusted = cv2.convertScaleAbs(roi, alpha=1.0, beta=self.beta)

        image[y:y+h, x:x+w] = adjusted
        return image
