from Header import JoinGroup, LeaveGroup

if __name__ == '__main__':
    option = int(input("Press 1 to join or 0 to leave: "))
    if option:
        JoinGroup()
    else:
        LeaveGroup()
