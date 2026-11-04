BEATS = {"R": "P", "P": "S", "S": "R"}   # BEATS[x] = the move that beats x
MOVES = ["R", "P", "S"]
DECAY = 0.9

# ---- experts: each predicts the opponent's NEXT move ----
def quincy(me, opp):
    choices = ["R", "R", "P", "P", "S"]
    return choices[(len(opp) + 1) % 5]

def kris(me, opp):
    return BEATS[me[-1]] if me else "P"

def mrugesh(me, opp):
    if not me:
        return "R"
    recent = me[-10:]
    return BEATS[max(MOVES, key=recent.count)]

def abbey(me, opp):
    seq = ["R"] + me                      # Abbey seeds its history with "R"
    counts = {a + b: 0 for a in MOVES for b in MOVES}
    for a, b in zip(seq, seq[1:]):
        counts[a + b] += 1
    last = seq[-1]
    predicted_mine = max(MOVES, key=lambda m: counts[last + m])  # ties -> R,P,S
    return BEATS[predicted_mine]

EXPERTS = {"quincy": quincy, "kris": kris, "mrugesh": mrugesh, "abbey": abbey}

# ---- persistent state (module level, so it survives between calls) ----
S = {"me": [], "opp": [], "score": {}, "last": {}}

def _reset():
    S["me"], S["opp"] = [], []
    S["score"] = {name: 0.0 for name in EXPERTS}
    S["last"] = {}

_reset()

def player(prev_play):
    if prev_play == "":                    # new match
        _reset()
    else:
        S["opp"].append(prev_play)
        # decayed reward/penalty for each expert's previous prediction
        for name, pred in S["last"].items():
            S["score"][name] = DECAY * S["score"][name] + (1 if pred == prev_play else -1)

    me, opp = S["me"], S["opp"]
    S["last"] = {name: f(me, opp) for name, f in EXPERTS.items()}

    best = max(S["score"], key=S["score"].get)
    my_move = BEATS[S["last"][best]]

    me.append(my_move)
    return my_move