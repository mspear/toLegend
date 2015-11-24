#!/usr/bin/env python3
import numpy as np
from toLegend import HearthstoneGameplayer

#This program will be using the HearthstoneGameplayer class I designed the the pervious file
#To create a more realistic graph with a decreasing win rate.

rank_dict = {20:3, 19:3, 18:3, 17:3, 16:3, \
	             15:4, 14:4, 13:4, 12:4, 11:4, \
	             10:5, 9:5, 8:5, 7:5, 6:5, 5:5, 4:5, 3:5, 2:5, 1:5}

class DecreasingReturns(HearthstoneGameplayer):
	"""docstring for DecreasingReturns"""
	def __init__(self, rank=20):
		super().__init__(rank)

	def testout(self):
		total_games = 0
		total_time = 0

		#The total stars will start at rank 20, the beginning of where one can loose stars.
		self.rank_stars = 0
		self.rank = self.origional

		#See if a winstreak is applicable
		wins = 0
		winrate_spread = [90, 80, 70, 60]

		while True:
			total_games += 1

			total_time += np.random.uniform(low=5, high=16)

			#selection statement to change win percentages as the program runs
			if self.rank > 15:
				self.win_percentage = winrate_spread[0]
			else:
				if self.rank > 10:
					self.win_percentage = winrate_spread[1]
				else:
					if self.rank > 5:
						self.win_percentage = winrate_spread[2]
					else:
						self.win_percentage = winrate_spread[3]
				

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
	player = DecreasingReturns()

	tmp_time = []
	tmp_games = []
	for runs in range(1000): #repeat 1000 times then take the average
		results = player.testout()
		tmp_time.append(results[0])
		tmp_games.append(results[1])

	total_time = np.average(tmp_time)
	yerr_time = np.std(tmp_time)

	total_games = np.average(tmp_games)
	yerr_games = np.std(tmp_games)

	print('With this spread of win rates it took {} games with and std of {} and {} hours with an std of {} to get to Legend\n'\
		.format(total_games, yerr_games, total_time, yerr_time))

if __name__ == '__main__':
	main()