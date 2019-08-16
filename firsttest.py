from ReAudio import ReAudio

f = ReAudio('Tobias_meeting.csv')

degrees = f.getHighestFourDegrees(True)
print(degrees)
f.assignUserLabel()
#
f.getSpeakingTime(True,'sec')
f.drawNetwork()
