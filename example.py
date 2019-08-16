# Examples for using ReAudio

from ReAudio import ReAudio

re = ReAudio('Tobias_meeting.CSV')
re.getHighestFourDegrees(plot=True)
#re.getSpeakingTime(plot=True)
#re.assignUserLabel()
re.drawNetwork()
