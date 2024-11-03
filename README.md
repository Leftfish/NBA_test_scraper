A horribly simple tool that scrapes (but gently, no more than 18-19 requests per minute, as required [here](https://www.sports-reference.com/bot-traffic.html)) data from Basketball Reference.

Everything inspired by a friend who was curious to see how well the advantage in 3P field goalds predicts wins in the NBA these days.

For now:
* data_updater.py fetches data and saves them to JSON
* data_analysis.py for now just checks how often teams with more 3PA, 3PM, 3P%, FTA or FTM win.

Note: "more" means "greater than", so ties are not included. 