import datetime
import time
import traceback
from colorama import Fore
from telethon.errors.rpcerrorlist import UserDeactivatedBanError, UserBannedInChannelError
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, \
    UserKickedError, UserAlreadyParticipantError, ChannelPrivateError, UsernameNotOccupiedError, ChannelInvalidError
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import UserStatusOnline
import random

# the group link, message, and the sim card list
link = 't.me/AliensGreen'
message_group_link = 't.me/bombasim'
sim_cards = [[1758569, '95e520b2fb86aafc53abbb24f5babe0a', '+972547465096', 'h22 mikro'],
             [1412506, 'b893435e54d384918aac832d8535650b', '+972543559332', 'h25 hayal'],
             [1422406, '56158792ced2a5c8a4fab80245ba7ec7', '+972547290956', 'h26 nesha'],
             [1492448, 'e35f5cd79232520ee0c73efe5a21f70b', '+972547290946', 'h27 biki'],
             [1786235, '09b1f838ff53fbdb462e25eb08b6207b', '+972547290826', 'h28 htm'],
             [1750977, 'd98d97a75b1e1ba1658a1a236fdec130', '+972547286932', 'h29 yalda'],
             [1463313, '4f0f2cec4da663292d30b21f2f27c048', '+972543559745', 'h30 dana'],
             [1486928, '67177edef1735abd76cfd204fa89f78f', '+972547681513', 'h31 hallo'],
             [1796998, '762999cb9097448891d304dcd8f8c0e1', '+972547287443', 'h33 nimar'],
             [1714830, '4919e5570f2fdf14f4661ca4763be928', '+972542916125', 'h34 boaz'],
             [1620491, '69eba10984f8127ec1b46b8f2472f962', '+972547681472', 'h36 barad'],
             [1760057, 'ae70777cede95bc6b3ec11731e70fd95', '+972547683860', 'h38 osa'],
             [1459033, '5c38e0d1d01d512f3cc3d7be479d9112', '+972547291206', 'h39 olala'],
             [1764509, 'b25757b99256eb64808c0ebe493af43d', '+972547291061', 'h40 bseder'],
             [1790300, '6998750254adf644047e77128bff932c', '+972547291043', 'h41 hoged'],
             [1474073, 'e7465f1c304ca154f3940923d3e8c45c', '+972547680593', 'h42 dedi'],
             [1455650, 'd8f6f66be5c287514a598cbaf05e279e', '+972547685362', 'h44 ha'],
             [1608768, 'f55081187befc3dfdc6e0cd1c4982dec', '+972547688964', 'h45 tel'],
             [1464864, '1d03101a7feeee34377f24457958fe3c', '+972547465658', 'h46 ha'],
             [1497923, '4958f41a09c73ad6b439de0d6a565a3d', '+972543559734', 'h47 vnik'],
             [1575934, '21816d06c04ebbb6b7be5ffc07ec6722', '+972547681250', 'h48 dab'],
             [1440771, 'b5ff8f9778919eb51ce9924eccf35689', '+972549370481', 'h49 xman'],
             [1431701, '282b364b5ae14dea9f8e609752c385dd', '+972546803702', 'h50 fem'],
             [1574761, '6a846abe4ad0cf06869b1504af6e67ff', '+972543094476', 'h51 dara'],
             [1596788, 'a6541ceed220e92a0a410037c27731a9', '+972546165599', 'h52 lamo'],
             [1466138, '3117cb15a5ad922d3572172333ab1288', '+972549059087', 'h53 zana'],
             [1607836, '6c49c8a55ad1b054563fdbdb8788c691', '+972544743047', 'h54 magi']
             ]

# the initial connection to get the list
main_phone = sim_cards[0]
first_client = TelegramClient(main_phone[2], main_phone[0], main_phone[1])
first_client.connect()

# gets the messages
print("Getting messages..")
message_entity = first_client.get_entity(message_group_link)
messages = first_client.get_messages(message_entity)

print("Scraping Members!")
# joins the group and gets the entity
group_entity = first_client.get_entity(link)
first_client(JoinChannelRequest(group_entity))

