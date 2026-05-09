import cv2
import numpy as np
from .base import AlterationStrategy

class ColorShift(AlterationStrategy):
    def __init__(self, shift_value=20):
        self.shift_value = shift_value

    def apply(self, image, region):
        x, y, w, h = region.get_rect()
        roi = image[y:y+h, x:x+w].copy()

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        h_channel, s_channel, v_channel = cv2.split(hsv)

        h_channel = (h_channel.astype(np.int16) + self.shift_value) % 180
        h_channel = h_channel.astype(np.uint8)

        shifted = cv2.merge([h_channel, s_channel, v_channel])
        roi = cv2.cvtColor(shifted, cv2.COLOR_HSV2BGR)

        image[y:y+h, x:x+w] = roi
        return image