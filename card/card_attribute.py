from utils.draw_text import center_text, color_text


class CardAttribute:
    def __init__(self, name: str, base_value, mod_value=0):
        self.name = name
        self.base_value = base_value
        self.mod_value = mod_value

    @property
    def real_value(self):
        return self.base_value + self.mod_value

    def increase_mod(self, amount):
        self.mod_value += amount

    def decrease_mod(self, amount):
        self.mod_value -= amount

    def set_mod(self, new_value):
        self.mod_value = new_value

    def __repr__(self):
        return f"CardAttribute(name={self.name!r}, base_value={self.base_value}, mod_value={self.mod_value})"

    def __str__(self):
        if self.mod_value < 0:
            return color_text(f"{self.base_value}{self.mod_value}", "green")
        elif self.mod_value == 0:
            return f"{self.base_value}"
        else:
            return color_text(f"{self.base_value}+{self.mod_value}", "yellow")


class CardAttributeFloat(CardAttribute):
    def __init__(self, name: str, base_value: float, mod_value: float = 0.0):
        super().__init__(name, base_value, mod_value)


class CardAttributeString(CardAttribute):
    def __init__(self, name: str, base_value: str, mod_value: str = ""):
        super().__init__(name, base_value, mod_value)

    @property
    def real_value(self):
        return self.base_value + self.mod_value

    def increase_mod(self, amount: str):
        self.mod_value += amount

    def decrease_mod(self, amount: str):
        self.mod_value = self.mod_value.replace(amount, "", 1)
