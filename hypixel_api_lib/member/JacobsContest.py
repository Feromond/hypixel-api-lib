class JacobsContestEntry:
    """
    Represents a single Jacob's Contest entry.

    Attributes:
        contest_id (str): The unique identifier for the contest.
        collected (int): The number of items collected during the contest.
        claimed_rewards (bool): Whether the rewards have been claimed.
        claimed_position (int or None): The player's position in the contest.
        claimed_participants (int or None): The total number of participants.
        claimed_medal (str or None): The medal claimed ('bronze', 'silver', etc.), if any.
    """

    def __init__(self, contest_id, data):
        self.contest_id = contest_id
        self.collected = data.get('collected', 0)
        self.claimed_rewards = data.get('claimed_rewards', False)
        self.claimed_position = data.get('claimed_position')
        self.claimed_participants = data.get('claimed_participants')
        self.claimed_medal = data.get('claimed_medal')

    def __str__(self):
        return (f"Contest ID: {self.contest_id}, Collected: {self.collected}, "
                f"Position: {self.claimed_position}, Medal: {self.claimed_medal}")

    def __repr__(self):
        return self.__str__()
    

class JacobsContestData:
    """
    Represents the Jacob's Contest data for a SkyBlock profile member.

    Attributes:
        medals_inv (dict of str to int): Inventory of medals ('bronze', 'silver', 'gold').
        perks (dict): Perks related to Jacob's Contest.
        contests (dict of str to JacobsContestEntry): Dictionary of contest entries.
        talked (bool): Whether the player has talked to Jacob.
        personal_bests (dict of str to int): Personal best scores for each crop.
        unique_brackets (dict of str to list of str): Unique brackets achieved.
    """

    def __init__(self, data):
        self.medals_inv = data.get('medals_inv', {})
        self.perks = data.get('perks', {})
        self.talked = data.get('talked', False)
        self.personal_bests = data.get('personal_bests', {})
        self.unique_brackets = data.get('unique_brackets', {})

        contests_data = data.get('contests', {})
        self.contests = {
            contest_id: JacobsContestEntry(contest_id, contest_info)
            for contest_id, contest_info in contests_data.items()
        }

    def __str__(self):
        medals = ', '.join(f"{medal}: {count}" for medal, count in self.medals_inv.items())
        return (f"JacobsContestData(Medals: {medals}, "
                f"Contests Participated: {len(self.contests)}, Talked: {self.talked})")
