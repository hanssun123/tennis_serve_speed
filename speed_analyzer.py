import numpy as np
import statsmodels.api as sm
# import matplotlib.pyplot as plt

COURT_LENGTH = 18 # 18 feet from baseline to service line
TOSS_OFFSET = 1 # approximating ball toss one foot into the court before impact
CAMERA_FRAMERATE = 240 # iPhone camera at max slo-mo setting
FPS_TO_MPH_CONVERSION_FACTOR = 0.681818 # 1 fps ≈ .68 mph


def main():
    x_coords = parseData("tracking_data.txt")
    impact_frame = slope_elbow(x_coords)
    exit_frame = len(x_coords) - 1

    print_ball_speed(impact_frame, exit_frame)



def parseData(file):
    data = []
    f = open(file, "r")

    for line in f:
        i, j = line.split(',')
        data.append(int(i))

    f.close()

    return data


# get elbow point based on OLS regression slope from trailing windowSize points and forward/leading windowSize points
def slope_elbow(x_coords, windowSize=5):
    t = range(len(x_coords))
    losses = [0]*(windowSize-1)
    for i in range(windowSize, len(x_coords)-windowSize):
        x_trail = x_coords[i-windowSize:i]
        t_trail = t[0:windowSize]
        t_trail = sm.add_constant(t_trail)

        x_forward = x_coords[i:i+windowSize]
        t_forward = t[0:windowSize]
        t_forward = sm.add_constant(t_forward)

        model_trail = sm.OLS(x_trail, t_trail)
        results_trail = model_trail.fit()
        _, slope_trail = results_trail.params

        model_forward = sm.OLS(x_forward, t_forward)
        results_forward = model_forward.fit()
        _, slope_forward = results_forward.params

        loss_i = slope_forward - slope_trail # biggest difference in trailing and forward slopes is where elbow is
        losses.append(loss_i)

    min_index = 0
    min_loss = float('inf')
    for i in range(len(losses)):
        if losses[i] < min_loss:
            min_loss = losses[i]
            min_index = i

    return min_index #impact point of tennis ball is at this frame
    # plt.plot(losses)
    # plt.show()


def print_ball_speed(impact_frame, exit_frame):
    print("Impact at frame " + str(impact_frame))
    print("Exit at frame " + str(exit_frame))

    num_frames = exit_frame - impact_frame
    ball_travel_distance = COURT_LENGTH - TOSS_OFFSET
    print("Total frames: " + str(num_frames))

    ball_travel_time = num_frames / CAMERA_FRAMERATE
    print("Ball travel time: " + str(round(ball_travel_time, 3)) + "s")

    ball_speed_fps = ball_travel_distance/ball_travel_time # feet, not frames per second
    ball_speed_mph = ball_speed_fps * FPS_TO_MPH_CONVERSION_FACTOR
    print("Serve speed: " + str(int(ball_speed_mph)) + "mph")


# get elbow point from minimal OLS loss point. OLS regression with penalty for small n
# slope_elbow detection algorithm works better due to variances in coordinates near elbow
def OLS_elbow(x):
    t = range(len(x))
    loss = []
    for i in range(5, len(x)): # calculate loss at increasing intervals, elbow is point of minimal loss
        x_i = x[0:i]
        t_i = t[0:i]
        t_i = sm.add_constant(t_i)

        model = sm.OLS(x_i, t_i)
        results = model.fit()
        intercept, slope = results.params
        loss.append(getOLSLoss(x_i, slope, intercept))

    min_index = 0
    min_loss = 999999999
    for i in range(len(loss)):
        if loss[i] < min_loss:
            min_loss = loss[i]
            min_index = i

    print(min_index)
    print(min_loss)

    plt.plot(loss)
    plt.show()

# Used in OLS_elbow elbow finder function, not used in slope_elbow
def getOLSLoss(data, slope, intercept):
    n = len(data)
    loss = 0
    for i in range(n):
        x_i = data[i]
        x_hat = i*slope + intercept
        loss += (x_hat - x_i)**2

    return loss/(1.07**n) # penalize loss for lower n

main()
