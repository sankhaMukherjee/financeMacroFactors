import logging
import requests
from bs4 import BeautifulSoup


logBase = 'financeMacroFactors.companies.marketWatchData.'

def convertNumberMW(number):
    '''translate a string to a potential number
    Marketwatch contains numbers within HTML tables as text. The
    text is present in a form that is specific to Marketwatch and
    thus cannot be easily translated. This function will help with
    the translation.
    
    Parameters
    ----------
    number : str
        A string that should be converted into a number
    
    Returns
    -------
    float or str
        If the correct translation was performed, then this is going
        to return a floating point number representing the number. 
        Otherwise, it will return the original string.
    '''

    logger = logging.getLogger(logBase + 'convertNumberMW')
    
    try:
        if number == '-':
            return 0

        number = number.replace(',', '')
        sign = 1
        # This is a negative number
        if number.startswith('(') and number.endswith(')'):
            number = number[1:-1]
            sign = -1
            
        multiplier = 1
        if number.endswith('T'):
            number = number[:-1]
            multiplier = 1e12
        if number.endswith('B'):
            number = number[:-1]
            multiplier = 1e9
        if number.endswith('M'):
            number = number[:-1]
            multiplier = 1e6
        if number.endswith('K'):
            number = number[:-1]
            multiplier = 1e3
        if number.endswith('%'):
            number = number[:-1]
            multiplier = 1e-2
        
        number = float(number) * multiplier * sign
        return number
    except Exception as e:
        logger.error(f'Unable to convert {number}: {e}', file=sys.stderr)
        return number
    
    return number

def getDataFromMWURL(url, convert=True):
    '''Get data from a mamrketwatch URL page
    Given a particular URL, this function is going to return
    all the data that is associated with the particular URL.
    Typically the results are present in multiple tables. The
    data from all the tables are combined into a single table
    before it is returned. Typically, the headers remain 
    unchained.
    Note that this function should not be used directly, but
    rather through the use of other functions present within
    this module, sinnce this function doees not check whether
    this url actually exists or not.
    In the case of an error, an empty list is returned.
    
    Parameters
    ----------
    url : str
        This should be a Markektwatch URL that deals with
        proper stock information.
    convert : bool, optional
        determine whether numbers represented as strings should
        be coonverted into numbers, by default ``True``.
    
    Returns
    -------
    list of list
        The data present within the tables within the supplied
        URL.
    '''
    
    logger = logging.getLogger(logBase + 'getDataFromMWURL')
    
    try:
        data = requests.get(url)
        html_data = data.text
        page_content = BeautifulSoup(html_data, 'lxml')
        
        allData = []

        tables = page_content.find_all('table')

        for tNo, table in enumerate(tables):
            for i, row in enumerate(table.find_all('tr')):
                if (i == 0) and (tNo == 0):
                    header = [d.get_text().strip() for d in row.find_all('th')][:-1]
                    allData.append(header)

                data = [d.get_text().strip() for d in row.find_all('td')][:-1]

                if len(data) == 0:
                    continue
                if data[0].endswith('Growth') or data[0].endswith('Margin'):
                    continue

                if convert:
                    data = data[:1] + [convertNumberMW(d) for d in data[1:]]
                allData.append(data)
                
        return allData
    except Exception as e:
        logger.error(f'Unable to obtain the data from the URL [{url}]: {e}')
        return []

def getTickerFundamentalDataMW(ticker, convert=True):
    '''get Valuation data for the supplied ticker
    This is going to get all financials from marketwatch, including the income statement,
    the balance sheet, and the cash-flow sheet for the lat few quarters and years separately
    and return the result in a dictionary. In case of any error is made, this is going to
    return an empty dictionary.
    
    Parameters
    ----------
    ticker : str
        A valid ticker for downloading company data.
    convert : bool, optional
        Used to convert numeric data present in the webpage as a string back into a 
        number, by default ``True``. Set this to False if you want to save the data
        from the internet as CSV files.
    
    Returns
    -------
    dict
        financial data associated with a particular stock
    '''

    logger = logging.getLogger(logBase + 'getTickerFundamentalDataMW')

    urls = {
        'IncomeStatement'       : 'https://www.marketwatch.com/investing/stock/{}/financials',
        'IncomeStatementQuarter': 'https://www.marketwatch.com/investing/stock/{}/financials/income/quarter',
        'BalanceSheet'          : 'https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet',
        'BalanceSheetQuarter'   : 'https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet/quarter',
        'CashFlow'              : 'https://www.marketwatch.com/investing/stock/{}/financials/cash-flow',
        'CashFlowQuarter'       : 'https://www.marketwatch.com/investing/stock/{}/financials/cash-flow/quarter',
    }

    allResults = {}

    try:
        for urlKey in urls:
            url = urls[urlKey].format(ticker)
            allData = getDataFromMWURL(url, convert=convert)

            allResults[urlKey] = allData

    except Exception as e:
        logger.error(f'Unable to generate information for ticker [{ticker}]: {e}')
        return {}
        

    return allResults


