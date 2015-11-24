import numpy as np
import matplotlib.pyplot as plt


rank_dict = {20:3, 19:3, 18:3, 17:3, 16:3, \
	             15:4, 14:4, 13:4, 12:4, 11:4, \
	             10:5, 9:5, 8:5, 7:5, 6:5, 5:5, 4:5, 3:5, 2:5, 1:5}
class HearthstoneGameplayer:
	def __init__(self, win_percentage=0, starting_rank=20):
		self.origional = starting_rank
		self.win_percentage = win_percentage
		self.rank = starting_rank

	def testout(self):
		#the total time in minutes. will be converted to hours/days at the end
		total_time = 0
		total_games = 0

		#The total stars will start at rank 20, the beginning of where one can loose stars.
		self.rank_stars = 0
		self.rank = self.origional

		#See if a winstreak is applicable
		wins = 0

		while True:
			total_games += 1
			#average amout of time per game is reported to be between 5-15 min.
			#http://www.hearthpwn.com/forums/hearthstone-general/general-discussion/12835-game-length-a-study
			#http://www.gamefaqs.com/boards/710060-hearthstone-heroes-of-warcraft/68564232
			total_time += np.random.uniform(low=5, high=16)

			if np.random.uniform(low=0, high=1) <= (self.win_percentage / 100):
				wins += 1
				self.rank_stars += 1
				#check for winstreak
				if wins >= 3 and self.rank > 5:
					self.rank_stars += 1
				rankup(self)
				if self.rank == 0:
					break
				continue

			if self.rank == 20 and self.rank_stars == 0:
				continue
			wins = 0
			self.rank_stars -= 1
			rankdown(self)

		return (total_time/60, total_games)


def rankup(player):
	#increases rank if necessary
	if rank_dict[player.rank] < player.rank_stars:
		player.rank -= 1
		if player.rank == 0:
			return
		player.rank_stars -= rank_dict[player.rank]


def rankdown(player):
	if player.rank_stars < 0:
		player.rank += 1
		player.rank_stars += rank_dict[player.rank]


def main():
	while True:
		winrate = input('Would you like to see stats for a spicific winrate or a spread?: ')
		if winrate == 'spread': break
		try:
			float(winrate)
			break
		except Exception:
			pass

	if winrate == 'spread':
		winrate_array = np.array([51, 60, 70, 80, 90, 100])
		player = HearthstoneGameplayer()


		total_time = []
		total_games = []
		yerr_time = []
		yerr_games = []

		for percents in winrate_array:
			player.win_percentage = percents
			tmp_time = []
			tmp_games = [] 
			for runs in range(1000):
				results = player.testout()
				tmp_time.append(results[0])
				tmp_games.append(results[1])

			total_time.append(np.average(tmp_time))
			yerr_time.append(np.std(tmp_time))

			total_games.append(np.average(tmp_games))
			yerr_games.append(np.std(tmp_games))
			

		for x in range(len(total_games)):
			print('{}%: {} games with an std of {} and {} hours with an std of {}\n'.format(winrate_array[x], total_games[x], yerr_games[x], total_time[x], yerr_time[x]))

		plt.figure(1)
		plt.errorbar(x=winrate_array, y=total_games, yerr=yerr_games)
		plt.title('Average number of games to legend from rank 20')
		plt.xlabel('Win percentage')
		plt.ylabel('Number of games played')
		


		plt.figure(2)
		plt.errorbar(x=winrate_array, y=total_time, yerr=yerr_time)
		plt.title('Average time to legend from rank 20')
		plt.xlabel('Win percentages')
		plt.ylabel('Time (in hours)')
		

		plt.show()

	else:
		while True:
			rank = input('What rank would you like to start at? (Leave blank for 20):')
			if rank == '':
				rank = 20
				break
			if int(rank) > 20:
				continue
			break
		player = HearthstoneGameplayer(win_percentage=int(winrate), starting_rank=int(rank))
		total_games = []
		total_time = []
		for x in range(100):
			results = player.testout()
			total_games.append(results[1])
			total_time.append(results[0])
		print('Starting from rank {}, it took an average of {} games and {} hours'.format(rank, np.average(total_games), np.average(total_time)))

if __name__ == '__main__':
	main()