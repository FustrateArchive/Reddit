"""

"""

# Common imports
import json, urllib2, os, time
from datetime import datetime, timedelta

# Imports from this package
from teams import getTeam
from database import db, connection, db_version

class Game(object):
	def __init__(self, gameday, start_time, away_code, home_code, status, version, date, away_r=0, away_h=0, away_e=0, home_r=0, home_h=0, home_e=0, winning_pitcher=None, losing_pitcher=None, save_pitcher=None, away_homers=[], home_homers=[]):
		self.gameday = gameday
		self.start_time = start_time
		self.home_team = getTeam(home_code)
		self.away_team = getTeam(away_code)
		self.status = status
		self.version = version
		self.home = {
			'runs': home_r,
			'hits': home_h,
			'errors': home_e
		}
		self.away = {
			'runs': away_r,
			'hits': away_h,
			'errors': away_e
		}
		self.winning_pitcher = winning_pitcher
		self.losing_pitcher = losing_pitcher
		self.save_pitcher = save_pitcher
		self.away_homers = away_homers.split("\n")
		self.home_homers = home_homers.split("\n")
		self.date = date

	def isInProgress(self):
		return self.status in ["In Progress"]

	def isOver(self):
		return self.status in ["Final", "Game Over"]

"""
"""
def getGame(team, gameday, game=1):
	db.execute("SELECT * FROM games WHERE (home_code = ? OR away_code = ?) AND date = ?", (team.code, team.code, gameday.strftime("%Y/%m/%d")))

	rows = db.fetchall()

	if len(rows) == game and rows[game-1]["version"] == db_version:
		return Game(*rows[game-1])








	try:
		file = urllib2.urlopen("http://gd2.mlb.com/components/game/mlb/year_%d/month_%02d/day_%02d/master_scoreboard.json" % (gameday.year, gameday.month, gameday.day))
	except urllib2.HTTPError:
		# There's no file for this day. Maybe future, maybe too far in the past?
		return False

	# No games today?
	try:
		games = json.load(file)["data"]["games"]["game"]
	except KeyError:
		games = []

	for game in games:
		if game["home_name_abbrev"] == team.code or game["away_name_abbrev"] == team.code:

			home_team = getTeam(game["home_name_abbrev"])
			away_team = getTeam(game["away_name_abbrev"])

			home_homers = []
			away_homers = []

			if "home_runs" in game:
				for player in game["home_runs"]["player"]:
					if player["team_code"] == home_team.schedule_code:
						home_homers.append(int(player["id"]))
					elif player["team_code"] == away_team.schedule_code:
						away_homers.append(int(player["id"]))

			data = dict(
				gameday = game["gameday"],
				start_time = game["time"],
				away_code = game["away_name_abbrev"],
				home_code = game["home_name_abbrev"],
				status = game["status"]["status"],
				version = db_version,
				away_r = game["linescore"]["r"]["away"],
				away_h = game["linescore"]["h"]["away"],
				away_e = game["linescore"]["e"]["away"],
				home_r = game["linescore"]["r"]["home"],
				home_h = game["linescore"]["h"]["home"],
				home_e = game["linescore"]["e"]["home"],
				winning_pitcher = game["winning_pitcher"]["id"] if "winning_pitcher" in game else None,
				losing_pitcher = game["losing_pitcher"]["id"] if "losing_pitcher" in game else None,
				save_pitcher = game["save_pitcher"]["id"] if "save_pitcher" in game else None,
				away_homers = "\n".join(away_homers),
				home_homers = "\n".join(home_homers),
				date = game["original_date"]
			)

			game = Game(**data)

			#db.execute("INSERT INTO games (gameday, start_time, away_code, home_code, status, version, away_r, away_h, away_e, home_r, home_h, home_e, winning_pitcher, losing_pitcher, save_pitcher, away_homers, home_homers, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", *data)

			return game

	return False

"""
"""
def getRecentGames(team, num):
	if not str(num).isdigit() or num < 1 or num > 30:
		raise Exception("Number of games must be an integer between 1 and 30")

	attempts = 0
	games = []
	gameday = datetime.now()

	while len(games) < num:
		attempts += 1

		if attempts > num * 2:
			raise Exception("Maximum number of failures exceeded.")

		game = getGame(team, gameday)
		
		if game is not False and game["status"]["status"] in ["Final", "Game Over"]:
			home = game["home_name_abbrev"] == team.code
			us = "home" if home else "away"
			them = "away" if home else "home"

			games.insert(0, {
				"date": gameday,
				"where": "vs." if home else "@",
				"against": getTeam(game[them + "_name_abbrev"]).subreddit,
				"outcome": "W" if int(game["linescore"]["r"][us]) > int(game["linescore"]["r"][them]) else "L",
			})

		gameday -= timedelta(1)

	return games