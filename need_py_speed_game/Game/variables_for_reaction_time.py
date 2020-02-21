import numpy as np
import math


def initialize():
    global general_stimulus
    general_stimulus = []
    global set_up_times_green_color, set_up_times_red_color, set_up_ambulance
    global react_time_red, react_time_green, react_time_ambulance
    set_up_times_green_color = []
    set_up_times_red_color = []
    react_time_red = []
    react_time_green = []
    set_up_ambulance = []
    react_time_ambulance = []


def get_stimulus_times():
    global general_stimulus
    return general_stimulus


def get_stimulus_times_variable():
    global set_up_times_green_color, set_up_times_red_color, set_up_ambulance
    return set_up_times_green_color, set_up_times_red_color, set_up_ambulance


def count_reaction_time():
    if len(react_time_green) == len(set_up_times_green_color):
        green_reaction_times = np.array(react_time_green) - np.array(set_up_times_green_color)
    elif len(react_time_green) == (len(set_up_times_green_color) - 1):
        green_reaction_times = np.array(react_time_green) - (np.array(set_up_times_green_color)[:-1])
    else:
        green_reaction_times = []
        print('different amount of detected start position - green')
        print('length set ups: ', len(set_up_times_green_color), 'length detected: ', len(react_time_green))
    green_reaction_times = [thing.total_seconds() for thing in green_reaction_times]
    if len(react_time_red) == len(set_up_times_red_color):
        red_reaction_times = np.array(react_time_red) - np.array(set_up_times_red_color)
    elif len(react_time_red) == (len(set_up_times_red_color) - 1):
        red_reaction_times = np.array(react_time_red) - (np.array(set_up_times_red_color)[:-1])
    else:
        red_reaction_times = []
        print('different amount of detected start position - red')
        print('length set ups: ', len(set_up_times_red_color), 'length detected: ', len(react_time_red))
    red_reaction_times = [thing.total_seconds() for thing in red_reaction_times]
    return green_reaction_times, red_reaction_times


def mean_reaction_time(green_reaction_times, red_reaction_times):
    if not len(green_reaction_times) == 0:
        green = np.mean(green_reaction_times)
    else:
        green = math.inf
    if not len(red_reaction_times) == 0:
        red = np.mean(red_reaction_times)
    else:
        red = math.inf
    print('Mean reaction time on green traffic lights was: ', green)
    print('Mean reaction time on red traffic lights was: ', red)
    return green, red


def best_reaction_time(green_reaction_times, red_reaction_times):
    if not len(green_reaction_times) == 0:
        green = np.min(green_reaction_times)
    else:
        green = math.inf
    if not len(red_reaction_times) == 0:
        red = np.min(red_reaction_times)
    else:
        red = math.inf
    print('Best reaction time on green traffic lights was: ', green)
    print('Best reaction time on red traffic lights was: ', red)
    return green, red
