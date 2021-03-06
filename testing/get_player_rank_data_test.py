from bs4 import BeautifulSoup
import requests

def get_html(username):

	url = f"https://r6.tracker.network/profile/pc/{username}"
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	
	return soup


def get_pic_and_level(soup):
	try:
		picture = soup.find('div', class_='trn-profile-header__avatar trn-roundavatar trn-roundavatar--white').img['src']
		level = int(soup.find('div', class_='trn-defstat__name', text='Level').find_next_sibling().text.strip())

		return {'picture': picture, 'level': level}
	except:
		return 'NOT FOUND'

	
	

def get_ranks_from_html(soup):
	ranks_html = soup.findAll('div', class_='r6-quickseason', limit=5)
	mmr_list = []

	img = ranks_html[0].find('img')['src']
	data = ranks_html[0].text.strip().split('\n')
	data = [x for x in data if x]
	print(data)

	if data[1] != 'Unranked':
		season = data[0]
		if ' ' in season:
			season = ' '.join([x.title() for x in season.split(' ')])

		rank_split = data[2].split(' ')
		rank = f"{rank_split[0].title()} {rank_split[1]}"

		mmr = data[1]
		rank_w_mmr = f"{rank} - {mmr}"
		mmr_list.append(int(mmr.split(' ')[0].replace(',','')))
	else:
		season = False


	for season_rank_html in ranks_html[1:]:
		data = season_rank_html.text.strip().split('\n')
		data = [x for x in data if x]

		if data[1] == 'Unranked':
			continue

		if not season:
			season = data[0]
			if ' ' in season:
				season = ' '.join([x.title() for x in season.split(' ')])

		mmr_list.append(int(data[1].split(' ')[0].replace(',','')))

	if not mmr_list:
		return {'rank_w_mmr': 'Unranked', 'avg_mmr': 'N/A', 'rank_img': 'https://r6.tracker.network/Images/r6/seasons/hd-rank0.svg', 'season': 'N/A'}

	mmr_list = mmr_list[:3]
	print(mmr_list)
	avg_mmr = round(sum(mmr_list) / len(mmr_list))

	return {'rank_w_mmr': rank_w_mmr, 'avg_mmr': avg_mmr, 'rank_img': img, 'season': season}
	


def get_player_rank_data(username):
	soup = get_html(username)
	#print(soup.prettify)
	player_data = get_pic_and_level(soup)

	if player_data == 'NOT FOUND':
		return 'NOT FOUND'

	player_data.update(get_ranks_from_html(soup))

	return player_data


if __name__ == '__main__':
	username = 'cryptdaddy.'
	#username = 'agentkazoo.'
	#username = 'crypto-spartan'
	player_rank_data = get_player_rank_data(username)
	print(player_rank_data)