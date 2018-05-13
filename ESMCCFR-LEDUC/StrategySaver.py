from InfoSet import InfoSet
from Strategy import Strategy
import csv

def save(filename, infoset_strategy_map):
	with open(filename, 'w') as f:
		writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_NONE)
		infosets = [(k, v.get_average_strategy(), v.count, v.regret_sum) for k,v in self.infoset_strategy_map.items()]
		for count, i in enumerate(infosets):
			infoset = i[0]
			writer.writerow([infoset.hole,
				infoset.board,
				_comma_join(infoset.bets_0),
				_comma_join(infoset.bets_1),
				_comma_join(['%d' % (1000 * round(k, 3)) for k in i[1]])])
			if count % 10000 == 0:
				print("Flushing %d / %d" % (count, len(infosets)))
				f.flush()
		f.flush()

def load(filename):
	infoset_strategy_map = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		i = 1
		for row in reader:
			hole = row[0]
			board = row[1]
			bets_0 = _comma_split_int(row[2])
			bets_1 = _comma_split_int(row[3])

			board = () if cards <= 3 else (cards // 3,)
			hole = cards % 3
			infoset = InfoSet(hole, board, (bets_0, bets_1))

			strategy = Strategy(0)
			strategy.average_strategy = [float(x)/1000 for x in _comma_split_int(row[4])]
			sum_strategy = sum(strategy.average_strategy)
			for s in strategy.average_strategy:
				s /= sum_strategy

			infoset_strategy_map[infoset] = strategy
			print(" ", i, end='\r')
			i += 1
	return infoset_strategy_map



def _comma_join(arr):
	return ','.join([str(a) for a in arr])

def _comma_split_int(str):
	return [int(s) for s in str.split(',')]