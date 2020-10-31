from telethon.errors.rpcerrorlist import PhoneCodeInvalidError, PhoneCodeExpiredError
from Header import CreateSimList, ClientConnect
from colorama import Fore

sim_cards = CreateSimList()  # reads the sim cards from the list
i = 0

while i < len(sim_cards):
    try:
        ClientConnect(sim_cards[i])
        i += 1

    except PhoneCodeInvalidError:
        print(Fore.RED + "Code Invalid! Try Again")

    except PhoneCodeExpiredError:
        print(Fore.RED + "Code expired after 5 minutes! Try Again")
