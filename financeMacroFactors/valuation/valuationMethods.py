import numpy as np
from scipy import interpolate


def discountedFutureEarnings(eps, discountingFactor=1.1, terminalFactor=10.0):
    '''obtain DFE Valuation

    Calculate the valuation using the Discounted Future Earnings valuation method.
    This function assumes that the input for the earnings per share relates to the
    yearly EPS values for a company for the previous N years. Ideally this value 
    is approcimately 5. If this value is less than 3, then an error will be registered
    and a value of ``None`` returned.
    
    Parameters
    ----------
    eps : earnings per share
        The last N years of data
    discountingFactor : float, optional
        The discounting factor by which future earnings shoule be discounted, by default 1.1
        which represents a 10% valuation for the future value of money
    terminalFactor : float, optional
        The value by which the final extrapolated EPS value should be multiplied so as to obtain
        a terminal value of the company, by default 10

    Returns
    -------
    float or None
        The calculated valuation of the company. If there is an error, a ``None`` will be
        returned.
    '''

    logger = logging.getLogger('financeMacroFactors.companies.companyLists.getSNP500CompanyList')

    dfeVlaue = None
    try:
        N     = len(eps)
        if N < 3:
            logger.error('Less than 3 EPS values provided.')
            logger.error('The result will not be good. A Null value will be returned.')
            return None

        xVals = np.arange(N)
        xExt  = np.arange(5) + 1 + xVals[-1]

        logger.debug('Extrapolating values to the next 5 points')
        f = interpolate.interp1d(xVals, eps, fill_value="extrapolate")
        epsExt = f(xExt)
        epsExt[-1] *= terminalFactors
        logger.debug(f'Extrapolated EPS = {epsExt}')

        logger.debug('Generating the discounting factor')
        discount = (np.ones(5)*discountingFactor)**np.arange(-1,-6, -1)
        logger.debug(f'discounting factor = {discount}')

        logger.debug('Calculating the DFE')
        dfeValue = epsExt @ discount

        return dfeValue


    except Exception as e:
        logger.error(f'+-----------------------------------------------')
        logger.error(f'| Unable to get the valuation using the DFE method: {e}')
        logger.error(f'| Input data provided: {eps}')
        logger.error(f'| A value of None will be returned')
        logger.error(f'+-------------------------------------')
        return None

    return dfeValue

