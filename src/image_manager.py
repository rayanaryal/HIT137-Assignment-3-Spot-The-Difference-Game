import cv2
import random
from .difference_region import DifferenceRegion
from .alterations.color_shift import ColorShift
from .alterations.blur_patch import BlurPatch
from .alterations.brightness_change import BrightnessChange

class ImageManager:
    """
    Handles image loading, region generation, and applying alteration strategies.
    Produces the original and modified images for the Spot-the-Difference game.
    """

    def __init__(self, image_path="", num_differences=5):
        self.image_path = image_path
        self.num_differences = num_differences
        self.image = None
        self.modified_image = None
        self.regions = []

        # Available alteration strategies
        self.strategies = [
            ColorShift(shift_value=20),
            BlurPatch(kernel_size=(15, 15)),
            BrightnessChange(beta=30)
        ]

    # ----------------------------------------------------------
    # Load the image
    # ----------------------------------------------------------
    def load_image(self):
        """
        Load the image from disk and resize it so it fits the GUI.
        """
        if not self.image_path:
            raise ValueError("No image path set.")

        # 1. Load the image
        self.image = cv2.imread(self.image_path)

        if self.image is None:
            raise FileNotFoundError(f"Could not load image: {self.image_path}")

        # 2. Resize to fit GUI window
        MAX_WIDTH = 550
        MAX_HEIGHT = 700

        h, w = self.image.shape[:2]
        scale = min(MAX_WIDTH / w, MAX_HEIGHT / h)

        new_w = int(w * scale)
        new_h = int(h * scale)

        self.image = cv2.resize(self.image, (new_w, new_h))

        # 3. Create modified copy
        self.modified_image = self.image.copy()

    # ---------------------------------------------------------
    # Generate non-overlapping regions
    # ---------------------------------------------------------
    def generate_regions(self, region_width=80, region_height=80):
        if self.image is None:
            raise ValueError("Image must be loaded before generating regions.")

        height, width, _ = self.image.shape

        # Validate region size
        if region_width <= 0 or region_height <= 0:
            raise ValueError("Region size must be positive.")

        if region_width > width or region_height > height:
            raise ValueError("Region size is larger than the image dimensions.")

        self.regions = []
        attempts = 0
        max_attempts = 200

        while len(self.regions) < self.num_differences and attempts < max_attempts:
            attempts += 1

            x = random.randint(0, width - region_width)
            y = random.randint(0, height - region_height)

            new_region = DifferenceRegion(x, y, region_width, region_height)

            # Check overlap
            if any(new_region.overlaps(existing) for existing in self.regions):
                continue

            self.regions.append(new_region)

        if len(self.regions) < self.num_differences:
            raise RuntimeError("Could not generate enough non-overlapping regions.")

    # ---------------------------------------------------------
    # Apply random strategies to each region
    # ---------------------------------------------------------
    def apply_strategies(self):
        if not self.strategies:
            raise RuntimeError("No alteration strategies available.")

        # Always start from a clean copy of the original image
        self.modified_image = self.image.copy()

        for region in self.regions:
            strategy = random.choice(self.strategies)
            region.alteration_type = strategy.__class__.__name__
            self.modified_image = strategy.apply(self.modified_image, region)

    # ---------------------------------------------------------
    # Return original image
    # ---------------------------------------------------------
    def get_original_image(self):
        return self.image

    # ---------------------------------------------------------
    # Return modified image
    # ---------------------------------------------------------
    def get_modified_image(self):
        return self.modified_image

    # ---------------------------------------------------------
    # Full pipeline helper
    # ---------------------------------------------------------
    def prepare_image(self):
        """
        Convenience method that performs the full image preparation pipeline:
        1. Load the image
        2. Generate non-overlapping regions
        3. Apply alteration strategies
        """
        self.load_image()
        self.generate_regions()
        self.apply_strategies()
