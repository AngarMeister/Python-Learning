"""It's a simple task with list and loops."""


def pizza(pizzas: list) -> None:
    """
    Small function to tell which pizza I like

    Really easy ex

    :param pizzas:
    :return: None
    """
    for pizza in pizzas:
        print(f"I love {pizza}")
    print("I really like all pizzas!")


def animals(animal: list) -> None:
    for loom in animal:
        print(f"I love {loom}")
    print("I really like all animals!")



if __name__ == '__main__':
    pizza(["Pepka", "Zerko", "Belko"])
    animals(["Pepka", "Zerko", "Belko"])