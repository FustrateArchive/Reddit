"""

"""

import urllib2, json
from xml.dom import minidom

from database import db, connection
from teams import getTeam

class Player(object):
	def __init__(self, mlb_id, first, last, num, team):
		self.mlb_id = mlb_id
		self.first = first
		self.last = last
		self.num = num
		self.team = getTeam(team)

"""
"""
def getPlayersOnTeam(team):
	db.execute("SELECT * FROM players WHERE team = ?", (team.code,))

	rows = db.fetchall()
	players = []

	if rows is None or len(rows) < 1:
		return []

	for player in rows:
		players.append(Player(*player))

	return players

"""
"""
def getPlayer(mlb_id):
	db.execute("SELECT * FROM players WHERE mlb_id = ?", (mlb_id,))

	row = db.fetchone()

	if row is None:
		# Let's go find this player! First we need to find out what team they're on, and what that team's last game_id was
		try:
			file = urllib2.urlopen("http://gd2.mlb.com/components/game/mlb/year_2012/batters/%s.xml" % mlb_id).read()
		except urllib2.HTTPError:
			return False

		dom = minidom.parseString(file)
		game_id = dom.getElementsByTagName("batting")[0].getAttribute("game_id")

		year, month, day, meh = game_id.split("/")
		game_id = game_id.replace("-", "_").replace("/", "_")

		try:
			file = urllib2.urlopen("http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/gid_%s/batters/%s.xml" % (year, month, day, game_id, mlb_id)).read()
		except urllib2.HTTPError:
			return False

		player = minidom.parseString(file).getElementsByTagName("Player")[0]

		db.execute("INSERT OR IGNORE INTO players (mlb_id, first, last, num, team) VALUES (?, ?, ?, ?, ?)", (
			mlb_id,
			player.getAttribute("first_name"),
			player.getAttribute("last_name"),
			player.getAttribute("jersey_number"),
			getTeam(player.getAttribute("team")).code
		))

		connection.commit()

		return getPlayer(mlb_id)

	return Player(*row)

"""
"""
def deepPlayerSearch(name):
	url = "http://www.mlb.com/lookup/json/named.search_player_all.bam?sport_code='mlb'&name_part='%s%%25'&active_sw='Y'" % urllib2.urlencode(name.upper())

	try:
		file = urllib2.urlopen(url)
	except urllib2.HTTPError:
		return False

	results = json.load(file)["search_player_all"]["query_results"]

	if int(results["totalSize"]) == 1:
		player = results["row"]

		# Should probably figure out how to get their jersey number
		db.execute("INSERT OR IGNORE INTO players (mlb_id, first, last, num, team) VALUES (?, ?, ?, ?, ?)", (
			player["player_id"],
			player["name_first"],
			player["name_last"],
			0,
			player["team_abbrev"]
		))

		return getPlayer(player["player_id"])

	return False