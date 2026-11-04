def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    if len(opponent_history) < 2:
        return "R"

    # Predict the opponent's next move based on previous patterns
    last_two = "".join(opponent_history[-2:])

    # Counter the most likely next move
    counter = {"R": "P", "P": "S", "S": "R"}

    # Look for patterns in the opponent's history
    patterns = {}
    for i in range(len(opponent_history) - 2):
        pattern = "".join(opponent_history[i:i + 2])
        next_move = opponent_history[i + 2]

        if pattern not in patterns:
            patterns[pattern] = {"R": 0, "P": 0, "S": 0}

        patterns[pattern][next_move] += 1

    if last_two in patterns:
        predicted_move = max(patterns[last_two], key=patterns[last_two].get)
        return counter[predicted_move]

    # Fallback strategy
    most_common = max(set(opponent_history), key=opponent_history.count)
    return counter[most_common]
