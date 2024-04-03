from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    token_bot: str
    token_payment: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            token_bot=env.str('TOKEN_BOT'),
            token_payment=env.str('TOKEN_PAYMENT'),
            admin_id=env.int('ADMIN_ID')
            
        )
    )


settings = get_settings('data/input.txt')
