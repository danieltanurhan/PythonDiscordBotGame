from typing import Dict, List
from datetime import datetime, timezone
from Game.Models.Player import Player

class Guild:
    def init(self, id: str, name: str):
        self.id = id
        self.name = name
        self.created_at = datetime.now(timezone.utc)
        self.description = ""
        self.members: List[str] = []  # List of member_ids
        self.leader_id = None
        self.join_requests: List[str] = []  # List of player_ids who requested to join

    def __init__(self, id: str, name: str, created_at: datetime = datetime.now(timezone.utc), description: str = "", leader_id: str = None, members: List[str] = []):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.description = description
        self.leader_id = leader_id
        self.members = members
        self.join_requests: List[str] = []  # List of player_ids who requested to join

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "description": self.description,
            "leader_id": self.leader_id,
            "members": self.members,
            "join_requests": self.join_requests
        }

    @classmethod
    def from_dict(cls, data: Dict):
        guild = cls(
            id=data['id'],
            name=data['name'],
            created_at=data['created_at'],
            description=data.get('description', ""),
            leader_id=data.get('leader_id'),
            members=data.get('members', [])
        )
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