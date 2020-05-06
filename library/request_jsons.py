def get_json_all(time=None, limit=1000, up=300):
    return '''
    {"filter":
        [{"left":"close",
        "operation":"nempty"},
        {"left":"type",
        "operation":"in_range",
        "right":["stock","dr","fund"]},
        {"left":"subtype",
        "operation":"in_range",
        "right":["common","","etf","unit","mutual","money","reit","trust"]}],
        "options":{"lang":"en"},
        "symbols":{"query":{"types":[]},"tickers":[]},
        "columns":["name","close","Recommend.All%s","Recommend.Other%s","Recommend.MA%s"],
        "sort":{"sortBy":"close","sortOrder":"asc"},"range":[%d,%d]}
    ''' % (f'|time' if time else '',
           f'|time' if time else '',
           f'|time' if time else '',
           up,
           limit)

def get_json_by_ticker(ticker, time=None):
    return '''
    {"symbols":
        {"tickers":["MOEX:%s"],
        "query":{"types":[]}},
        "columns":["Recommend.All%s","Recommend.Other%s","Recommend.MA%s"]}
    ''' % (ticker,
           f'|time' if time else '',
           f'|time' if time else '',
           f'|time' if time else '')
