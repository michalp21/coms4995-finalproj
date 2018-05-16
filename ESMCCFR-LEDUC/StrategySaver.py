from InfoSet import InfoSet
from Strategy import Strategy
import csv

def save(filename, infoset_strategy_map):
	with open(filename, 'w') as f:

		writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONE)
		count = 1
		for infoset, v in infoset_strategy_map.items():
			row = _write_row(infoset, v)
			assert _read_row(row)[0] == infoset
			writer.writerow(row)
			print("  Saving csv %d" % (count), end='\r')
			if count % 10000 == 0:
				f.flush()
			count += 1
		f.flush()
		print("csv Saved")

def load(filename):
	infoset_strategy_map = {}
	with open(filename, 'r') as f:
		reader = csv.reader(f, delimiter=';')
		i = 1
		for row in reader:
			infoset, strategy = _read_row(row)
			infoset_strategy_map[infoset] = strategy
			print("  Loading csv", i, end='\r')
			i += 1
		print("csv Loaded")

	#Print Infosets
	# infosets = []
	# for k,v in infoset_strategy_map.items():
	# 	infosets.append((k,v.get_average_strategy(),v.count,v.regret_sum))
	# for i in sorted(infosets, key=lambda j: j[0]):
	# 	print(i[0],i[1])

	return infoset_strategy_map

def _write_row(infoset, v):
	return [infoset.hole,
			infoset.board,
			_comma_join(infoset.bets_0),
			_comma_join(infoset.bets_1),
			_comma_join('%d' % (100000 * round(k, 5)) for k in v.get_average_strategy())]

def _read_row(row):
	hole = int(row[0])
	board = row[1]
	if board == 0:
		board = ()
	else:
		board = ((int(board),),)
	bets_0 = _comma_split_int(row[2])
	bets_1 =_comma_split_int(row[3])

	infoset = InfoSet((hole,), board, (bets_0, bets_1))

	strategy = Strategy(0)
	strategy.average_strategy = [float(x)/100000 for x in _comma_split_int(row[4])]
	sum_strategy = sum(strategy.average_strategy)
	for s in strategy.average_strategy:
		s /= sum_strategy

	return infoset, strategy


def _comma_join(arr):
	return ','.join([str(a) for a in arr])

def _comma_split_int(str):
	if str == '':
		return []
	return [int(s) for s in str.split(',')]