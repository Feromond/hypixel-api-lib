from hypixel_api_lib.Elections import Elections

elections = Elections()
current_mayor = elections.get_mayor()
current_election = elections.get_current_election()

print(f"Current Mayor: {current_mayor}")
print(f"Current Election: {current_election}")

# List all candidates in the current election
for candidate in current_election.candidates:
    print(candidate)

print(f"Current Mayor: {current_mayor.name}")
ministers = current_mayor.get_ministers()
if ministers:
    print("Current Ministers and their perks:")
    for candidate, perks in ministers:
        print(f"Minister {candidate.name}:")
        for perk in perks:
            print(f"  - {perk.name}: {perk.description}")
else:
    print("No ministers in the current mayor's term.")

sorted_candidates = current_election.get_candidates_by_votes()
print(f"Candidates for Election Year {current_election.year} sorted by votes:")
for candidate in sorted_candidates:
    print(f"{candidate.name} - {candidate.votes} votes")

# Get a candidate by name
finnegan = current_election.get_candidate_by_name('Finnegan')
print(f"Candidate Finnegan's perks:")
for perk in finnegan.perks:
    print(perk)


