import requests
from pprint import pprint as pp 

API_KEY = 'b186fae5dec7f020a3166f973329902c'
SPORT = 'soccer_epl' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
REGIONS = 'uk' # uk | us | eu | au. Multiple can be specified if comma delimited
MARKETS = 'h2h,spreads' # h2h | spreads | totals. Multiple can be specified if comma delimited
ODDS_FORMAT = 'decimal' # decimal | american
DATE_FORMAT = 'iso' # iso | unix

def get_all_sports():
    """
    Fetches all sports from the Odds API.
    """
    return requests.get(
        'https://api.the-odds-api.com/v4/sports',
        params={'api_key': API_KEY}
    )

def get_odds(sport=SPORT, regions=REGIONS, markets=MARKETS):
    """
    Returns a list of upcoming and live games with recent odds for a given sport, region and market

    :param sport: The sport key (e.g., 'upcoming', 'soccer_epl', etc.)
    :param regions: Comma-separated list of regions (e.g., 'uk,us,eu,au')
    :param markets: Optional, Comma-separated list of markets (e.g., 'h2h,spreads')
    """
    return requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
        params={
            'api_key': API_KEY,
            'markets': markets,
            'regions': regions,
        }
    )

def get_scores(sport=SPORT, days_from=1):
    """
    Returns a list of scores for a given sport and number of days from today.
    Live and recently completed games contain scores. 
    Games from up to 3 days ago can be returned using the daysFrom parameter. 
    Live scores update approximately every 30 seconds.

    :param sport: The sport key (e.g., 'upcoming', 'soccer_epl', etc.)
    :param days_from: Optional, number of days from today to include scores for (default is 1)
    """
    return requests.get(
        f'https://api.the-odds-api.com/v4/sports/{sport}/scores',
        params={
            'api_key': API_KEY,
            'daysFrom': days_from,
        }
    )

    # Check the usage quota
    # print('Remaining requests', odds_response.headers['x-requests-remaining'])
    # print('Used requests', odds_response.headers['x-requests-used'])

odds_data = get_odds().json()
scores_data = get_scores().json()