S_ALONE = 0
S_TALKING = 1

# ==============================================================================
# Group class:
# member fields:
#   - An array of items, each a Member class
#   - A dictionary that keeps who is a chat group
# member functions:
#    - join: first time in
#    - leave: leave the system, and the group
#    - list_my_peers: who is in chatting with me?
#    - list_all: who is in the system, and the chat groups
#    - connect: connect to a peer in a chat group, and become part of the group
#    - disconnect: leave the chat group but stay in the system
# ==============================================================================
import copy

class Group:

    def __init__(self):
        self.members = {} # {name1: state1, name2: state2, ...}
        self.chat_grps = {} # {1: [name1, name2], 2: [a, b, c], ...}
        self.grp_ever = 0

    def join(self, name):
        self.members[name] = S_ALONE
        return

    def is_member(self, name):

        # IMPLEMENTATION
        '''return True if name is in members, False otherwise'''
        # ---- start your code ---- #
        if name in self.members:
            return True
        return False
        # ---- end of your code --- #

    # implement
    def leave(self, name):
        """
        leave the system,
        remove name from members and the group
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        self.disconnect(name)
        if self.is_member(name):
            self.members.pop(name)
        # ---- end of your code --- #
        return


    def find_group(self, name):
        """
        Auxiliary function internal to the class; return two
        variables: whether "name" is in a group, and if true
        the key to its group
        """

        found = False
        group_key = 0
        # IMPLEMENTATION
        # ---- start your code ---- #
        found = self.members[name] == 1
        if found:
            for i in self.chat_grps.keys():
                if name in self.chat_grps[i]:
                    group_key = i
                    break
        # ---- end of your code --- #
        return found, group_key




    def connect(self, me, peer):
        """
        me is alone, connecting peer.
        if peer is in a group, join it
        otherwise, create a new group with you and your peer
        """
        peer_in_group, group_key = self.find_group(peer)

        # IMPLEMENTATION
        # ---- start your code ---- #
        self.members[me] = 1
        search = self.find_group(peer)
        if search[0]:
            self.chat_grps[search[1]].append(me)
        else:
            self.members[peer] = 1
            i = 1
            while True:
                if i not in self.chat_grps.keys():
                    self.chat_grps[i] = [me, peer]
                    break
                i += 1
            self.grp_ever += 1
        # ---- end of your code --- #
        return

    # implement
    def disconnect(self, me):
        """
        find myself in the group, quit, but stay in the system

        Remove "me" from my current chat group.
        If the group has only one peer left,
        remove that peer as well, and delete the chat group.
        """
        # IMPLEMENTATION
        # ---- start your code ---- #
        search = self.find_group(me)
        if search[0]:
            self.chat_grps[search[1]].remove(me)
            if len(self.chat_grps[search[1]]) == 1:
                self.disconnect(self.chat_grps[search[1]][0])
            elif len(self.chat_grps[search[1]]) == 0:
                self.chat_grps.pop(search[1])
        self.members[me] = 0
        # ---- end of your code --- #
        return

    def list_all(self):
        # a simple minded implementation
        full_list = "Users: ------------" + "\n"
        full_list += str(self.members) + "\n"
        full_list += "Groups: -----------" + "\n"
        full_list += str(self.chat_grps) + "\n"
        full_list += "Loners: -----------\n"
        full_list += str(self.find_loners())+"\n"
        full_list += "Largest Group(s): -----------\n"
        full_list += str(self.find_largest_group())+"\n"
        return full_list

    # implement
    def list_me(self, me):
        """
        Return the chat group which "name" is in, as a list.
        IMPORTANT: "name"  is the first element in that returning list.
        (hint: use find_group)
        """
        my_list = []
        # IMPLEMENTATION
        # ---- start your code ---- #
        my_list = [me]
        search = self.find_group(me)
        if search[0]:
            my_list.append(self.chat_grps[search[1]])
        # ---- end of your code --- #
        return my_list

    #Improvement: find the number of loners
    def find_loners(self):
        count = 0
        for i in self.members.keys():
            count += self.members[i]
        return len(self.members) - count
    
    #Improvement: find the largest groups:
    def find_largest_group(self):
        hi_len = 0
        hi_grp = []
        for i in self.chat_grps:
            if len(self.chat_grps[i]) > hi_len:
                hi_len = len(self.chat_grps[i])
                hi_grp = [self.chat_grps[i][:]]
            elif len(self.chat_grps[i]) == hi_len:
                hi_grp.append(self.chat_grps[i])
        return hi_grp
    
    #improvement: find the groups with n members:
    def find_grp_based_on_size(self,n):
        result = []
        for i in self.chat_grps:
            if len(self.chat_grps[i]) == n:
                result.append(self.chat_grps[i])
        return result

if __name__ == "__main__":
    g = Group()
    g.join('a')
    g.join('b')
    g.join('c')
    g.join('d')
    g.join('e')
    g.join('f')
    g.connect("e","f")
    print(g.list_all())
    g.connect('a', 'b')
    print(g.list_all())
    print("listing groups with 2 members:", g.find_grp_based_on_size(2),"\n")
    g.connect('c', 'a')
    print(g.list_all())
    print("listing the groups c is in: \n",g.list_me("c"),"\n")
    g.leave('c')
    print(g.list_all())
    g.disconnect('b')
    print(g.list_all())
