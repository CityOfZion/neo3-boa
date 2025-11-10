from boa3.sc.compiletime import public


class Example:
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris tempus accumsan imperdiet. Pellentesque vel augue
    ipsum. Morbi at varius enim. Praesent eu elit id metus tincidunt pharetra eu pharetra diam. Cras ac imperdiet lacus.
    Nullam dapibus tellus vel neque malesuada, non egestas orci lobortis. Curabitur et blandit lorem. Nunc luctus
    sollicitudin elit ac molestie. Maecenas nec pulvinar justo. Vestibulum sed justo bibendum, gravida ipsum at,
    maximus eros. Vivamus a volutpat lorem. Sed id ligula sit amet eros mollis luctus. Quisque at auctor erat.
    Curabitur dui turpis, tincidunt a eros eu, tempor consectetur ex. In eget justo ac odio molestie pharetra id
    feugiat leo.
    """
    123456
    True
    False
    b'Lorem ipsum dolor sit amet, consectetur adipiscing elit'

    @staticmethod
    def return_1() -> int:
        return 1


@public
def main() -> int:
    return Example.return_1()
