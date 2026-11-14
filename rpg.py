def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(f"{self.name} -> {func.__name__}")
        return func(self, *args, **kwargs)
    return wrapper

class Character:
    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self.hp = hp
        self.level = level
        Character.count += 1

    @classmethod
    def from_string(cls, text):
        name, hp = text.split(":")
        return cls(name, int(hp))

    @staticmethod
    def is_valid_name(name):
        return len(name) >= 2 and len(name) <= 20

    def __eq__(self, other):
        if not isinstance(other, Character):
            return False       #self.level   #self.level
        return          self.name == other.name 

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    @property #chatgpts davawerine(ar vici ras nishnavs)
    def is_alive(self):
        return self.hp > 0

    @log_action
    def attack(self, target):
        target.take_damage(5)

class Inventory:
    def __init__(self):
        self.items = []

    def add(self, **item):
        self.items.append(item)

    def find(self, **filters):
        return [item for item in self.items
                if all(item.get(key) == value
                for key, value in filters.items())]
    def __len__(self):
        return len(self.items)


class Warrior(Character):
    def __init__(self, name, hp=100, strength=10):
        super().__init__(name, hp)
        self.strength = strength

    @log_action
    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):
    def __init__(self, name, hp=100, mana=50):
        super().__init__(name, hp,)
        self.mana = mana

    @log_action
    def attack(self, target):
        if self.mana >= 10:
            target.take_damage(20)
            self.mana -= 10
        else:
            super().attack(target)

    def __str__(self):
        return f"{super().__str__()} MN {self.mana}"

class Priest(Character):
    def __init__(self, name, hp=100):
        super().__init__(name, hp)

    @log_action
    def heal(self, target, amount):
        target.hp += amount

def battle(a, b):
    while a.is_alive and b.is_alive:
        a.attack(b)

        if not b.is_alive:
            break

        b.attack(a)

    if a.is_alive:
        return a
    return b        


inv = Inventory()
inv.add(name="sword", kind="weapon", power=10)
inv.add(name="potion", kind="heal", power=30)

print(len(inv))                  # 2
print(inv.find(kind="weapon"))   # [{'name': 'sword', 'kind': 'weapon', 'power': 10}]
print(inv.find(kind="heal", power=30))   # [{'name': 'potion', 'kind': 'heal', 'power': 30}]

# t = Warrior("Tariel")
# n = Mage("Nestan")
# t.attack(n)                      # Tariel → attack


fight_winner = battle(
    Warrior("Tariel", hp=150),
    Mage("Nestan", hp=100)
)

print(f"გამარჯვებულია: {fight_winner}")