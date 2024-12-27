"""Lists exec from PCC."""
import random
from unittest import result


def list_of_guest(invites: list) -> None:
    """
    Create list of guests.

    When invites guest.
    """
    for guest  in invites:
        print(f"Hello, {guest}, you are invited to join PCC.!")


def list_of_guest_corrected(invites: list, new_guest: str) -> None:
    """
    Create list of guests corrected.

    One guest, cannot be, we should replace him.
    """
    removed_guest = invites.pop(random.randint(0, len(invites) - 1))
    print(f"Guest {removed_guest} is deleted!")

    invites.append(new_guest)
    print("\n".join(f"Hello, {guest}, you are invited to join PCC!" for guest in invites))


def adding_more_guest_to_list(invites: list, people_to_add: list):
    """
    Create list of guests.

    add more guests to list.
    :param people_to_add:
    :param invites:
    :return: None
    """
    invites.insert(0, people_to_add[0])
    invites.insert(2, people_to_add[1])
    invites.append(people_to_add[2])
    print("\n".join(f"Hello, {guest}, you are invited to join PCC!" for guest in invites))
    return invites


def deleting_all_from_list(invites:list, people_to_ad: list) -> None:
    result = adding_more_guest_to_list(invites, people_to_ad)
    for guest in result:
        print(f"Giest: {guest}, you are invited to join PCC!")

    print(f"There are too many guests to join PCC! Amount is {len(invites)}")

    while len(result) > 2:
        removed_guest = result.pop()
        print(f"Removed guest: {removed_guest}")

    print("PCC is good, I will delete all of you...")
    while result:
        del result[0]

    print(f"Let's print our result {result}")

if __name__ == '__main__':
    list_of_guest(["Petrov Mireko", "Arjton Kovabango", "Iremar Bilbo"])
    list_of_guest_corrected(["Petrov Mireko", "Arjton Kovabango", "Iremar Bilbo"], "Bilos Trav")
    adding_more_guest_to_list(["Petrov Mireko", "Arjton Kovabango", "Iremar Bilbo"], ["Mikla Sirinkov", "Zelezni Krai", "Genadi Grozny"])
    deleting_all_from_list(["Petrov Mireko", "Arjton Kovabango", "Iremar Bilbo"], ["Mikla Sirinkov", "Zelezni Krai", "Genadi Grozny"])