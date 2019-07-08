# ReAudio
ReAudio is a python library to analyze the data recieved by ReSpeaker 4 Mic with direction of arrival algorithm. ReSpeaker comes with DoA (Direction of arrival) and Voice Activation Detection (VAD) algorithm which eases the analysis work. This library will help in extracting the speaking time, generating the edge list for social network and drawing the social network of interaction among participants.



# Functions
#### 1. getHighestFourDegree(plot)
This function process the input file and provide four highest occuring DoA in degrees. It takes one argument plot (Boolean) as flag to plot the distribution of DoA degrees. It returns a list of four items (degree,frequency) where degree represents the DoA and frequency represents the number of times that degree appears in the file.
Example:
```python
from ReAudio import ReAudio
re = ReAudio('demo.csv')
degrees = re.getHighestFourDegree(True)
```
![](https://github.com/pankajchejara23/ReAudio_library/blob/master/distri.png)

#### 2.assignUserLabel()
This function assign the user labels on the basis of DoA. It assumes the following orientation for users sitting arrangement.
![](https://github.com/pankajchejara23/ReAudio_library/blob/master/re_orient.png)
This function first finds out the four highly occuring directions and then sort those direction in ascending order. Then, first degree considered as user-1 DoA, second for user-2, third for user-3 and fourth for user-4.

Once the DoA is associated with their corresponding users, each degree then assigned a user label. This assignment is done on the basis of the closeness with identified DoA for each users.
Example:
```python
from ReAudio import ReAudio
re = ReAudio('demo.csv')
re.assignUserLabel(True)
```

#### 3. getSpeakingTime(plot,time)
This function computes speaking time for each user. Each entry in the file represent a speech activity for 200 ms. This function simply count the number of entries for each user and then multiply it with 200/1000 to get speaking time in seconds.
**Parameters**:
* plot (Boolean type): if want to plot the speaking time for each user, specify True otherwise False.
* time(string, possible values=['sec','min','hour']): Specify the time unit for computing speaking time.

**Return value**
* Dictionary containing user speaking time. keys:users, values:speaking time

**Example:**
```python
from ReAudio import ReAudio
re = ReAudio('demo.csv')
re.getSpeakingTime(True,'sec')
```


#### 4. generateEdgeFile()
This function generate a edge file for drawing graph of interactions. To remove the wrong entries, we assumed that atleaset four consecutive entries (one entry represents speaking time for 200 ms) must be there to qualified as a speaking activity. As we observed that during identifying the DoA some wrong entries are also recorded. This function uses user labels assigned to each entry and computes the continuous occurrence.
For example:
> a = [1,1,1,2,2,2,2,3,3]
> continuous_occurrence = {1:3,2:4,3:2}

It then uses these occurrence to remove entries having less than 4 occurrence. After this step final user speaking sequence is generated. This sequence is then used to generate edge list. This function generates a file 'edges.txt' which can be used by graph generating software to draw graphs.

#### 5. drawNetwork()
This function draws an interaction network between participants. If an edge is repeated then its weight is increased correspondigly. The thickness of edge determines its frequency.

For nodes, three different colors are used. If a node's correpsonding user has spoken more than average speaking time then it's represented using green color code. In the case of below average speaking time, red color code is used. For the remaining category, plum color code is used.

**Example:**
```python
from ReAudio import ReAudio
re = ReAudio('demo.csv')
re.assignUserLabel()
re.drawNetwork()
```
