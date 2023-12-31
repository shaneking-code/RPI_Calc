def get_season_params(games):
    season_teams = set()
    season_games_obj = []
    for game in games:
        if game.winner not in season_teams:
            season_teams.add(game.winner)
        if game.loser not in season_teams:
            season_teams.add(game.loser)

        season_games_obj.append({
            "Winner" : game.winner.name,
            "Loser" : game.loser.name,
            "Location" : game.home_team.name
        })
    
    return season_teams, season_games_obj

# Calculate RPI of "team"
def calc_rpi(team,
             games,
             location_matters=False,
             high_weight=1,
             low_weight=1,
             weight_wp=0.25,
             weight_opwp=0.50,
             weight_opopwp=0.25):

    wp     = get_wp(team, games, location_matters, high_weight, low_weight)
    opwp   = get_opwp(team, games)
    opopwp = get_opopwp(team, games)

    return (weight_wp * wp) + (weight_opwp * opwp) + (weight_opopwp * opopwp)

# Calculate winning percentage of "team"
def get_wp(team,
           games,
           location_matters=False,
           high_weight=1,
           low_weight=1):
    
    wins = losses = 0

    home_win_weight = away_loss_weight = low_weight
    home_loss_weight = away_win_weight = high_weight
 
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
