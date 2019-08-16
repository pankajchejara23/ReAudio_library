"""
Eatherpad Log Analyzer

Author: Pankaj Chejara
Date : 16 Aug 2019

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class etherLogAnalyzer(object):
    """
    init function initialize the etherLogAnalyzer object.
    it takes one parameter the file name as
    """
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            self.file = pd.read_csv(file_name,names=['timestamp','ip','action','oldlen','newlen','changeset','charbank','noadd','noremove'])
            print('File loaded successfully....')

            print('Setting timestamp as index...')
            self.file = self.file.set_index(pd.DatetimeIndex(self.file['timestamp']))

        except:
            print('Error occured while opening the file')



    """
    This function will return the number of total ip recorded in the log file.
    """

    def getAuthorCount(self):
        return len(self.file.ip.unique())

    """
    This function returns the list of Author's IP recorded in the log file.
    """

    def getAuthorIP(self):
        return self.file.ip.unique()

    """
    Logs are recorded in same file for all the pads, therefore this function will seperate the log file
    on the basis of group. It reuires parameter e.g. group name and group ips.
    @params: group_name (String): name of group
             group_ips (List): list containing ips belong to that group
    Return type: Pandas dataframe.
    """

    def getLogForGroup(self,group_name,group_ips):
        temp_df = self.file[self.file.ip.isin(group_ips)]
        return temp_df

    """
    This function will generate statistics for each author in the group. These statistics are in form of number of addition
    and deletion along with time.
    @params:
       ip (String): ip address for which you want to see the stats
       timescale (String): it specify the time window for aggregating statistics.
       Possible values: Alias   Description
                        B       business day frequency
                        C       custom business day frequency (experimental)
                        D       calendar day frequency
                        W       weekly frequency
                        M       month end frequency
                        BM      business month end frequency
                        CBM     custom business month end frequency
                        MS      month start frequency
                        BMS     business month start frequency
                        CBMS    custom business month start frequency
                        Q       quarter end frequency
                        BQ      business quarter endfrequency
                        QS      quarter start frequency
                        BQS     business quarter start frequency
                        A       year end frequency
                        BA      business year end frequency
                        AS      year start frequency
                        BAS     business year start frequency
                        BH      business hour frequency
                        H       hourly frequency
                        T, min  minutely frequency
                        S       secondly frequency
                        L, ms   milliseonds
                        U, us   microseconds
                        N       nanoseconds
        plot(Boolean): Specify True if you want to plot the graph


     Return type: Dataframe


    """



    def generateStatsForAuthor(self,ip,plot=False,timescale='30S'):
        temp = self.file.copy()
        temp = temp.loc[temp['ip']==ip,:]
        temp['addition'] = temp['newlen']-temp['oldlen']
        temp['deletion'] = temp['oldlen']-temp['newlen']
        mask = temp['addition']<0
        mask2 = temp['deletion']<0
        temp.loc[mask,'addition']=0
        temp.loc[mask2,'deletion']=0
        stat = temp.groupby(pd.Grouper(freq=timescale)).sum()
        if plot:
            stat[['addition','deletion']].plot(kind='bar')
            plt.title('Stats for User:'+ip)
        return stat

analyzer = etherLogAnalyzer('Tobias_etherpad.csv')
stat = analyzer.generateStatsForAuthor(ip='193.40.238.205',plot=True,timescale='2T')
