def get_estimate_from_latest_messages(latest_bets):
    sample_list = list(latest_bets.values())[0].estimate
    elem_weights = {elem: 0 for elem in sample_list}
    for validator in latest_bets:
        bet = latest_bets[validator]
        estimate = bet.estimate
        for i, elem in enumerate(estimate):
            elem_weights[elem] += validator.weight * (len(estimate) - i)

    return sorted(elem_weights, key=lambda elem: elem_weights[elem], reverse=True)
