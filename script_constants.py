ALLSCORES = ["https://www.basketball-reference.com/leagues/NBA_{}_games-october.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-november.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-december.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-january.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-february.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-march.html",
             "https://www.basketball-reference.com/leagues/NBA_{}_games-april.html"]
BOXSCORE_STR = "https://www.basketball-reference.com/boxscores/{}.html"
RE_BOXSCORE = r'<a href="\/boxscores\/(\w+)\.html">Box Score</a>'
RE_GAME = r'([A-Z]+) \(([0-9]+)\) vs ([A-Z]+) \(([0-9]+)\)'
RE_TOTALS = r'Team Totals<\/th>(.+)<\/tr>'
RE_STAT = r'data-stat="(\w+)" >([0-9]+)<\/td>'
SLEEP = 3.2
FILENAME = "gamedata{}.json"
