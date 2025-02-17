
def generate_urls_from_query(query):
    """
    Dynamically generates a list of URLs to scrape based on the user's query.
    """
    # Example mapping of keywords to URLs (can be expanded)
    keyword_to_urls = {
        'soccer': [
            'https://www.espn.com/soccer/',
            'https://www.bbc.com/sport/football',
            'https://www.goal.com/',
        ],
        'basketball': [
            'https://www.espn.com/nba/',
            'https://www.nba.com/news',
            'https://bleacherreport.com/nba',
        ],
        'tennis': [
            'https://www.atptour.com/',
            'https://www.wtatennis.com/',
            'https://tennis.com/',
        ],
        'sports betting': [
            'https://www.sportsbettingdime.com/',
            'https://www.actionnetwork.com/',
            'https://www.oddschecker.com/',
        ],
        'baseball': [
            'https://www.mlb.com/',
            'https://www.espn.com/mlb/',
            'https://bleacherreport.com/mlb',
        ],
        'football': [
            'https://www.nfl.com/',
            'https://www.espn.com/nfl/',
            'https://www.profootballfocus.com/',
        ],
        'hockey': [
            'https://www.nhl.com/',
            'https://www.espn.com/nhl/',
            'https://www.hockeybuzz.com/',
        ],
        'cricket': [
            'https://www.espncricinfo.com/',
            'https://www.cricket.com/',
            'https://www.icc-cricket.com/',
        ],
        'golf': [
            'https://www.pgatour.com/',
            'https://www.golfchannel.com/',
            'https://www.espn.com/golf/',
        ],
        'mma': [
            'https://www.ufc.com/',
            'https://www.mmafighting.com/',
            'https://www.espn.com/mma/',
        ]
    }


    # Check for keywords in the query
    query_lower = query.lower()
    urls = []
    for keyword, associated_urls in keyword_to_urls.items():
        if keyword in query_lower:
            urls.extend(associated_urls)

    # Fallback to default sports betting URLs if no keywords match
    if not urls:
        urls = ['https://www.sportsbettingdime.com/', 'https://www.actionnetwork.com/']

    return urls