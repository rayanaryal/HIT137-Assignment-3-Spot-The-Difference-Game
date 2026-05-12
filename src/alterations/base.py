
from abc import ABC, abstractmethod

class AlterationStrategy(ABC):
    """
    Abstract base class for all alteration strategies.
    Each alteration modifies a selected image region in a different way.
    """

    @abstractmethod
    def apply(self, image, region):
        """
        Apply the alteration to the given image region.
        Must return the modified image.
        """
        pass
