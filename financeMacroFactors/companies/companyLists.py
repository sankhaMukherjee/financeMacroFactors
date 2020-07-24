import logging
import requests
from bs4 import BeautifulSoup

def getSNP500CompanyList():
    '''get the list of SNP 500 companies. 

    This function downloads the data from the
    `Wikipedia page
    <https://en.wikipedia.org/wiki/List_of_S%26P_500_companies>`_
    and populate a list of dictionaries. No check is performed
    on the accuracy or consistency of the result. If there is
    an error, an error message will be logged, and in that case
    an empty list will be returned.

    Returns
    -------
    list of dictionaries
        This will return a list of dictionaries, where each key
        will represent the header and each value will represent
        the associated text present within a particular table
        data element. In case of an error, an empty list will
        be returned. The logger will be used for exporting errors
        and warnings to the user.
    '''

    logger = logging.getLogger('financeMacroFactors.companies.companyLists.getSNP500CompanyList')

    try:
        
        logger.debug('Downloading data from the wikipedia page ...')
        website = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text

        logger.debug('Parsing the web data...')
        soup = BeautifulSoup(website, features="html.parser")
        companyTable = soup.find('table', {'id':'constituents'})
        rows = companyTable.find_all('tr')

        # Get the header information
        header = rows[0]
        header = [h.getText().strip() for h in header.find_all('th')]

        # Get the rest of the informaiton
        results = []
        for values in rows[1:]:
            data = {h:v.getText().strip() for h, v in zip(header, values.find_all('td'))}
            results.append( data )

        logger.debug(f'{len(results)} rows of data generated ...')

        return results

    except Exception as e:
        logger.error('Error while attempting to get S&P 500 company listings')
        logger.error(f'{e}')
        return []

    return []

    