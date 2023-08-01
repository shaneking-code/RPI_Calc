"""
gameslog = [
    { "Winner" : "UCONN", "Loser" : "Kansas", "Location" : "UCONN"},
    { "Winner" : "UCONN", "Loser" : "Duke", "Location" : "UCONN"},
    { "Winner" : "UCONN", "Loser" : "Wisconsin", "Location" : "Wisconsin"},
    { "Winner" : "Kansas", "Loser" : "UCONN", "Location" : "Kansas"},
    { "Winner" : "Duke", "Loser" : "Wisconsin", "Location" : "Duke"},
    { "Winner" : "Kansas", "Loser" : "Wisconsin", "Location" : "Wisconsin"}
]
"""

# Calculate RPI of "team"
def calc_rpi(team,
             games,
             location_matters=False,
             mode="normal",
             mode_high_weight=1,
             mode_low_weight=1,
             weight_wp=0.25,
             weight_opwp=0.50,
             weight_opopwp=0.25):

    wp     = get_wp(team, games, location_matters, mode, mode_high_weight, mode_low_weight)
    opwp   = get_opwp(team, games)
    opopwp = get_opopwp(team, games)

    return (weight_wp * wp) + (weight_opwp * opwp) + (weight_opopwp * opopwp)

# Calculate winning percentage of "team"
def get_wp(team,
           games,
           location_matters=False,
           mode="normal",
           mode_high_weight=1,
           mode_low_weight=1):
    
    wins = losses = 0
    home_win_weight = home_loss_weight = away_win_weight = away_loss_weight = 1

    if mode == "baseball":
        home_win_weight = away_loss_weight = 0.7
        home_loss_weight = away_win_weight = 1.3
    if mode == "basketball":
        home_win_weight = away_loss_weight = 0.6
        home_loss_weight = away_win_weight = 1.4
    if mode == "custom":
        home_win_weight = away_loss_weight = mode_low_weight
        home_loss_weight = away_win_weight = mode_high_weight
 
    if location_matters:
        for game in games:
            if game["Winner"] == team and game["Location"] == team:
                wins += home_win_weight
            if game["Winner"] == team and game["Location"] != team:
                wins += away_win_weight
            if game["Loser"] == team and game["Location"] == team:
                losses += home_loss_weight
            if game["Loser"] == team and game["Location"] != team:
                losses += away_loss_weight
    else:
        for game in games:
            if game["Winner"] == team:
                wins += 1
            if game["Loser"] == team:
                losses += 1

    if wins == 0 and losses == 0:
        return 0
    return wins / (wins + losses)

# Get the winning percentage of "team" without games against "opponent"
def get_wp_minus_team(team, opponent, games):

    games_without_opponent = []

    for game in games:
        if game["Winner"] != opponent and game["Loser"] != opponent:
            games_without_opponent.append(game)

    return get_wp(team, games_without_opponent)

# Calculate "team"s opponents winning percentage sans "team"
def get_opwp(team, games):

    opponent_schedule = []

    for game in games:
        if game["Winner"] == team:
            opponent = game["Loser"]
            opponent_schedule.append(get_wp_minus_team(opponent, team, games))
        if game["Loser"] == team:
            opponent = game["Winner"]
            opponent_schedule.append(get_wp_minus_team(opponent, team, games))

    return sum(opponent_schedule) / len(opponent_schedule)

# Calculate "team"s opponents opponents winning percentage sans "team"
def get_opopwp(team, games):

    opponents = []

    for game in games:
        if game["Winner"] == team:
            opponents.append(game["Loser"])
        if game["Loser"] == team:
            opponents.append(game["Winner"])

    opponents_opwp = []

    for opponent in opponents:
        opponents_opwp.append(get_opwp(opponent,games))

    return sum(opponents_opwp) / len(opponents_opwp)

"""
teams = ["UCONN", "Kansas", "Duke", "Wisconsin"]
location_matters_test = True
mode = "normal"
mode_high_weight = 1.3
mode_low_weight = 0.7

for team in teams:
    team_wp = get_wp(team, gameslog, location_matters_test, mode)
    team_opwp = get_opwp(team, gameslog)
    team_opopwp = get_opopwp(team, gameslog)
    team_rpi = calc_rpi(team, gameslog, location_matters_test, mode, mode_high_weight, mode_low_weight)
    print(f"{team}'s winning percentage is: {team_wp:.4f}")
    print(f"{team}'s opponents winning percentage is: {team_opwp:.4f}")
    print(f"{team}'s opponents opponents winning percentage is {team_opopwp:.4f}")
    print(f"{team}'s RPI is: {team_rpi:.4f}\n")
"""