# La Liga Fantasy Marca Budget scraper

This python project is used to calculate the budget of each player in a league.

:warning: **Warning**: This scraper doesn't take into account money spent on clauses, so if you league has that feature
enabled, the budget might be inaccurate.

## Usage

1. Install requirements: `pip install -r requirements.txt`
2. Replace the variables `USERNAME`, `PASSWORD` with your credentials. :warning: **Don't commit changes that contain
your credentials!**
3. Get your league_id and replace it at the variable `LEAGUE_ID`.
   1. Access to you league at [laligafantasymarca.com](https://www.laligafantasymarca.com/)
   2. Go to `Inspect` and then to the Network section
   3. Get a request where the league_id is used and grab that id. For example, `https://api.laligafantasymarca.com/api/v3/league/YOUR_ID_IS_HERE/market/info?x-lang=es`
4. Run `python app/main.py`
5. If you have registered with using your Google account, you will have to repeat the steps in 3. in order to get a valid token. Use 
that token in the `TOKEN` variable. These tokens have a duration of 24 hours. I haven't still figured out how to do this automatically.


## TODOs

I don't want to spend too much time in this project, but if you want to do it, these are the possible betterments:
- Store the credentials safely. Possible options
  - In a file ignored by `.gitignore`
  - Read them from args or env variables
- For Google accounts, get the token automatically
- Figure out how to get the money spend on clauses.