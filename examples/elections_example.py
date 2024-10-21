from hypixel_api_lib.Elections import *

e = Elections()

# current election candidates in order of votes
current = e._current
candidates = sorted([i for i in current._candidates], key = lambda x: x._votes, reverse=True)
for i in candidates:
    print(i)


curr_minister = e._mayor._minister

print("Minister name: %s" % curr_minister._name)
print("Minister perk %s" % curr_minister._perk.description)

# view details of last election
last = e._mayor._election
print("Last election year: %d" % last._year)
candidates = sorted([i for i in last._candidates], key = lambda x: x._votes, reverse=True)
for i in candidates:
    print(i)



