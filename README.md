# pythonEmailTest5
# Below is the question for the test.

Please download daily price data of about 500 stocks in S&amp;P 500 to calculate daily return series of
500 stock in S&amp;P500. Now you can calculate correlation between 500 stocks from return series.
This will be written as 500 x 500 matrix with ones along the diagonal. Let's define Corr(A,B) as the
correlation coefficient between A and B derived from their return series. Then, build clusters
satisfying the following conditions:
 
Correlation between any pair of stock in the same cluster must be higher than pair of stocks from
different cluster. For example, A and B are from one cluster and C are for another cluster; Corr(A,B)\>= Corr(A,C) and Corr(A,B) >= Corr(B,C)
 
Then, you are now supposed to find clusters defined above to optimize the following objective
functions.
 
  1) Summation over Correlations between stocks in the same cluster is maximized. This sum of
correlation is sum of all the elements in correlation matrix. I.e. if you constructed a cluster with 100
stocks. You can calculate 100 x 100 correlation matrix and sum up all the elements to get &quot;sum of
correlation&quot;. In other word, stocks in the same cluster must be highly correlated.
  2) The number of clusters is not restricted as long as you have more than four clusters. But standard
deviation of the numbers of clusters is to be minimized. For example, clusters of 100 stocks, 100
stocks, 100 stocks and 200 stocks are better than those of 300 stocks, 160 stocks, 35 stocks and 5
stocks.
  3) You can calculate the average of returns of stocks in the same cluster. If you have four clusters, you
will have four average returns, from which 4x4 correlation matrix can be calculated. Summation over
Correlation  between average returns of clusters is minimized. In other word, clusters must not be
correlated in terms of average return
