from pandas import read_csv
import numpy as np
from pandas import DataFrame as df
import os, csv
from itertools import zip_longest

path = "Janči"

sex = "M"  # F/M
gamer = True

entries = os.listdir(path)


def load_information(path):
    data = read_csv(path, delimiter=',',
                    decimal=".")
    reaction_time = data.iloc[:, 0]
    ambulance = data.iloc[:, 1]
    start_stimulus = data.iloc[:, 2]
    detected_activity = data.iloc[:3]
    return reaction_time, ambulance, start_stimulus, detected_activity


def load_concrete_reaction_times(path):
    data = read_csv(path, delimiter=',',
                    decimal=".")
    sem = data.loc[data['Ambulance'] == False]
    change_to_green = sem[::2]
    change_to_green = change_to_green.loc[change_to_green["Reaction time"] > 0.15]
    change_to_red = sem[1::2]
    change_to_red = change_to_red[change_to_red["Reaction time"] > 0.15]
    display_ambulance = data.loc[data['Ambulance'] == True]
    display_ambulance = display_ambulance.loc[display_ambulance["Reaction time"] > 0.15]
    return change_to_green, change_to_red, display_ambulance


mean_each_game = []

mean_changed_green = []
mean_changed_red = []
mean_displayed_ambulance = []

game = 0

for signal in entries:
    file = signal[:-4]
    if signal[-3:] != "csv":
        pass
    elif file[-11:] == "whole_data_":
        game = game + 1
        path_signal = path + os.sep + signal
        reaction_time, ambulance, start_stimulus, detected_activity = load_information(path_signal)
        change_to_green, change_to_red, display_ambulance = load_concrete_reaction_times(path_signal)

        mean_each_game.append(
            np.mean(reaction_time[np.array(np.where(reaction_time > 0.15))[0]]))  # under 0.15 is not physical

        # green
        if change_to_green.shape[0] > 0:
            gr = np.mean(change_to_green.iloc[:, 0])  # reaction times
        else:
            gr = None
        mean_changed_green.append(gr)
        # red
        if change_to_red.shape[0] > 0:
            red = np.mean(change_to_red.iloc[:, 0])  # reaction times
        else:
            red = None
        mean_changed_red.append(red)
        # ambulance
        if display_ambulance.shape[0] > 0:
            mean_displayed_ambulance.append(np.mean(display_ambulance.iloc[:, 0]))
        else:
            mean_displayed_ambulance.append(None)

# save data
game = [1, 2, 3, 4, 5]
data = [game, mean_each_game, mean_changed_green, mean_changed_red, mean_displayed_ambulance]
with open(path + os.sep + "results.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Game", "Mean", "Green", "Red", "Ambulance"])
    for values in zip_longest(*data):
        writer.writerow(values)

# calculate mean throw all games
# remove None: [i for i in a if i]
mean_all_games = np.mean(mean_each_game)
mean_all_games = round(mean_all_games, 2)
mean_green = np.mean(mean_changed_green)
mean_green = round(mean_green, 2)

mean_changed_red = [i for i in mean_changed_red if i]
if len(mean_changed_red):
    mean_red = np.mean(mean_changed_red)
    mean_red = round(mean_red, 2)
else:
    mean_red = np.nan

mean_displayed_ambulance = [i for i in mean_displayed_ambulance if i]
if len(mean_displayed_ambulance) > 0:
    mean_ambulance = np.mean(mean_displayed_ambulance)
    mean_ambulance = round(mean_ambulance, 2)
else:
    mean_ambulance = np.nan

# add user to table
user_data = [path, sex, gamer, mean_all_games, round(mean_each_game[0], 2), round(mean_each_game[1], 2), round(mean_each_game[2], 2),
             round(mean_each_game[3], 2), round(mean_each_game[4], 2), mean_green, mean_red, mean_ambulance]

title = "vysledky.csv"
if not os.path.isfile(title):
    with open(title, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name","Sex", "Gamer", "Mean", "First game", "Second game", "Third game",
                         "Fourth game", "Fifth game", "On green", "On red", "On ambulance"])
        writer.writerow(user_data)
else:
    with open(title, 'a+', newline='') as write_obj:
        writer = csv.writer(write_obj)
        writer.writerow(user_data)
