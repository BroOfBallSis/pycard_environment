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

    def get_colored_str(self, get_color=True) -> str:
        if self.mod_value < 0:
            real_value_str = center_text(f"{self.base_value}{self.mod_value}", 4)
            if get_color:
                real_value_str = color_text(f"{real_value_str}", "green")
        elif self.mod_value == 0:
            return center_text(f"{self.base_value}", 4)
        else:
            real_value_str = center_text(f"{self.base_value}+{self.mod_value}", 4)
            if get_color:
                real_value_str = color_text(f"{real_value_str}", "yellow")
        return real_value_str
               
    def __str__(self):
        return self.get_colored_str(get_color=False)


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
