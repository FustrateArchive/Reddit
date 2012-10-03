"""
"""

import urllib2, json
from datetime import datetime
from cache import load, save

"""
"""
def getStandings(teams):
	key = "standings_" + "_".join(teams)
	standings = load(key)
	now = datetime.now()

	if standings is None:
		data = urllib2.urlopen("http://mlb.mlb.com/lookup/json/named.standings_schedule_date.bam?season=%d&schedule_game_date.game_date='%s'&sit_code='h0'&league_id=103&league_id=104&all_star_sw='N'&version=2" % (now.year, now.strftime("%Y/%m/%d")))
		data = json.load(data)["standings_schedule_date"]["standings_all_date_rptr"]["standings_all_date"]

		rows = data[0]["queryResults"]["row"] + data[1]["queryResults"]["row"]

		standings = []

		for row in rows:
			found = getTeam(row["team_abbrev"])

			if found is not None and row["team_abbrev"] in teams:
				standings.append({
					"name": found.name,
					"abbrev": found.code,
					"subreddit": found.subreddit,
					"wins": int(row["w"]),
					"losses": int(row["l"]),
					"percent": row["pct"],
					"games_back": row["gb"]
				})

		standings.sort(lambda a, b: -1 if a["percent"] > b["percent"] else 1 if a["percent"] < b["percent"] else -1 if a["wins"] > b["wins"] else 1 if a["wins"] < b["wins"] else 0)

		save(key, standings, 30)

	return standings
