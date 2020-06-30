def Main(number: int) -> int:
    if number % 3 == 1:
        return number - 1
    elif number % 2 == 1:
        number += 1  # the function doesn't have return in this case
    else:
        return number
