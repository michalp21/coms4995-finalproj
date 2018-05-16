from deuces2.card import Card
from InfoSet import InfoSet
from Strategy import Strategy
import pickle
import csv

# Credit: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

# Print iterations progress
length = 50

def printProgressBar (iteration, total):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:.1f}%").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = u"♣" * filledLength + '-' * (length - filledLength)
    print(('\r Iter %d/%d |%s| %s Complete' % (iteration, total, bar, percent)), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

#Credit: https://stackoverflow.com/questions/42653386/does-pickle-randomly-fail-with-oserror-on-large-files?rq=1
def save_as_pickled_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])

def try_to_load_as_pickled_object_or_None(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    try:
        input_size = os.path.getsize(filepath)
        bytes_in = bytearray(0)
        with open(filepath, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        obj = pickle.loads(bytes_in)
    except:
        return None
    return obj


def repr_board(board):
    return repr([[Card.int_to_str(c) for c in round_cards] for round_cards in board])

def repr_hole(hole):
    return repr([Card.int_to_str(c) for c in hole])

def repr_bets(bets):
    return ':'.join(
        [','.join(str(h) for h in bets[k])for k in sorted(bets)])