import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt 
from datetime import timedelta as tDel

logBase = 'financeMacroFactors.companies.yahooData.'

def getStockDataYahoo( ticker, startDate=dt.now()-tDel(365), endDate=dt.now(), frequency='1mo', convert=True):
    '''obtains historical stock prices from Yahoo!

    Historic prices of a company as obtained form yahoo. It comprises of a list of lists.
    The first like represents the header. The data is present in the following lines. 
    Data for dividents and stock splits are removed from the list. All numerical values
    are converted to floating point numbers. If ``convert`` is set to ``True``, the dates
    are converted into a ``datetime.datetime`` object. Otherwise it is retained as a string.

    The returned data like the following:

    [['Date', 'Open', 'High', 'Low', 'Close*', 'Adj. close**', 'Volume'],
    [datetime.datetime(2020, 7, 31, 0, 0), 204.4, 205.1, 199.01, 205.01, 205.01, 51247969.0],
    [datetime.datetime(2020, 7, 1, 0, 0), 203.14, 216.38, 197.51, 205.01, 205.01, 770306200.0],
    ...
    ]

    In case there is an error, an error will be logged and an empty list will be returned.

    Parameters
    ----------
    ticker : str
        a valid sticker symbol of the company for which the data is to be obtained.
    startDate : datetime.datetime, optional
        This is the start date from which the date should be obtained, by default 
        ``dt.now()-tDel(365)``
    endDate : datetime.datetime, optional
        This is the last datetime for which the data should be obtained, 
        by default ``dt.now()``
    frequency : str, optional
        This is either ``'1d'``, ``'1wk'``, ``'1mo'``. By default this is set
        to ``'1mo'`` for an average data for a month.
    convert : bool, optional
        If this is set to ``True``, then the dates are converted into ``datetime.datetime``
        objects. Otherwise, they are kept as strings. By default, this is set to
        ``True``.

    Returns
    -------
    list of list
        Stock data as returned from Yahoo. See the description above.
    '''

    logger = logging.getLogger(logBase + 'getTickerFundamentalDataMW')

    possibleFrequencies = ['1d', '1wk', '1mo']
    if frequency not in possibleFrequencies:
        logger.error(f'Incorrect frequency supplied {frequency}. Should be one of {possibleFrequencies}')
        return []
    
    try:

        string  = f'https://sg.finance.yahoo.com/quote/{ticker}/history?'
        string += f'period1={int(startDate.timestamp())}'
        string += f'&period2={int(endDate.timestamp())}'
        string += '&interval=1mo'
        string += '&filter=history'
        string += '&frequency=1mo' 

        logger.debug(f'Attempting to obtain data from {string}')

        html_data = requests.get(string).text

        logger.debug(f'Obtained HTML data')

        page_content = BeautifulSoup(html_data, 'lxml')
        logger.debug(f'Converted to page content information')

        tables = page_content.find_all('table')
        logger.debug(f'Table informaiton generated. Starting to parse the data')

        # There is only a single table in this page
        allData = []
        for tNo, table in enumerate(tables):
            for i, row in enumerate(table.find_all('tr')):
                if (i == 0) and (tNo == 0):
                    header = [d.get_text().strip() for d in row.find_all('th')]
                    allData.append(header)


                data = [d.get_text() for d in row.find_all('td')]

                if len(data) < len(header):
                    continue
                    
                # convert the date to datetime
                if convert:
                    d, m, y = data[0].split()
                    d, m, y = int(d), miniMonthMaps[m], int(y)
                    date    = dt(y, m, d)
                    data[0] = date
                    
                data = data[:1] + [float(d.replace(',','')) for d in data[1:]]
                allData.append(data)

        logger.debug(f'A total if {len(allData)} values generated. Returning data')

        return allData

    except Exception as e:
        logger.error(f'Unable to get Stock data from Yahoo: {e}')
        return []


    return []