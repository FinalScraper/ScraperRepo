import time
import traceback
from colorama import Fore
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, \
    UserChannelsTooMuchError, UserKickedError, FloodWaitError, UserAlreadyParticipantError, ChannelPrivateError, \
    UsernameInvalidError, RpcCallFailError, UserDeactivatedBanError, UserBannedInChannelError, PhoneNumberBannedError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import PeerChannel
from telethon.errors.common import MultiError
from Header import Init, DeleteRow, isFull, JoinGroup, LeaveGroup, TOTAL_SLEEP_TIME

print("WELCOME TO FINAL SCRAPER!\n\n")
print("Add cards to target group? (if already in group type 0)")
option = int(input("Enter option (1/0): "))
if option:
    JoinGroup()
    time.sleep(10)
    print(Fore.BLUE + "\033[1m" + "\nSim cards are in the target group! starting FinalScraper...")

# Final Scraper #
flag = True
i, fe_count, ban_count = 0, 0, 0
while flag:
    try:
        cards, participants, TARGET_ID = Init()
        flag = False
    except MultiError:
        print("Initial Multi Error! Trying again in 20 seconds..")
        time.sleep(20)
        del cards, participants, TARGET_ID

for j in range(60):
    for sim in cards:
        if len(cards) < 10:
            print(Fore.RED + "NOT ENOUGH SIM CARDS! EXITING..")
            exit(1)
        try:
            client = TelegramClient(sim.phone, sim.ID, sim.name)
            client.connect()
            print(Fore.MAGENTA + f"Connected to {sim.name}")
            time.sleep(TOTAL_SLEEP_TIME / 2)

        except (PhoneNumberBannedError, UserBannedInChannelError, UserDeactivatedBanError) as e:
            print(Fore.BLUE + f"SIM {sim.name} GOT {type(e).__name__}! Deleting..")
            cards.remove(sim)
            ban_count += 1
            client.disconnect()
            del client
            DeleteRow(sim.phone)
            continue

        except (ConnectionError, RpcCallFailError):
            print("Connection Error! skipping sim..")
            continue

        # keeping count how many left
        print(Fore.GREEN + "The amount of users left is: {}".format(len(participants) - i))

        # for every sim add 1 user and go to the next
        while True:
            try:
                target_group = client.get_input_entity(PeerChannel(int(TARGET_ID)))  # the group to add to
                user_to_add = client.get_input_entity(participants[i].username)  # the user to add
                client(InviteToChannelRequest(target_group, [user_to_add]))
                print(Fore.GREEN + "Added member {} from sim {}".format(participants[i].id, sim.name))
                time.sleep(TOTAL_SLEEP_TIME / 2)
                if isFull(client, target_group):
                    print(Fore.BLUE + "TARGET GROUP IS FULL! PULLING OUT SIM CARDS..")
                    client.disconnect()
                    del client
                    LeaveGroup()
                    exit(0)
                client.disconnect()
                del client
                i += 1
                break

            except (PeerFloodError, FloodWaitError):
                print(Fore.WHITE + f"Sim {sim.name} get Flood Error .. Deleting ..")
                client.disconnect()
                del client
                cards.remove(sim)
                fe_count += 1
                i += 1
                time.sleep(TOTAL_SLEEP_TIME / 2)
                break

            except (ValueError, UserPrivacyRestrictedError, UserChannelsTooMuchError, UserAlreadyParticipantError,
                    UserKickedError, UserNotMutualContactError, ChannelPrivateError, UsernameInvalidError) as ex:
                print(Fore.RED + f"Can't add user! Error: {type(ex).__name__} ")
                i += 1

            except (UserDeactivatedBanError, PhoneNumberBannedError, UserBannedInChannelError) as ex:
                print(Fore.BLACK + f"SIM {sim.name} GOT {type(ex).__name__}!")
                cards.remove(sim)
                ban_count += 1
                client.disconnect()
                del client
                DeleteRow(sim.phone)
                time.sleep(TOTAL_SLEEP_TIME / 2)
                break

            except MultiError:
                client.disconnect()
                del client
                print("Multi error!.. waiting 12 seconds")
                time.sleep(12)
                break

            except IndexError:
                print(Fore.BLUE + "GROUP IS EMPTY! ENTER NEW LINK!\nEXITING..")
                client.disconnect()
                exit(1)

            except Exception:
                traceback.print_exc()
                print(Fore.RED + "Unexpected Error")
                client.disconnect()
                del client
                i += 1
                break

    print(Fore.YELLOW + "LOOP NUMBER {}. Sim cards left: {}\n"
                        "Flood Errors: {}. Bans: {}".format(j + 1, len(cards), fe_count, ban_count))
    time.sleep(TOTAL_SLEEP_TIME)
