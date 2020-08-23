import numpy as np
from scipy import interpolate
import logging


def discountedFutureEarnings(eps, discountingFactor=1.1, terminalFactor=10.0):
    '''obtain DFE Valuation

    Calculate the valuation using the Discounted Future Earnings valuation method.
    This function assumes that the input for the earnings per share relates to the
    yearly EPS values for a company for the previous N years. Ideally this value 
    is approcimately 5. If this value is less than 3, then an error will be registered
    and a value of ``None`` returned.
    
    Parameters
    ----------
    eps : numpy 1d-array
        The earnings for share for the last N years of data
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

    logger = logging.getLogger('financeMacroFactors.valuation.valuationMethods.discountedFutureEarnings')

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
        epsExt[-1] *= terminalFactor
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

def discountedCashFlow(fcf, shares, discountingFactor=1.1, terminalFactor=10.0):
    '''valuation of a company using the DCF method

    This funciton calculates the valuation of a company using the Discounted Cash Flow method.
    In case there is an error in the calculations, this is going to log an error and will
    return a value of ``None``.

    Parameters
    ----------
    fcf : numpy 1d-array
        The free cash flow of the company for N years
    shares : numpy 1d-array
        Number of free shares outstanding for the company. This should have the same dimensionality
        as the fcf vector. Moreover, there should be a one-to-one correspondence between the values
        within the fcf vector and the shares vector.
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


    logger = logging.getLogger('financeMacroFactors.valuation.valuationMethods.discountedCashFlow')

    dfeVlaue = None
    try:

        assert len(fcf) == len(shares), 'dimensions of the fcf and shares vectors are different'

        N     = len(fcf)

        if N < 3:
            logger.error('Less than 3 EPS values provided.')
            logger.error('The result will not be good. A Null value will be returned.')
            return None

        fcf = np.array(fcf)
        shares = np.array(shares)


        fcfPerShare = fcf/shares
        xVals = np.arange(N)
        xExt  = np.arange(5) + 1 + xVals[-1]

        logger.debug('Extrapolating values to the next 5 points')
        f = interpolate.interp1d(xVals, fcfPerShare, fill_value="extrapolate")
        fcfExt = f(xExt)
        fcfExt[-1] *= terminalFactor
        logger.debug(f'Extrapolated EPS = {fcfExt}')

        logger.debug('Generating the discounting factor')
        discount = (np.ones(5)*discountingFactor)**np.arange(-1,-6, -1)
        logger.debug(f'discounting factor = {discount}')

        logger.debug('Calculating the DFE')
        dcfValue = fcfExt @ discount

        return dcfValue


    except Exception as e:
        logger.error(f'+-----------------------------------------------')
        logger.error(f'| Unable to get the valuation using the DFE method: {e}')
        logger.error(f'| Input data provided: ')
        logger.error(f'|    fcf    : {fcf}')
        logger.error(f'|    shares : {shares}')
        logger.error(f'| A value of None will be returned')
        logger.error(f'+-------------------------------------')
        return None

    return dfeValue

def priceToSalesRatio(revenue, shares, price):
    '''valuation of a company using the P/S ration method

    This will allow you to get the valuation of the company with the price-to-sales method. 
    In case that there is an error detected, this is going to return a ``None`` and will 
    also log an appropriate error.

    Parameters
    ----------
    revenue : numpy 1d-array
        This is a vector of yearly revenues associated with the company for the last N
        years. This is typically present in the Income Statement of the company.
    shares : numpy 1d-array
        This is a vector containing the number of shares outstanding of the company
        for the same years for which the revenue is provided. There should be a 
        one-to-one correspondence between the revenue and the number of shares
        outstanding.
    price : numpy 1d-array
        This is a vector representing the price of a single share for the last N
        years. The size of the vector should be the same as the size of the other
        two input vectors. There should be a one-to-one correspondence between the
        values within the vector.

    Returns
    -------
    float
        The valuation of the company according to the P/S method
    '''

    psValue = None
    logger = logging.getLogger('financeMacroFactors.valuation.valuationMethods.priceToSalesRatio')

    try:
        
        assert len(revenue) == len(shares), 'dimensions of the revenue and shares vectors are different'
        assert len(revenue) == len(price), 'dimensions of the revenue and price vectors are different'

        logger.debug(f' Input | revenue : {revenue}')
        logger.debug(f' Input | shares  : {shares}')
        logger.debug(f' Input | price   : {price}')
        logger.debug(f' Calcualting the price to sales ratio')

        revenue = np.array(revenue)
        shares  = np.array(shares)
        price   = np.array(price)

        p_s = price / ( revenue / shares )
        logger.debug(f'price to sales ratio = {p_s}')

        mean_ps = p_s.mean()
        logger.debug(f'The average value of the P/S ratio = {mean_ps}')

        psValue =  mean_ps * (revenue[-1] / shares[-1])
        logger.debug(f'The P/S valuation = {psValue}')

        return psValue

    except Exception as e:
        logger.error(f'+-----------------------------------------------')
        logger.error(f'| Unable to get the valuation using the DFE method: {e}')
        logger.error(f'| Input data provided: ')
        logger.error(f'|    revenue : {revenue}')
        logger.error(f'|    shares  : {shares}')
        logger.error(f'|    price   : {price}')
        logger.error(f'| A value of None will be returned')
        logger.error(f'+-------------------------------------')
        return None
        

    return psValue

def priceToEarningsRatio(eps, price):
    '''valuation of a company using the P/E ration method

    This will allow you to get the valuation of the company with the price-to-earnings method. 
    In case that there is an error detected, this is going to return a ``None`` and will 
    also log an appropriate error.

    Parameters
    ----------
    eps : numpy 1d-array
        This is a vector of yearly earnings per share associated with the company 
        for the last N years. This is typically present in the Income Statement of 
        the company.
    price : numpy 1d-array
        This is a vector representing the price of a single share for the last N
        years. The size of the vector should be the same as the size of the other
        two input vectors. There should be a one-to-one correspondence between the
        values within the vector.

    Returns
    -------
    float
        The valuation of the company according to the P/E method
    '''

    peValue = None
    logger = logging.getLogger('financeMacroFactors.valuation.valuationMethods.priceToSalesRatio')

    try:
        
        assert len(eps) == len(price), 'dimensions of the eps and price vectors are different'
        
        logger.debug(f' Input | eps     : {eps}')
        logger.debug(f' Input | price   : {price}')
        logger.debug(f' Calcualting the P/E ratio')

        eps   = np.array(eps)
        price = np.array(price)

        p_e = price / ( eps )
        logger.debug(f'price to earnings ratio = {p_e}')

        mean_pe = p_e.mean()
        logger.debug(f'The average value of the P/E ratio = {mean_pe}')

        peValue =  mean_pe * (eps[-1])
        logger.debug(f'The P/E valuation = {peValue}')

        return peValue

    except Exception as e:
        logger.error(f'+-----------------------------------------------')
        logger.error(f'| Unable to get the valuation using the DFE method: {e}')
        logger.error(f'| Input data provided: ')
        logger.error(f'|    eps : {eps}')
        logger.error(f'|    price   : {price}')
        logger.error(f'| A value of None will be returned')
        logger.error(f'+-------------------------------------')
        return None
        

    return peValue
