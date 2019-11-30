import numpy as np

"""
def initialize_green_color_set_up():
    global set_up_times_green_color
    set_up_times_green_color = []


def initialize_red_color_set_up():
    global set_up_times_red_color
    set_up_times_red_color = []


def initialize_react_time_red():
    global react_time_red
    react_time_red = []


def initialize_react_time_green():
    global react_time_green
    react_time_green = []
"""


def initialize():
    global set_up_times_green_color
    set_up_times_green_color = []
    global set_up_times_red_color
    set_up_times_red_color = []
    global react_time_red
    react_time_red = []
    global react_time_green
    react_time_green = []


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
