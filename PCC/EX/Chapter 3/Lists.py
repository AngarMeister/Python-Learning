"""Lists exec from PCC."""

def list_of_guest(invites: list) -> None:
    """
    Create list of guests.

    When invites guest.
    """
    for guest  in invites:
        print(f"Hello, {guest}, you are invited to join PCC.!")


if __name__ == '__main__':
    list_of_guest(["Petrov Mireko", "Arjton Kovabango", "Iremar Bilbo"])