# gets the group list
group_participants = first_client.get_participants(group_entity, aggressive=True)

# don't need him anymore, disconnect
first_client.disconnect()
del first_client

# start and end date for filter
start_date = datetime.datetime(2020, 7, 17, 1, 1, 1, tzinfo=datetime.timezone.utc)
end_date = datetime.datetime(2020, 7, 22, 1, 1, 1, tzinfo=datetime.timezone.utc)

final_participants = []

# filter the bots and non active members from the group
print("Filtering Members..")
for user in group_participants:
    if user.username is not None:
        if not user.bot:  # if its a bot
            if hasattr(user.status, 'was_online') and start_date < user.status.was_online < end_date:
                final_participants.append(user)
            elif type(user.status) == UserStatusOnline:
                final_participants.append(user)

# loops over the whole participants
i = 0
message_counter = 0  # counts how many messages has been sent
for j in range(20):  # send a message from every sim and run 40 times on the whole list
    for sim in sim_cards:

        # connect to sim
        api_id = sim[0]
        api_hash = sim[1]
        phone = sim[2]

        try:
            client = TelegramClient(phone, api_id, api_hash)
            client.connect()

        except PhoneNumberBannedError:
            print(Fore.BLUE + "Phone {} banned cant connect! skipping ..".format(sim.name))
            sim_cards.remove(sim)
            time.sleep(2)
            continue

        # keeping count how many left
        print("The amount of users left is: {}".format(len(final_participants) - i))

        # loop through every sim send 1 message and go to the next
        while True:
            if i == len(final_participants):
                print("GROUP IS EMPTY! EXITING")
                exit(1)
            try:
                message = random.choice(messages)  # a random message
                entity = client.get_entity(message_group_link)  # the group where the message came from
                receiver = client.get_input_entity(final_participants[i].username)  # the reciever entity
                client.forward_messages(receiver, messages=message.id, from_peer=entity, silent=True)
                print(Fore.GREEN + "Sending message to {} from {}".format(final_participants[i].username, sim.name))
                client.disconnect()
                del client
                message_counter += 1
                i += 1
                break

            except PeerFloodError:
                sim_cards.remove(sim)  # if flood error remove from the list
                print(Fore.WHITE + "Sim {} get Flood Error. Deleting Him.. skipping".format(sim.name))
                client.disconnect()
                del client
                break

            except ValueError:
                print(Fore.RED + "Value Error! skipping user.. ")
                i += 1

            except UsernameNotOccupiedError:
                print(Fore.RED + "Can't find username! skipping user.. ")
                i += 1

            except UserPrivacyRestrictedError:
                print(Fore.RED + "The user's privacy settings do not allow you to do this. Skipping.")
                i += 1

            except UserAlreadyParticipantError:
                print(Fore.RED + "User is already in the Group! Skipping.")
                i += 1

            except UserKickedError:
                print(Fore.RED + "User got kicked from th Group! Skipping.")
                i += 1

            except UserNotMutualContactError:
                print(Fore.RED + "User is not mutual contact! Skipping..")
                i += 1

            except ChannelPrivateError:
                print(Fore.RED + "The group is private or sim {} got BANNED!. Skipping..".format(sim.name))
                i += 1

            except ChannelInvalidError:
                print(Fore.RED + "Invalid user! skipping..")
                i += 1

            except UserDeactivatedBanError:
                print(Fore.BLACK + "Phone got banned.. Skipping sim..")
                time.sleep(2)
                break

            except PhoneNumberBannedError:
                print("Phone NUMBER has been banned!")
                sim_cards.remove(sim)
                time.sleep(2)
                break

            except UserBannedInChannelError:
                print(Fore.BLUE + "Phone {} BANNED IN CHANNEL! skipping ..".format(sim.name))
                sim_cards.remove(sim)
                time.sleep(2)
                break

            except:
                traceback.print_exc()
                print(Fore.RED + "Unexpected Error")
                client.disconnect()
                del client
                break
    print(Fore.LIGHTBLACK_EX + "Loop Number: {}. Messages sent: {}".format(j + 1, message_counter))
    print("Sleeping 90 seconds ..")
    time.sleep(90)
