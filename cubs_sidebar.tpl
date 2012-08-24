# Please Do Not Post Game Results

Many of our subscribers are outside of Cubs viewing area and like to watch the games after they are played. Any posts containing direct game results will be removed. Thanks!

# Upcoming Games

Date|Time|Team|TV
:--|:--:|:--:|:--:
{% for line in calendar %}
{{- line -}}
{% endfor %}

# 2012 Current Standings

Team|W|L|PCT|GB
:--:|:--:|:--:|:--:|:--:
{%- for team in standings %}
[{{ team.location if team.name != "Cubs" else ("**" + team.location + "**") }}]({{ team.url }})|{{ team.wins }}|{{ team.losses }}|{{ team.percent }}|{{ team.games_back }}
{%- endfor %}

Last Updated {{ now|datetime("%m/%d/%y at %I:%M %p") }}

# Links

[How to get your own r/Cubs Flair](http://www.reddit.com/r/Cubs/comments/x5by8/all_rcubs_subscribers_can_now_assign_themselves/)

[Official Website](http://cubs.mlb.com/)

[Live shot outside Wrigley](http://www.earthcam.com/usa/illinois/chicago/wrigleyfield/?cam=wrigleyfield_hd)

[Official Cubs Twitter](http://twitter.com/Cubs)

[Chicago Bears Subreddit](/r/chibears)

[r/Chicago](/r/Chicago)

[r/Baseball](/r/baseball)

# Championships

## World Series Champions
1907, 1908

## NL Pennants
1876, 1880, 1881, 1882, 1885, 1886, 1906, 1907, 1908, 1910, 1918, 1929, 1932, 1935, 1938, 1945