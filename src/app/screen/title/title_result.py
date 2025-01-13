import dataclasses

@dataclasses.dataclass
class TitleScreenResult:
    user_name:str = None
    is_start:bool = False
    is_exit:bool = False