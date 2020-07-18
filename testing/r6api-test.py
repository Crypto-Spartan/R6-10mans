import asyncio
import r6sapi as api

async def test():
	auth = api.Auth('tylerbelfield@gmail.com', 'CiscoSquad14')

	player = await auth.get_player('Crypto-Spartan', api.Platforms.UPLAY)

	await player.check_level()
	#for season_num in [-1, -2, -3]:
	#	await player.get_rank('NA', season=season_num)

	await player.get_rank('NA', season=-2)
	level = player.level
	ranks = player.ranks
	url = player.url

	await auth.close()

	print(url)
	print(level)
	print(ranks)

asyncio.run(test())


#https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/r6karma/players?board_id=pvp_ranked&profile_ids=%s&region_id=%s&season_id=%s  (self.spaceid, self.platform_url, self.player_ids, region, season)

#https://game-rainbow6.ubi.com/en-us/uplay/player-statistics/f59b1e86-3906-46af-bfc3-b897f035b188/multiplayer