from pydantic import BaseModel, field_validator

from nonebot import get_plugin_config


class Config(BaseModel):
    db_host: str = None
    db_port: int = None
    db_user: str = None
    db_password: str = None
    superusers: list[int] = []
    broadcast_time: list[int] = []
    broadcast_groups: list[int] = []

    @field_validator('boardcast_time')
    @classmethod
    def check_superusers(self, value: list[int]):
        if len(value) != 2:
            raise ValueError('broadcast_time must be a list of two integers')
        hour, minute = value
        if not 0 <= hour <= 23:
            raise ValueError('the frist item of list must be between 0 and 23 because it is hour')
        if not 0 <= minute <= 59:
            raise ValueError('the second item of list must be between 0 and 59 because it is minute')
        return value

    @field_validator('boardcast_groups')
    @classmethod
    def check_broadcast_groups(self, value: list[int]):
        if not value:
            raise ValueError('broadcast_groups cannot be empty')
        for group in value:
            if not 10000000 <= group <= 99999999:
                raise ValueError('broadcast_groups must be a list of QQ group number')
        return value


config: Config = get_plugin_config(Config)
