class DebugSetting:
    __automatic_talk: bool = False
    __automatic_vote: bool = False
    __automatic_divine: bool = False
    __automatic_attack: bool = False

    def __init__(
        self,
        *,
        auto_talk: bool = False,
        auto_vote: bool = False,
        auto_divine: bool = False,
        auto_attack: bool = False,
    ) -> None:
        self.__automatic_talk = auto_talk
        self.__automatic_vote = auto_vote
        self.__automatic_divine = auto_divine
        self.__automatic_attack = auto_attack

    @property
    def automatic_talk(self) -> bool:
        return self.__automatic_talk

    @property
    def automatic_vote(self) -> bool:
        return self.__automatic_vote

    @property
    def automatic_divine(self) -> bool:
        return self.__automatic_divine

    @property
    def automatic_attack(self) -> bool:
        return self.__automatic_attack

    def set_automatic_talk(self) -> None:
        self.__automatic_talk = True

    def set_automatic_vote(self) -> None:
        self.__automatic_vote = True

    def set_automatic_divine(self) -> None:
        self.__automatic_divine = True

    def set_automatic_attack(self) -> None:
        self.__automatic_attack = True
