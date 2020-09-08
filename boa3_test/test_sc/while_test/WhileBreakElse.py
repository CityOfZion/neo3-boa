def Main() -> int:
    a = 0
    b = 0
    sequence = (3, 5, 15)

    while a < len(sequence):
        x = sequence[a]
        a += 1

        if x % 5 == 0:
            b += x
            break

        b += 1
    else:
        b = -1

    return b
