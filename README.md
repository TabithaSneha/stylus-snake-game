# Stylus Snake Game

***

In this project, the Classic Snake Game (which uses a keypad-control) has been recreated to a Stylus-controlled Snake Game, where the movement of the snake is controlled a Stylus in front of the computer camera. 

## Results:-

# Capturing the Stylus:
![55E9AE87-3550-4678-A15E-A29106A2A55C](https://user-images.githubusercontent.com/87858655/136691892-5bca8dfa-80a8-438d-906c-59087345ff92.jpeg)

# Stylus Snake Game:
![D517F2FF-6C2D-4D6B-85D5-568D3035A089](https://user-images.githubusercontent.com/87858655/136691821-96d4a427-f87d-4ad1-8f39-536c43c6dca4.jpeg)

![65CB77AB-1F31-4B87-B393-A11804E1D857](https://user-images.githubusercontent.com/87858655/136691895-960f7807-59e2-44e3-bf22-9e36638b1d4a.jpeg)

## Methodology:-

The Stylus Snake Game was constructed using the concepts of Computer Vision from OpenCV and the game environment from Pygame.

## Structure of the Code:-

### Capturing the Stylus:
* Created a window where the user will place the Stylus within a rectangular region to capture it.
* Take the average of the HSV values of the pixels in that Region of Interest. 

### Object Tracking using HSV Colour Thresholding:

* Take each frame captured by the computer camera.
* Convert it from BGR to HSV.
* Thresholded the HSV image within a range of the captured average.
* Reduced considerable amount of noise by using Morphological Transformations of Closing and Opening.
* Applied Gaussian Blur.
* Using Contour features, we obtained the coordinates of the centroid of the object.

### Detecting the movement of the Stylus:

* The camera window is divided into 4 triangles-  marking the region of UP, DOWN, LEFT, RIGHT.
* Used a function to find out if the centroid coordinates of the Stylus lies within these regions, using the area of triangles concept.

### Creating the game environment using Pygame:

* Created the main game window, along with the snake body and also added fruits at random positions.
* Used a function to add 5 different obstacle layouts randomly to the game screen.
* Directed the motion of the snake according to the movements of the Stylus.
* Added the following game over constraints:
    * Getting out-of-bounds of the game window.
    * Touching the snake body.
    * Touching the obstacles.
* Used a Game Over function to display the final score and end the game.

## View Project:-

Click here to view the demonstration of the Stylus Snake Game.
