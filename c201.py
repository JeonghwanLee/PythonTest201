import urllib2
from math import sqrt

# Function to open wikipedia SNP 500 list page and return 500 tickers
def getSNP():
    lst = []
    urlOpening = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    html = urlOpening.read()
    snptableHtml = html[:html.find('</table>')]
    start = 0
    while start < snptableHtml.find('ZTS'):
        trStartLoc = snptableHtml.find('<tr>', start)  
        tdStartLoc = snptableHtml.find('<td>', trStartLoc)
        tickerStartLoc = snptableHtml.find('>', tdStartLoc+4)+1
        tickerEndLoc = snptableHtml.find('</a>', tdStartLoc)
        lst.append(snptableHtml[tickerStartLoc:tickerEndLoc])
        trEndLoc = snptableHtml.find('</tr>', tickerEndLoc) 
        start = trEndLoc
    # Update the above list of tickers due to changes of SNP 500 companies
    changetableHtml = html[start:]
    start = changetableHtml.find('Reason')
    tdCounter = 1 
    while start < changetableHtml.find('<tfoot></tfoot>'):
        trLoc = changetableHtml.find('<tr>', start)
        tdLoc = changetableHtml.find('<td>', trLoc)
        tdEndLoc = changetableHtml.find('</td>',tdLoc)
        while tdCounter < 5:
            if tdCounter % 2 != 0:
                tdLoc = changetableHtml.find('<td>', tdEndLoc)
                tdCounter +=1
            # Add new companies to SNP 500 list
            elif tdCounter == 2:
                lst.append(changetableHtml[tdLoc+4:tdEndLoc])
                tdLoc = changetableHtml.find('<td>', tdEndLoc)
                tdCounter +=1
            # Remove the companies removed from SNP 500
            else:
                lst.remove(changetableHtml[tdLoc+4:tdEndLoc])
                tdLoc = changetableHtml.find('<td>', tdEndLoc)
                tdCounter +=1
        trEndLoc = hangetableHtml.find('</tr>', tdLoc)
        start = trEndLoc
        tdCounter = 1
    # Remove five companies in SNP 500 list to return only 500 out of 505    
    lst.remove('BRK.B')
    lst.remove('BF.B')
    lst.remove('PNR')
    lst.remove('ZION')
    lst.remove('ZTS')   
    return lst

# Function to calculate its daily return 
# Get open-price and close-price for each company in SNP list 
def calDailyReturn(tickerList):
    i = 0
    dailyReturnList = []
    tableCounter = 2
    for ticker in tickerList:
        # Open yahoo finance historical data page for each company
        url = "https://finance.yahoo.com/quote/%s/history?p=%s"%(ticker,ticker)
        urlOpening = urllib2.urlopen(url)
        html = urlOpening.read()
        # Find second '<tbody>' block because stock history is on that bloack on the web
        # Then, minimize html range which shows the stock price history table        
        tbodyLoc = html.find('<tbody ')
        secondTbodyLoc = html.find('<tbody ', tbodyLoc)
        tbodyEndLoc = html.find('</tbody ', secondTbodyLoc)
        html = html[secondTbodyLoc:tbodyEndLoc]
        trCounter = 1
        tdCounter = 1
        start = 0
        openPrice = 0
        closePrice = 0
        dailyReturn = []
        # trCounter means 'row' of the stock history table on the web
        # 'trCounter < 8' means the recent 7 days stock price data in the history table
        while trCounter < 8:
            trStartLoc = html.find('<tr class', start)
            tdStartLoc = html.find('<td class',trStartLoc)
            tdEndLoc = html.find('</td>',tdStartLoc)
            while tdCounter < 6:
                if tdCounter == 2:
                    priceHtml = html[html.find('</span>',tdStartLoc,tdEndLoc)-9:html.find('</span>',tdStartLoc,tdEndLoc)]
                    # If there's 'Dividend' in the price table, skip the day (or the table row)
                    if priceHtml.find('Dividend')>0:
                        trCounter += -1
                        break
                    else:
                        priceHtml = priceHtml[priceHtml.find('>')+1:]
                        if priceHtml.find('>') > 0:
                            priceHtml = priceHtml[priceHtml.find('>')+1:]
                            openPrice = float(priceHtml.replace(',', ''))
                        else:
                            openPrice = float(priceHtml.replace(',', ''))
                        tdStartLoc = html.find('<td class', tdEndLoc)
                        tdEndLoc = html.find('</td>',tdStartLoc)
                        tdCounter += 1
                elif tdCounter == 5:
                    priceHtml = html[html.find('</span>',tdStartLoc,tdEndLoc)-10:html.find('</span>',tdStartLoc,tdEndLoc)]
                    if priceHtml.find('Dividend')>0:
                        trCounter += -1
                        break
                    else:  
                        priceHtml = priceHtml[priceHtml.find('>')+1:]
                        if priceHtml.find('>') > 0:
                            priceHtml = priceHtml[priceHtml.find('>')+1:]
                            closePrice = float(priceHtml.replace(',', ''))
                        else:
                            closePrice = float(priceHtml.replace(',', ''))
                        tdStartLoc = html.find('<td class', tdEndLoc)
                        tdEndLoc = html.find('</td>',tdStartLoc)
                        tdCounter +=1
                        # Append daily return into 'dailyReturn' list
                        dailyReturn.append(round((closePrice/openPrice - 1)*100, 2))
                else:
                    priceHtml = html[html.find('</span>',tdStartLoc,tdEndLoc)-10:html.find('</span>',tdStartLoc,tdEndLoc)]
                    if priceHtml.find('Dividend')>0:
                        break
                    else:
                        tdCounter +=1
                        tdStartLoc = html.find('<td class', tdEndLoc)
                        tdEndLoc = html.find('</td>',tdStartLoc)
            trEndLoc = html.find('</tr>', tdEndLoc)
            start = trEndLoc
            tdCounter = 1
            trCounter +=1
        # Index order of the list is the same with companies in tickerList, the input of this function
        dailyReturnList.append(dailyReturn)
        dailyReturn = []
    return dailyReturnList

