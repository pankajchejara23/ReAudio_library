"""
      ReAudio: Library for generating interaction network and speech feature from data captured using ReSpeaker 4 Mic version 1
      Developer: Pankaj Chejara
      Date: 8/07/2019
"""

# Import package
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import Counter
import sys

class ReAudio(object):

    """
    Arguemnts: file_name
               Specify the name of file which contains records in format (timestamp,degree) and has a csv extention
    """
    def __init__(self,file_name):
        self.file_name = file_name
        self.Directions = np.array([0,0,0,0])


    """
    getHighestFourDegrees: This function will search through the file and extract four degrees corresponding to users.
                           It simply count the degree frequency and return four degrees with highest frequencies.

    Arguemnts: plot (Boolean)
              Setting this argument to True with plot all degrees found in the file.
    """
    def getHighestFourDegrees(self,plot):
        try:
            # Read the file
            self.file = pd.read_csv(self.file_name)

            # If file is not in required format then break
            if len(self.file.columns) != 2:
                print('File has more than two columns. File must have two columns (timestamp,degree)')
                return null

            # Set the column names
            self.file.columns=['timestamp','degree']

            # Count the frequency of each degree in the file
            degree_frequency = Counter(self.file['degree'])

            # Plot the bar graph for degree frequency if plot = True
            if plot:
                plt.bar(degree_frequency.keys(),degree_frequency.values(),width=10)
                plt.xlabel('Direction of arrival')
                plt.ylabel('Frequency')
                plt.title('Frequncy distribution of DoA (Direction of Arrival)')
                plt.show()

            # Sort the degrees on the basis of their counted frequency
            sorted_deg_freq = sorted(degree_frequency.items(),key=lambda x:x[1])

            # Get four highest degrees
            highest_degrees = sorted_deg_freq[-4:]


            # Sort the order of highest degrees and return
            highest_degrees = sorted(highest_degrees,key=lambda x:x[0])
            return highest_degrees
        except Exception as e:
            print('Exception:',sys.exc_info())




    """


    """
    def assignUserLabel(self):
        highDegrees = self.getHighestFourDegrees(plot=False)
        users = np.array([item[0] for item in highDegrees])

        def assign_label(degree):
            user_diff = np.absolute(users-degree)
            min_diff = np.min(user_diff)

            indices = np.where(user_diff==min_diff)
            ind = indices[0]+1
            return ind[0]

        self.file['users'] = self.file['degree'].map(assign_label)

        #print(self.file.head())




    def getSpeakingTime(self,plot,time='sec'):
        speech_count = self.file.groupby('users').count()

        user_speak_time = {1:0,2:0,3:0,4:0}

        for i in range(4):
            if time=='sec':
                user_speak_time[i+1] = speech_count.loc[i+1,'degree']*float(200/1000)
            elif time=='min':
                user_speak_time[i+1] = speech_count.loc[i+1,'degree']*float(200/60*1000)
            elif time=='hour':
                user_speak_time[i+1] = speech_count.loc[i+1,'degree']*float(200/(60*60*1000))
        print(user_speak_time)

        if plot:
            plt.figure()
            plt.bar(user_speak_time.keys(),user_speak_time.values())

            plt.ylabel('Time(%s)' % time)
            plt.xlabel('Users')
            plt.xticks(np.arange(4)+1,['user-1','user-2','user-3','user-4'])
            plt.title('Speaking time for each user')
            plt.show()
        return user_speak_time


    def generateEdgeFile(self):
        if 'users' in self.file.columns:
            sequence = self.file['users'].to_numpy()
        else:
            self.assignUserLabel()
            sequence = self.file['users'].to_numpy()
        #print('Seq:',sequence)
        df = pd.DataFrame(columns=['users','conti_frequency'])

        def count_conti_occurence(index):
            count=0
            j = index
            while j<len(sequence):
                if sequence[j] == sequence[index]:
                    count +=1
                else:
                    break
                j +=1
            return count,(j-index)
        i = 0
        while i < len(sequence):
            count,diff = count_conti_occurence(i)
            #print('Item:%d Count:%d Next_index:%d'%(sequence[i],count,diff))
            df = df.append({'users':sequence[i],'conti_frequency':count},ignore_index=True)
            i = i + diff
        #print(df)
        process_df = df.where(df.conti_frequency>4)
        process_df.dropna(axis=0,how='any',inplace=True)

        processed_sequence = process_df['users'].to_numpy()
        file  = open('edges.txt','w')
        self.edge_list = list()

        node1=node2=0

        for i in range(len(processed_sequence)):
            if node1==0:
                node1=processed_sequence[i]
            else:
                node2=processed_sequence[i]
                self.edge_list.append((node1,node2))
                print("{},{}".format(node1,node2))
                file.write("{},{}\n".format(node1,node2))
                node1=node2
        file.close()
        print('Edge file is generate with name edges.txt')

    def drawNetwork(self,edge_file):
        self.generateEdgeFile()

        G = nx.Graph()
        for edge in edge_list:
            for edge in edge_list:
                if G.has_edge(edge[0],edge[1]):
                    w = G[edge[0]][edge[1]]['weight']
                    G.remove_edge(edge[0],edge[1])
                    G.add_edge(edge[0],edge[1],weight=w+.5)

                else:
                    G.add_edge(edge[0],edge[1],weight=.5)


                    pos = nx.spring_layout(G)

                    edges = G.edges()
                    weights = [G[u][v]['weight'] for u,v in edges]
                    color_map = []
                    for node in G:

                        if sp_beh[node]<sp_avg-1:
                            color_map.append('red')
                        elif sp_beh[node]<sp_avg+1 and sp_beh[node]>sp_avg-1:
                            color_map.append('plum')
                        else:
                            color_map.append('lawngreen')

                        print (color_map)

                        nx.draw(G, pos,node_color=color_map,  edges=edges,width=weights,with_labels=True)
                        plt.show()
