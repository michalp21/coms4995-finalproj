from deuces2.card import Card

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
    percent = ("{0:.1f}%%").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(('\rIter %d/%d |%s| %s Complete' % (iteration, total, bar, percent)), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def repr_board(board):
    return repr([[Card.int_to_str(c) for c in round_cards] for round_cards in board])

def repr_hole(hole):
    return repr([Card.int_to_str(c) for c in hole])

def repr_history(history):
    return ':'.join(
        [','.join(str(h) for h in history[k])for k in sorted(history)])