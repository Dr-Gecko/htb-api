from typing import List

from . import htb
from .solve import MachineSolve


class Machine(htb.HTBObject):
    name: str = None
    os: str = None
    points: int = None
    release_date: str = None
    user_owns: int = None
    root_owns: int = None
    free: bool = None
    user_owned: bool = None
    root_owned: bool = None
    reviewed: bool = None
    stars: float = None
    avatar: str = None
    difficulty: str = None

    _detailed_attributes = ('active', 'retired', 'user_own_time', 'root_own_time', 'user_blood',
                            'root_blood', 'user_blood_time', 'root_blood_time')
    active: bool = None
    retired: bool = None
    difficulty_number: int = None
    completed: bool = None
    user_own_time: str = None
    root_own_time: str = None
    user_blood: MachineSolve = None
    root_blood: MachineSolve = None
    user_blood_time: str = None
    root_blood_time: str = None

    # noinspection PyUnresolvedReferences
    _authors: List["User"] = None
    _author_ids: List[int] = None

    # noinspection PyUnresolvedReferences
    @property
    async def authors(self) -> List["User"]:
        if not self._authors:
            self._authors = []
            for uid in self._author_ids:
                self._authors.append(await self._client.get_user(uid))
        return self._authors

    def __repr__(self):
        return f"<Machine '{self.name}'>"

    def __init__(self, data: dict, client: htb.HTBClient, summary: bool = False):
        self._client = client
        self._detailed_func = client.get_synchronous_machine
        self.id = data['id']
        self.name = data['name']
        self.os = data['os']
        self.points = data['points']
        self.release_date = data['release']
        self.user_owns = data['user_owns_count']
        self.root_owns = data['root_owns_count']
        self.user_owned = data['authUserInUserOwns']
        self.root_owned = data['authUserInRootOwns']
        self.reviewed = data['authUserHasReviewed']
        self.stars = float(data['stars'])
        self.avatar = data['avatar']
        self.difficulty = data['difficultyText']
        self.free = data['free']
        self._author_ids = [data['maker']['id']]
        if data['maker2']:
            self._author_ids.append(data['maker2']['id'])
        if not summary:
            self.active = bool(data['active'])
            self.retired = bool(data['retired'])
            self.user_own_time = data['authUserFirstUserTime']
            self.root_own_time = data['authUserFirstRootTime']
            if data['userBlood']:
                user_blood_data = {
                    "date": data['userBlood']['created_at'],
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "user"
                }
                self.user_blood = MachineSolve(user_blood_data, self._client)
                self.user_blood_time = data['userBlood']['blood_difference']
            if data['rootBlood']:
                user_blood_data = {
                    "date": data['rootBlood']['created_at'],
                    "first_blood": True,
                    "id": data['id'],
                    "name": data['name'],
                    "type": "root"
                }
                self.root_blood = MachineSolve(user_blood_data, self._client)
                self.root_blood_time = data['rootBlood']['blood_difference']
