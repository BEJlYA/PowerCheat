from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    token_bot: str
    admin_id: int
    api_proxy: str


@dataclass
class Setting:
    bots: Bots


def get_setting(path: str):
    env = Env()
    env.read_env(path)

    return Setting(
        bots=Bots(
            token_bot=env.str('TOKEN_BOT'),
            admin_id=env.int('ADMIN_ID'),
            api_proxy=env.str('API_PROXY')
        )
    )


setting = get_setting('data/tokens.env')
