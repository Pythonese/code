class Port(int):
    UNDEFINED = -1
    def __new__(cls, value):
        try:
            int(value)
        except:
            raise ValueError(f"invalid literal for Port(): '{value}'")
        return super().__new__(cls, value)

    def __init__(self, value):
        if self < 0:
            raise ValueError(f"negative port '{value}'")
        elif self > 65535:
            raise ValueError(f"too large port '{value}'")