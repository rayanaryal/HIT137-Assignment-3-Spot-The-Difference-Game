# HIT137-Assignment-3-Spot-The-Difference-Game

## Group assignment of Software Now.
Team Members
- Rajan Aryal
- Rupesh Timalsina
- Swastik Bista


## DEscription
This project is a desktop spot-the-difference game built with Python, Tkinter, and OpenCV.
The player loads an image, the program creates a modified copy with hidden differences, and the user must find them by clicking on the altered image.

## Technologies used
- Python
- Tkinter
- OpenCV
- GitHub



First we created a folder named src, and inside the folder we created follwoing files.
    1. main.py (the entry point)
    2. gui.py (manages the Tkinter interface)
    3. image_mangaer.py (handles OpenCV loading, cloning, and modification logic)
    4. game_logic.py (manages the game state like score, mistakes, win/loss tracking)
    5. difference_region.py (encapsulates the logic for a single difference point (the 'data' object for our differences))


Creating folder name alterations inside folder named src. And following files are created inside alteration foler
    1. base.py
    2. color_shift.py
    3. blur_patch.py
    4. brightness_change.py


## Class Design: DifferenceRegion

### Purpose
Represents a single difference region in the image. It stores the position, size, and whether the region has been found by the user.

### Attributes
- x: The X coordinate of the top-left corner of the region.
- y: The Y coordinate of the top-left corner of the region.
- width: The width of the difference region.
- height: The height of the difference region.
- found: A boolean value that indicates whether the region has already been found.

### Methods
- contains_point(x, y): Returns True if a user's click is inside this region.
- mark_found(): Marks the region as found.
- is_found(): Returns True if the region has already been found.

### Reason this class exists
The game needs to track each difference separately. This class helps the GameLogic class check:
- if the user clicked inside a difference
- if the difference was already found
- how many differences remain



## After DifferenceRegion class, creating GameLogic class which is brain of the game


  ## Class Design: GameLogic
    ## Class Design: GameLogic

### Purpose
'GameLogic' manages the rules and flow of the Spot-the-Difference game. It tracks difference regions, user mistakes, click checking, and win/lose conditions.

### Attributes
- 'regions': List of 'DifferenceRegion' objects.
- 'max_mistakes': Maximum number of mistakes allowed, default is 3.
- 'mistakes': Current number of mistakes made by the user.
- 'game_over': Boolean flag indicating whether the game has ended.

### Methods
- 'add_region(region)': Adds a 'DifferenceRegion' to the game.
- 'check_click(x, y)': Checks whether the user clicked on a difference.
- 'all_found()': Returns 'True' if all differences are found.
- 'remaining_differences()': Returns the number of differences left.
- 'is_game_over()': Returns 'True' if the game is over.
- 'reset()': Resets mistakes and found states for a new game.

### Why this class exists
This class acts as the central controller for game rules. It keeps game logic separate from the GUI and makes the program easier to maintain and extend.


## Class Design: AlterationStrategy (Base Class)

### Purpose
This abstract base class defines the common interface for all alteration types used in the Spot-the-Difference game. Each alteration modifies a selected region of the image in a different way.

### Method
- 'apply(image, region)': Applies the alteration to the given image region and returns the modified image.

### Why this class exists
This class enables polymorphism. Each alteration type ('BlurPatch', 'ColorShift', 'BrightnessChange') inherits from this base class and implements its own version of 'apply()'. This keeps 'ImageManager' clean and makes it easy to add new alteration types later.


## Class Design: ColorShift

### Purpose
'ColorShift' applies a colour-based modification to a selected region of the image.  
It can shift hue, saturation, or RGB values to create a noticeable but natural-looking difference for the Spot-the-Difference game.

### Attributes
- 'shift_value': Amount of colour shift to apply, such as increasing hue or adjusting RGB values.
- 'region': The image region provided by 'ImageManager' for modification.

### Methods
- 'apply(image, region)': Applies the colour shift to the specified image region and returns the modified image.

### Why this class exists
This class is one of the concrete implementations of 'AlterationStrategy'. It demonstrates polymorphism by overriding 'apply()' with its own colour-shifting behaviour. It keeps image processing modular and allows 'ImageManager' to apply different alteration types without knowing their internal logic.


## Class Design: BlurPatch

### Purpose
'BlurPatch' applies a blur effect to a selected region of the image.  
This reduces detail in that area, creating a subtle but noticeable difference for the Spot-the-Difference game.

### Attributes
- 'kernel_size': Size of the Gaussian blur kernel, for example '(15, 15)'. Larger values produce stronger blur.
- 'region': The image region provided by 'ImageManager' for modification.

### Methods
- 'apply(image, region)': Applies a Gaussian blur to the specified region and returns the modified image.

