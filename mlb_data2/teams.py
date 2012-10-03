"""

"""

from database import db

_localCache = {}

class Team(object):
	def __init__(self, code, name, location, subreddit, tv_stations, radio_stations, schedule_code, league, division, mlb_id, timezone):
		self.code = code
		self.name = name
		self.location = location
		self.subreddit = subreddit
		self.tv_stations = tv_stations
		self.radio_stations = radio_stations
		self.schedule_code = schedule_code
		self.league = league
		self.division = division
		self.mlb_id = mlb_id
		self.timezone = timezone

team_matching = {
	"ARI": ["diamondbacks", "diamondback", "dbacks", "dback", "arizona", "az"],
	"ATL": ["braves", "brave", "atlanta"],
	"BAL": ["orioles", "oriole", "baltimore"],
	"BOS": ["red sox", "boston", "bosox"],
	"CHC": ["cubs", "cub", "chicago cubs", "chicago cub", "chn"],
	"CIN": ["reds", "red", "cincinnati"],
	"CLE": ["indians", "indian", "cleveland"],
	"COL": ["rockies", "rockie", "colorado"],
	"CWS": ["white sox", "chicago white sox", "cha"],
	"DET": ["tigers", "tiger", "detroit"],
	"HOU": ["astros", "astro", "houston"],
	"KC":  ["royals", "royal", "kansas city", "kansas", "kca"],
	"LAA": ["angels", "angel", "anaheim", "ana", "los angeles angel", "los angeles angels", "la angels", "la angel", "laaa", "los angeles angels of anaheim"],
	"LAD": ["dodgers", "dodger", "los angeles", "la", "los angeles dodgers", "los angeles dodger", "la dodger", "la dodgers", "lan"],
	"MIA": ["marlins", "marlin", "miami", "florida", "flo"],
	"MIL": ["brewers", "brewer", "milwaukee"],
	"MIN": ["twins", "twin", "minnesota"],
	"NYM": ["mets", "met", "new york mets", "new york met", "nyn"],
	"NYY": ["yankees", "yankee", "new york yankees", "new york yankee", "nya"],
	"OAK": ["athletics", "athletic", "as", "oakland"],
	"PHI": ["phillies", "phillie", "philly", "philadelphia"],
	"PIT": ["pirates", "pirate", "buccos", "bucco", "pittsburgh"],
	"SD":  ["padres", "padre", "san diego", "sdn"],
	"SEA": ["mariners", "mariner", "seattle"],
	"SF":  ["giants", "giant", "san fran", "san francisco", "gigantes", "sfn"],
	"STL": ["cardinals", "cardinal", "st louis", "st. louis", "sln"],
	"TB":  ["rays", "ray", "devil rays", "devil ray", "tampa", "tampa bay", "tba"],
	"TEX": ["rangers", "ranger", "texas"],
	"TOR": ["blue jays", "blue jay", "bluejays", "bluejay", "jays", "jay", "toronto"],
	"WSH": ["nationals", "natinals", "national", "washington", "was"]
}

divisions = {
	"al": {
		"east": ["BAL", "BOS", "NYY", "TB", "TOR"],
		"central": ["CLE", "CWS", "DET", "KC", "MIN"],
		"west": ["LAA", "OAK", "SEA", "TEX"]
	},
	"nl": {
		"east": ["ATL", "MIA", "NYM", "PHI", "WSH"],
		"central": ["CHC", "CIN", "HOU", "MIL", "PIT", "STL"],
		"west": ["ARI", "COL", "LAD", "SD", "SF"]
	}
}

"""
Find a team's 2/3-letter code from a few common names (i.e. "braves", "brave", "atlanta" all point to "ATL")
"""
def getTeam(name):
	if isinstance(name, Team):
		_localCache[name.code] = name
		return name

	if name in _localCache:
		return _localCache[name]

	db.execute("SELECT * FROM teams WHERE code = ?", (name,))
	row = db.fetchone()

	if row is not None:
		_localCache[row["code"]] = Team(*row)
		return _localCache[row["code"]]

	name = name.lower()

	for code in team_matching:
		if name in team_matching[code]:
			return getTeam(code)

	return None