# Function to calculate correlation coefficient of two stocks having 7-days daily return
def Corr(A,B):
    sampleSize = len(A)
    aPowerSum = 0
    bPowerSum = 0
    abMultiSum = 0
    aSum = 0
    bSum = 0
    for i in range(sampleSize):
        aPowerSum = aPowerSum + A[i]*A[i]
        bPowerSum = bPowerSum + B[i]*B[i]
        abMultiSum = abMultiSum + A[i]*B[i]
        aSum = aSum + A[i]
        bSum = bSum + B[i]
    r = ((sampleSize*abMultiSum) - (aSum*bSum)) / sqrt(((sampleSize*aPowerSum) - (aSum*aSum))*((sampleSize*bPowerSum) - (bSum*bSum))) 
    return r
    
# Main function
# 1. Get SNP company list and its daily return list
# 2. Calulate correlation coefficient between first 500 companies
# 3. Sort the company list in descending order by correlation coefficient value
# 4. Make first 100 companies a 'cluster' and remove the 100 companies from snp company list and daily reuturn list
# 5. Build five clusters which are made of 100 companies which are highly correlated with each other
def main():
    clusterList = []
    cluster = []
    corrList = []
    snpCompanies = getSNP()
    snpDailyReturnList = calDailyReturn(snpCompanies)
    i = 0
    j = 0
    while i < 5:
        while j < len(snpDailyReturnList):
            # Make the absolute value of a correlation coefficient to see how data are correlated with each other
            # If the absolute value is close to '1', it means that two data are highly correlated
            corr = Corr(snpDailyReturnList[0],snpDailyReturnList[j])
            corrList.append(abs(corr))
            j+=1
        j = 0
        # Sort corrList in descending order by correlation coefficient value
        # Syncronize its order with dailyReturnList and snpCompanies
        for k in range(len(snpDailyReturnList)):
            if corrList[k-1] < corrList[k]:
                corrList[k-1], corrList[k] = corrList[k], corrList[k-1]
                snpCompanies[k-1], snpCompanies[k] = snpCompanies[k], snpCompanies[k-1]
                snpDailyReturnList[k-1], snpDailyReturnList[k] = snpDailyReturnList[k], snpDailyReturnList[k-1]
        # Set 100 companies which are correlated with each other in one cluster
        l = 99
        while l >= 0:
            cluster.append(snpCompanies[l])
            snpCompanies.remove(snpCompanies[l])
            snpDailyReturnList.pop(l)
            l += -1
        clusterList.append(cluster)
        corrList = []
        cluster = []
        i+=1    
    for clusters in clusterList:
        print clusters   
# Takes a few mintues to get the result        
main()    