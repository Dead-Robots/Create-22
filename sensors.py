from createserial.createCommands import read_cliff_signals


def read_cliffs():
    right_cliff_sig, left_cliff_sig = read_cliff_signals()
    print("Right: ", right_cliff_sig, "Left: ", left_cliff_sig)
    return right_cliff_sig, left_cliff_sig