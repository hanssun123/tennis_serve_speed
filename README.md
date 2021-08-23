# tennis_serve_speed
This project uses the CSRT tracker from the OpenCV library to track a tennis ball hit from the baseline across the first service line.

![image](https://user-images.githubusercontent.com/25471763/130425388-3e40c2c1-9653-45ad-b96b-f7550b7dabf1.png)


The point of impact is automatically determined by finding the elbow on the graph of the ball's x position over time.

![image](https://user-images.githubusercontent.com/25471763/129860575-3ce71bcd-3f1c-48c8-a8b4-bb8981373f3e.png)

Video must be recorded at 240fps (capable on newer iPhones) for accurate speed measurement, but the input video may be at any framerate as long as the total number of frames is the same (1 second video at 240fps is the same as 10 second video at 24fps, at .1x speed).

# How to Use
Install OpenCV 4, statsmodels, and NumPy.

To obtain service speed, first record a video of the service at 240fps with the closest service line directly on the left edge of the camera's field of view. The line should be parallel or close to parallel with the edge of your screen when recording. For best results, make sure that the background and the tennis racket contrast from the tennis ball's color so that the tracker can accurately follow the ball (bright green/yellow foliage behind the ball's path are not ideal). Videos taken at night as well as videos taken against a blue sky work well. Although not tested, a pink tennis ball (manufacturers make these to support breast cancer research) would probably also work well.

![image](https://user-images.githubusercontent.com/25471763/129860865-baeb59af-28d5-47f6-963b-fb72860af325.png)


Run `python opencv_ball_tracker.py -v [PATH TO VIDEO]` to open a GUI. Select the window and press `s` before the server makes impact with the ball, and select the tennis ball with the mouse by dragging a rectangle around it. Make sure the selection rectangle is as small as possible but contains the tennis ball entirely for best results.

![image](https://user-images.githubusercontent.com/25471763/129862348-bc997d73-baaa-4fba-88a2-f9139f61db79.png)

For higher speed serves, a selection rectangle elongated along the x-axis can help the tracking algorithm follow the ball better after impact since the ball has motion blur along the direction of travel after impact. However, try to estimate the left boundary of the selection rectangle as close as possible to the extent of the blur, since this is where the algorithm records the ball's coordinates to be.

![image](https://user-images.githubusercontent.com/25471763/130412579-db75b1eb-347f-404b-9791-904e5b12b69e.png)

![image](https://user-images.githubusercontent.com/25471763/130417153-094df785-6c05-41b7-8184-0b70748d4b9b.png)



Press `space` or `enter` to allow the video to finish playing, which may take a few seconds due to slower playback while tracking. After the ball exits the left side of the screen, you can press `q` to immediately exit in case the video continues for a while. A data file will be generated. Next, run `python speed_analyzer.py` to analyze the data file and obtain service speed. 

# Accuracy
Theoretically, assuming everything runs perfectly, service speeds estimated by the model can be accurate to within ±5mph up to ~125mph, after which higher framerates must be used for higher speed resolution. However, there is likely a bias between the actual and predicted service speed due to a few factors. 

First, the model assumes the server will toss the ball and make contact with it approximately 1 foot into the court. The actual contact point may vary depending on serve type, server height, player skill level, and more.

Second, due to the natural variance of tennis ball positions as well as selection rectangle size in each frame in different videos (assume the ball is traveling at the same speed, and think about what happens if the ball just manages to pass the left border when the frame is taken vs what happens if the ball manages to just clip the edge of the left border), there may be ±1 frames from the point of impact to the point of exit. At higher service speeds (100mph+), this effect is magnified because the ball travels farther in between frames and there are thus fewer frames to calculate service speed from (one additional frame of the tennis ball being on screen post impact will result in a ~5mph reduction in estimated speed at true service speeds of ~125mph). 

Finally, professional radar guns found at tennis tournaments measure the highest speed of the ball, which occurs shortly after the point of impact. This model determines the average speed of the ball across 17ft, which is likely slower than the maximum velocity achieved by the ball due to wind resistance. In addition, only the horizontal speed of the ball is taken into account, but in reality, the ball is dropping over time, resulting in a slight increase to the true service speed.
