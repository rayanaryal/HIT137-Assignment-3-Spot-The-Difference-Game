import cv2
from .base import AlterationStrategy

class BlurPatch(AlterationStrategy):
    """
    Applies a Gaussian blur to a selected region of the image.
    This reduces detail and creates a subtle difference.
    """

    def __init__(self, kernel_size=(15, 15)):
        self.kernel_size = kernel_size

    def apply(self, image, region):
        x, y, w, h = region.x, region.y, region.width, region.height
        roi = image[y:y+h, x:x+w].copy()
        blurred = cv2.GaussianBlur(roi, self.kernel_size, 0)
        image[y:y+h, x:x+w] = blurred
        return image
