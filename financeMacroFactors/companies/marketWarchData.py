import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt 
from datetime import timedelta as tDel


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

monthMaps = {
    'January'    : 1  , 
    'February'   : 2  , 
    'March'      : 3  , 
    'April'      : 4  , 
    'May'        : 5  , 
    'June'       : 6  , 
    'July'       : 7  , 
    'August'     : 8  , 
    'September'  : 9  , 
    'October'    : 10 ,  
    'November'   : 11 ,  
    'December'   : 12 }

miniMonthMaps = {
    'Jan'  : 1  , 
    'Feb'  : 2  , 
    'Mar'  : 3  , 
    'Apr'  : 4  , 
    'May'  : 5  , 
    'Jun'  : 6  , 
    'Jul'  : 7  , 
    'Aug'  : 8  , 
    'Sep'  : 9  , 
    'Oct'  : 10 ,  
    'Nov'  : 11 ,  
    'Dec'  : 12 }

def convertToDates(yearInfo):
    'Internal function - do not use'
    
    logger = logging.getLogger(logBase + 'convertToDates')

    try:
        startingMonth = yearInfo[0][0].split('.')[0].split()[-1].split('-')[0]
        startingMonth = monthMaps[startingMonth] # Convert month to an integer

        # Sometimes in marketwatch data, the year is an empty string. We
        # Need to address that. This typically happens when the data is not
        # available on a aprticular year ...
        years = [(int(y) if y!='' else -1) for y in yearInfo[0][1:]]
        dates = [((dt(y, startingMonth, 1)- tDel(1)  ) if y > 1900 else None)  for y in years ]
    except Exception as e:
        print(f'Unable to convert {yearInfo} to a date: {e}')
        return None
            
    return dates

def extractYearlyData(info, toExtract='EPS (Diluted)'):
    '''extract required data from a given list of items

    This is a utility function that will allow one to easily
    extract any informamtion from the MWData that you have already
    downloaded. For example, from the "IncomeStatement" It is 
    possible to extract information about the "Earnings per Share".

    It is important to know that the information provided should
    not ge generated by the user, but rather through the function
    ``getTickerFundamentalDataMW()`` with the parameter ``convert``
    set to ``False``.
    

    Parameters
    ----------
    info : list
        List containing yearly information about a particular company.
    toExtract : str, optional
        Information that you wish to extract, by default 'EPS (Diluted)'

    Returns
    -------
    list
        returns a list of tuples containing the dates and the
        values corresponding to the information requested
    '''
    
    logger = logging.getLogger(logBase + 'extractYearlyData')

    try:
        if info == []:
            logger.error('Empty input provided. Unable to generate output. Empty list returned')
            return []

        dates = convertToDates(info)
        if dates is None:
            logger.error(f'Unable to extract date information. Empty list returned.')
            return []


        data = [d[1:] for d in info if d[0]==toExtract]

        if data == []:
            availableVariables = '[' + ']['.join([d[0] for d in info]) + ']'
            logger.error(f'Unable to extract [{toExtract}] from the data')
            logger.error(f'Check to see whether the information you provided is correct')
            logger.error(f'Available variables are: {availableVariables}')
            return []
        
        # In case there is a descripency in the dates such that a particular
        # date is 0, this is going to exclude that date ...
        data = data[0]
        dates, data = zip(*[(d1, d2) for d1, d2 in  zip(dates, data) if d1 is not None])
        data = list(zip(dates, data))
        
        return data

    except Exception as e:
        logger.error(f'Unable to extract requested data from {info}: {e}')
        return []

def convertToMonths(info):
    'Internal function - do not use'
    
    logger = logging.getLogger(logBase + 'convertToMonths')

    try:

        dates = []
        for d in info[0][1:]:

            if d == '':
                dates.append(None)
                continue

            d, m, y = d.split('-')
            d, y = int(d), int(y)
            m = miniMonthMaps[m]
            
            dates.append( dt(y, m, d) )
    except Exception as e:
        logger.error(f'Unable to convert to month {info}: {e}')
        return None

    return dates

def extractQuarterlyData(info, toExtract='EPS (Diluted)'):
    '''extract required data from a given list of items

    This is a utility function that will allow one to easily
    extract any informamtion from the MWData that you have already
    downloaded. For example, from the "IncomeStatement" It is 
    possible to extract information about the "Earnings per Share".

    It is important to know that the information provided should
    not ge generated by the user, but rather through the function
    ``getTickerFundamentalDataMW()`` with the parameter ``convert``
    set to ``False``.
    

    Parameters
    ----------
    info : list
        List containing quarterly information about a particular company.
    toExtract : str, optional
        Information that you wish to extract, by default 'EPS (Diluted)'

    Returns
    -------
    list
        returns a list of tuples containing the dates and the
        values corresponding to the information requested
    '''

    logger = logging.getLogger(logBase + 'extractQuarterlyData')
    
    try:
        if info == []:
            logger.error(f'Empty data provided. An empty list is returned')
            return []

        dates = convertToMonths(info)
        if dates is None:
            logger.error(f'Unable to extract date information. Empty list returned.')
            return []

        data = [d[1:] for d in info if d[0]==toExtract]
        if data == []:
            availableVariables = '[' + ']['.join([d[0] for d in info]) + ']'
            logger.error(f'Unable to extract [{toExtract}] from the data')
            logger.error(f'Check to see whether the information you provided is correct')
            logger.error(f'Available variables are: {availableVariables}')
            return []
        
        
        data = data[0]
        dates, data = zip(*[(d1, d2) for d1, d2 in  zip(dates, data) if d1 is not None])
        data = list(zip(dates, data))

        return data
    
    except Exception as e:
        logger.error(f'Unable to extract requested data: {e}')
        return []


    return []

