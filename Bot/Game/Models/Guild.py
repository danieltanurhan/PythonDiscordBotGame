from typing import Dict, List

class Guild:
    def __init__(self, discord_server_id: str, name: str):
        self.discord_server_id = discord_server_id
        self.name = name
        self.members: List[str] = []  # List of member_ids
        self.join_requests: List[str] = []  # List of player_ids who requested to join

    def to_dict(self) -> Dict:
        return {
            "discord_server_id": self.discord_server_id,
            "name": self.name,
            "members": self.members,
            "join_requests": self.join_requests
        }

    @classmethod
    def from_dict(cls, data: Dict):
        guild = cls(data['discord_server_id'], data['name'])
        guild.members = data.get('members', [])
        guild.join_requests = data.get('join_requests', [])
        return guild

    def add_member(self, member_id: str):
        if member_id not in self.members:
            self.members.append(member_id)

    def remove_member(self, member_id: str):
        if member_id in self.members:
            self.members.remove(member_id)

    def add_join_request(self, player_id: str):
        if player_id not in self.join_requests:
            self.join_requests.append(player_id)

    def remove_join_request(self, player_id: str):
        if player_id in self.join_requests:
            self.join_requests.remove(player_id)