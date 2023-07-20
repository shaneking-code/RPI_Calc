import random
import time
from rpi import calc_rpi

gameslog = []
teams = ["Diamondbacks",
         "Braves",
         "Orioles",
         "Red Sox",
         "Cubs",
         "White Sox",
         "Reds",
         "Guardians",
         "Rockies",
         "Tigers",
         "Astros",
         "Royals",
         "Angels",
         "Dodgers",
         "Marlins",
         "Brewers",
         "Twins",
         "Mets",
         "Yankees",
         "Athletics",
         "Phillies",
         "Pirates",
         "Padres",
         "Giants",
         "Mariners",
         "Cardinals",
         "Rays",
         "Rangers",
         "Blue Jays",
         "Nationals"]

# test the RPI calculation with "iteration" number of games
def test(iterations):
    for i in range(iterations):

        # select teams
        team_one = random.choice(teams)
        teams_without_team_one = [team for team in teams if team != team_one]
        team_two = random.choice(teams_without_team_one)

        # decide who will be the home team
        selector = []
        selector.append(team_one)
        selector.append(team_two)

        # create game result to be appended
        matchup = {
            "Winner" : team_one,
            "Loser" : team_two,
            "Location" : random.choice(selector)
        }

        # add game result to gameslog
        gameslog.append(matchup)

    rpis = []
    # calculate RPIs for each team
    for team in teams:
        rpi = calc_rpi(team, gameslog, location_matters=True, mode="baseball")
        rpis.append(rpi)

    # combine teams with their RPIs and sort
    teams_with_rpis = zip(teams, rpis)
    teams_with_rpis = sorted(teams_with_rpis, key=lambda x: x[1], reverse=True)
    for team, rpi in teams_with_rpis:
        print(f"{team}'s RPI is: {rpi:.4f}")

iterations = int(input("Enter the desired number of iterations: "))
start_time = time.time()

try:
    test(iterations)
except ZeroDivisionError:
    print("Divide by zero error!")

print(f"Time elapsed: {(time.time() - start_time):.4f}")
print("Program finished")



    