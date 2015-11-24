from toLegend import HearthStoneGamePlayer()

#This program will be using the HearthStoneGamePlayer class I designed the the pervious file
#To create a more realistic graph with a decreasing win rate.

class DecreasingReturns(HearthstoneGameplayer):
	"""docstring for DecreasingReturns"""
	def __init__(self):
		super(HearthstoneGameplayer, self, win_percentage=90).__init__()

	def testout(self):
		
		

def main():
	winrate_array = np.array([60, 70, 80, 90, 100])
	player = HearthstoneGameplayer()


	total_time = []
	total_games = []
	yerr_time = []
	yerr_games = []

	for percents in winrate_array:
		#reset the tmp lists and go to the next win percentage
		player.win_percentage = percents
		tmp_time = []
		tmp_games = []
		for runs in range(1000): #repeat 1000 times then take the average
			results = player.testout()
			tmp_time.append(results[0])
			tmp_games.append(results[1])

		total_time.append(np.average(tmp_time))
		yerr_time.append(np.std(tmp_time))

		total_games.append(np.average(tmp_games))
		yerr_games.append(np.std(tmp_games))

if __name__ == '__main__':
	main()