### Why this class exists
This class is another concrete implementation of the 'AlterationStrategy' base class. It demonstrates polymorphism by overriding 'apply()' with its own blur-based behaviour. It keeps image processing modular and allows 'ImageManager' to apply different alteration types without knowing how each one works internally.


## Class Design: BrightnessChange

### Purpose
'BrightnessChange' adjusts the brightness of a selected region of the image.  
This creates a subtle but visible difference by making the area slightly lighter or darker, which is ideal for a Spot-the-Difference game.

### Attributes
- 'brightness_factor': Numeric value controlling brightness adjustment. Values greater than '1.0' make the region brighter, while values less than '1.0' make it darker.
- 'region': The image region provided by 'ImageManager' for modification.

### Methods
- 'apply(image, region)': Applies brightness adjustment to the specified region and returns the modified image.

### Why this class exists
This class is a concrete implementation of 'AlterationStrategy'. It demonstrates polymorphism by overriding 'apply()' with brightness-specific behaviour. It keeps image processing modular and allows 'ImageManager' to apply different alteration types without knowing their internal logic.


## Class Design: ImageManager

### Purpose
'ImageManager' is responsible for loading images, generating random non-overlapping regions for modification, applying alteration strategies, and producing the final pair of images for the Spot-the-Difference game. It acts as the central controller that coordinates region generation and image modification.

### Responsibilities
- Load the original image from disk.
- Generate exactly 5 'DifferenceRegion' objects.
- Ensure regions do not overlap.
- Apply a randomly selected 'AlterationStrategy' to each region.
- Produce the modified image.
- Provide both the original and altered images to the GUI.

### Attributes
- 'image_path': Path to the original image file.
- 'image': The loaded OpenCV image.
- 'regions': A list of generated 'DifferenceRegion' objects.
- 'strategies': A list of available alteration strategies, such as 'ColorShift', 'BlurPatch', and 'BrightnessChange'.
- 'num_differences': Number of differences to generate, set to 5.

### Methods
- 'load_image()': Loads the image from disk using OpenCV.
- 'generate_regions()': Creates random, non-overlapping regions and ensures each region fits inside the image.
- 'apply_strategies()': Applies a randomly selected 'AlterationStrategy' to each generated region.
- 'get_original_image()': Returns the unmodified image.
- 'get_modified_image()': Returns the altered image with differences applied.

### Why this class exists
'ImageManager' keeps image loading, region generation, and alteration handling separate from the GUI and game rules. This makes the program easier to maintain, test, and extend.


## Class Design

### Overview

This project uses a modular object-oriented design with three main classes:

- 'ImageManager' handles image loading, region generation, and image alteration.
- 'DifferenceRegion' represents each hidden difference area.
- 'GameLogic' manages click checking, mistakes, and game progress.

Together, these classes separate image processing, game rules, and data storage.

### ImageManager

'ImageManager' prepares the original and modified images.

It is responsible for:
- loading the image,
- generating five non-overlapping difference regions,
- applying random OpenCV-based alterations,
- storing both the original and modified images.

This class keeps all image-processing tasks in one place.

### DifferenceRegion

'DifferenceRegion' stores the properties of a single difference.

It contains:
- position and size information,
- the found/not-found state,
- methods for point detection and overlap checking.

This class is intentionally small and focused on region data.

### GameLogic

'GameLogic' controls the gameplay rules.

It is responsible for:
- starting a new round,
- checking whether a click matches a difference,
- tracking mistakes,
- identifying when the game is finished,
- supporting reveal and reset actions.

This class connects the GUI with the image management layer.

### Class Interaction

'''text
GUI -> GameLogic -> ImageManager -> DifferenceRegion
'''

The GUI handles user input and display.  
'GameLogic' applies the game rules.  
'ImageManager' prepares the images and regions.  
'DifferenceRegion' stores the details of each difference.

## GUI Design

### Overview

The interface is built with Tkinter and acts as the presentation layer of the game.

Its main responsibilities are:
- displaying the original and modified images side by side,
- capturing clicks on the modified image,
- showing remaining differences and mistakes,
- providing buttons for loading a new image, revealing differences, and quitting.

The GUI does not contain game rules; it delegates that work to 'GameLogic'.

### Layout

The window is organized into three areas:

- **Title area** for the game heading.
- **Image area** for the original and modified images.
- **Control panel** for counters and buttons.

The modified image is the only one that responds to clicks.

### Interaction Flow

1. The player clicks on the modified image.
2. The GUI sends the click coordinates to 'GameLogic'.
3. If a difference is found, the GUI draws a red circle around it.
4. If the reveal option is used, unfound differences are marked with blue circles.
5. The interface updates the remaining differences and mistake count after each action.

### Design Benefits

This structure keeps the program clear, maintainable, and easy to extend. It also supports clean separation of concerns and matches the assignment requirements well.