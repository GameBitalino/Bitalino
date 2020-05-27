from pandas import read_csv
import numpy as np
from pandas import DataFrame as df
import pandas as pd
import os, csv
import matplotlib.pyplot as plt

csfont = {'fontname': 'Times New Roman'}
plt.rcParams["font.family"] = "Times New Roman"
SMALL_SIZE = 14
MEDIUM_SIZE = 16
BIGGER_SIZE = 18
TITLE_SIZE = 20
plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)

path = os.getcwd() + r"\vysledky.csv"
data = pd.read_csv(path, encoding='cp1252')

names = data.iloc[:, 0]
sex = data.iloc[:, 1]
gamer = data.iloc[:, 2]
mean_games = data.iloc[:, 3]
first = data.iloc[:, 4]
second = data.iloc[:, 5]
third = data.iloc[:, 6]
fourth = data.iloc[:, 7]
fifth = data.iloc[:, 8]
on_green = data.iloc[:, 9]
on_red = data.iloc[:, 10]
on_ambulance = data.iloc[:, 11]

men_mean = mean_games.loc[sex == "M"]
women_mean = mean_games.loc[sex == "F"]

sex = [men_mean, women_mean]
fig = plt.figure(1)
plt.boxplot(sex)
plt.title("Průměrná reakční doba ve hře", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['Muži', 'Ženy'])
plt.xlabel("Pohlaví")
plt.ylabel("Reakční doba [s]")
plt.savefig('Pohlavi.png', dpi=300)
plt.show()

# gamer
gamers = data["Mean"][(data["Gamer"] == True)]
no_gamers = data["Mean"][(data["Gamer"] == False)]

gaming = [gamers, no_gamers]
plt.boxplot(gaming)
plt.title("Průměrná reakční doba ve hře", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['ANO', 'NE'])
plt.xlabel("Hráč počítačových her")
plt.ylabel("Reakční doba [s]")
plt.savefig('Hraci.png', dpi=300)
plt.show()

men_gamers = data["Mean"][(data["Gamer"] == True) & (data["Sex"] == "M")]
men_no_gamers = data["Mean"][(data["Gamer"] == False) & (data["Sex"] == "M")]

gaming = [men_gamers, men_no_gamers]
plt.boxplot(gaming)
plt.title("Průměrná reakční doba ve hře - muži", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['ANO', 'NE'])
plt.xlabel("Hráč počítačových her")
plt.ylabel("Reakční doba [s]")
plt.savefig('Hraci_muzi.png', dpi=300)
plt.show()

women_gamers = data["Mean"][(data["Gamer"] == True) & (data["Sex"] == "F")]
women_no_gamers = data["Mean"][(data["Gamer"] == False) & (data["Sex"] == "F")]

gaming = [women_gamers, women_no_gamers]
plt.boxplot(gaming)
plt.title("Průměrná reakční doba ve hře - ženy", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['ANO', 'NE'])
plt.xlabel("Hráč počítačových her")
plt.ylabel("Reakční doba [s]")
plt.savefig('Hraci_zeny.png', dpi=300)
plt.show()

mean_red_green = []
for i in range(len(on_green)):
    mean_red_green.append(on_green[i])
    mean_red_green.append(on_red[i])
item = [mean_red_green, on_ambulance]
plt.boxplot(item)
plt.title("Průměrná reakční doba pro rozdílné podněty", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['Změna barvy', 'Zobrazení vozu záchranné služby'])
plt.xlabel("Druh podnětu")
plt.ylabel("Reakční doba [s]")
plt.savefig('podnety.png', dpi=300)
plt.show()

color = [on_green, on_red]
plt.boxplot(color)
plt.title("Průměrná reakční doba při změně barvy semaforu", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['Na zelenou', 'Na červenou'])
plt.xlabel("Změna barvy")
plt.ylabel("Reakční doba [s]")
# plt.savefig('barva.png', dpi=300)
plt.show()

# nejlepší

compare = [first, second, third, fourth, fifth]
plt.boxplot(compare)
plt.title("Průměrná reakční doba v jedtnotlivých hrách", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2, 3, 4, 5], ['První', 'Druhá', 'Třetí', 'Čtvrtá', 'Pátá'])
plt.xlabel("Pořadí hry")
plt.ylabel("Reakční doba [s]")
plt.savefig('poradi.png', dpi=300)
plt.show()

# zlepšení
gamers_first_game = data["First game"][(data["Gamer"] == True)]
gamers_fifth_game = data["Fifth game"][(data["Gamer"] == True)]
no_gamers_first_game = data["First game"][(data["Gamer"] == False)]
no_gamers_fifth_game = data["Fifth game"][(data["Gamer"] == False)]
diff_gamers = gamers_first_game - gamers_fifth_game
diff_no_gamers = no_gamers_first_game - no_gamers_fifth_game
compare = [diff_gamers, diff_no_gamers]

plt.boxplot(compare)
plt.title("Průměrné zlepšení reakční doby", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['ANO', 'NE'])
plt.xlabel("Hráč počítačových her")
plt.ylabel("Zlepšení reakčních časů [s]")
plt.savefig('zlepseni.png', dpi=300)
plt.show()


# hraci - muzi vs zeny
gamers_men = data["Mean"][(data["Gamer"] == True) & (data["Sex"] == "M")]
gamers_women = data["Mean"][(data["Gamer"] == True) & (data["Sex"] == "F")]

gaming = [gamers_men, gamers_women]
plt.boxplot(gaming)
plt.title("Průměrná reakční doba ve hře - jedinci hrající hry", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['Muži', 'Ženy'])
plt.xlabel("Pohlaví")
plt.ylabel("Reakční doba [s]")
plt.savefig('gamers.png', dpi=300)
plt.show()



# nehraci - muzi vs zeny
no_gamers_men = data["Mean"][(data["Gamer"] == False) & (data["Sex"] == "M")]
no_gamers_women = data["Mean"][(data["Gamer"] == False) & (data["Sex"] == "F")]

gaming = [no_gamers_men, no_gamers_women]
plt.boxplot(gaming)
plt.title("Průměrná reakční doba ve hře - jedinci nehrající hry", fontweight='bold', fontsize=TITLE_SIZE)
plt.xticks([1, 2], ['Muži', 'Ženy'])
plt.xlabel("Pohlaví")
plt.ylabel("Reakční doba [s]")
plt.savefig('nogamers.png', dpi=300)
plt.show()
