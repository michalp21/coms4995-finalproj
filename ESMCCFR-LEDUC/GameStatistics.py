import re
import sys
from Summary import Summary
from rules.Leduc import Leduc
from Deal import Deal

card_to_rank = {'A':1, 'K':2, 'Q':3}

def isTerminal(cards, betting):
	# if the line looks like 'card|card/card', then it is terminal
	# NOTE: GAME CAN ALSO BE TERMINAL BY ENDING ON FOLD, IN WHICH CASE YOU DO NOT KNOW THE OPPONENT'S CARD
	num_cards = sum([1 for c in cards if len(c) > 0])
	if num_cards == 3:
		return True
	elif betting[1]:
		return betting[1][-1] == 'f'
	elif betting[0]:
		return betting[0][-1] == 'f'
	else:
		return False

def pfr_vpip(position, round1_bets, p1_contrib, p2_contrib):
	p1_pfr, p2_pfr, p1_vpip, p2_vpip = False, False, False, False
	for i in range(len(round1_bets)):
		bet = round1_bets[i]
		if bet.startswith('c'):
			if p1_contrib == p2_contrib:
				pass
			elif p1_contrib < p2_contrib:
				p1_contrib = p2_contrib
				p1_vpip = True
			elif p2_contrib < p1_contrib:
				p2_contrib = p1_contrib
				p2_vpip = True
		elif bet.startswith('r'):
			if int(position) == i % 2:
				p1_contrib += int(bet[1:])
				p1_pfr = True
				p1_vpip = True
			elif int(position) != i % 2:
				p2_contrib += int(bet[1:])
				p2_pfr = True
				p2_vpip = True
		elif bet.startswith('f'):
			pass
	return p1_pfr, p2_pfr, p1_vpip, p2_vpip

def amt_winner(position, round1_bets, round2_bets, contribs, cards):
	winner = None
	previous_bet = 0
	# assume player 1 in position 0. otherwise switch at the end
	for i in range(len(round1_bets)):
		bet = round1_bets[i]
		if bet.startswith('c'):
			contribs[i%2] += previous_bet
		elif bet.startswith('r'):
			contribs[i%2] = int(bet[1:])
			previous_bet = int(bet[1:]) - previous_bet
		elif bet.startswith('f'):
			winner = 1-(i%2)

	for i in range(len(round2_bets)):
		bet = round2_bets[i]
		if bet.startswith('c'):
			contribs[i%2] += previous_bet
		elif bet.startswith('r'):
			contribs[i%2] = int(bet[1:])
			previous_bet = int(bet[1:]) - previous_bet
		elif bet.startswith('f'):
			winner = 1-(i%2)

	# evaluate cards to determine winner if no one folded yet
	if winner is None:
		leduc = Leduc()
		deal = Deal(None, None, None, None)
		deal.board = [[card_to_rank[cards[0][0]]]]
		deal.small = [card_to_rank[cards[1][0]]]
		deal.big = [card_to_rank[cards[2][0]]]
		winner = 0 if leduc.evaluate(deal) > 0 else 1
	amt = min(contribs)
	return amt, winner

def get_stats(position, cards, betting):
	p1_contrib = 100
	p2_contrib = 100
	p1_pfr, p2_pfr, p1_vpip, p2_vpip = pfr_vpip(position, betting[0], p1_contrib, p2_contrib)
	amt, winner = amt_winner(position, betting[0], betting[1], [p1_contrib, p2_contrib], cards)
	# need to count the winner and the amount that they won!!!
	return Summary(p1_pfr, p2_pfr, p1_vpip, p2_vpip, amt, winner)

def parse_cards(cards):
	card0, card1 = cards.split('|')
	card2 = ''
	if '/' in card1:
		card1, card2 = card1.split('/')
	cards = (card0.strip(), card1.strip(), card2.strip())
	return cards

def parse_betting(betting):
	betting0 = betting
	betting1 = None
	if '/' in betting:
		betting0, betting1 = betting.split('/')
	betting0 = re.findall(r'(\D{1}\d*)', betting0)
	betting1 = re.findall(r'(\D{1}\d*)', betting1) if betting1 else []
	return (betting0, betting1)

def main(server_output):
	games = []
	with open(server_output, 'r') as file:
		for row in file:
			# arbitrarily choose player to parse
			if row.startswith('TO 1 at'):
				matchstate, position, hand_num, betting, cards = row.split(':')
				cards = parse_cards(cards)
				betting = parse_betting(betting)		
				if isTerminal(cards, betting):
					game = get_stats(position, cards, betting)
					print(game.p1_pfr, game.p2_pfr, game.p1_vpip, game.p2_vpip, game.pot_size, game.winner)
					games.append(game)

		values = [0, 0, 0, 0, 0, 0]
		for game in games:
			print(game.p1_pfr)
			values[0] += game.p1_pfr
			values[1] += game.p2_pfr
			values[2] += game.p1_vpip
			values[3] += game.p2_vpip
			values[4] += game.pot_size
			values[5] += game.winner
	print("\np1pfr, p2pfr, p1vpip, p2vpip, potsize, winner:")
	print(values)
	print("\naverage over",len(games),"games:")
	print([values[i]/len(games) for i in range(len(values))])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python GameStatistics.py {server_output}")
        sys.exit(1)

    main(sys.argv[1])
