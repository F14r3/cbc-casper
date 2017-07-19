from settings import ESTIMATE_SPACE, WEIGHTS, VALIDATOR_NAMES
import random as r
import copy


def get_max_weight_indexes(scores):

    max_score = 0
    max_score_estimate = None
    for e in scores.keys():
        if max_score == 0:
            max_score = scores[e]

        if scores[e] > max_score:
            max_score = scores[e]

    max_weight_estimates = set()

    for e in scores.keys():
        if scores[e] == max_score:
            max_weight_estimates.add(e)

    return max_weight_estimates


def get_favorite_child_of_block(block, children, latest_messages):

    scores = dict()
    for child in children[block]:
        scores[child] = 0

    memo = set()
    for child in children[block]:
        for v in latest_messages.keys():
            if v in memo:
                continue
            if child.is_in_blockchain(latest_messages[v]):
                scores[child] += WEIGHTS[v]

    max_weight_children = get_max_weight_indexes(scores)

    c = r.choice(tuple(max_weight_children))
    print "c:--------", len(max_weight_children)
    return c


def get_fork_choice(last_finalized_block, children, latest_messages):

    best_block = last_finalized_block
    while(best_block in children.keys()):
        best_block = get_favorite_child_of_block(best_block, children, latest_messages)

    return best_block


def get_estimate_from_latest_bets(latest_bets, default=None):
    estimates = []
    for v in latest_bets:
        if latest_bets[v].estimate not in estimates:
            estimates.append(latest_bets[v].estimate)

    scores = dict()
    for e in estimates:
        scores[e] = 0

    for v in latest_bets:
        scores[latest_bets[v].estimate] += WEIGHTS[v]

    mwe = get_max_weight_estimates(scores)

    if default is not None:
        if default in mwe:
            return default

    if mwe == set():
        mwe = ESTIMATE_SPACE

    return r.choice(tuple(mwe))
