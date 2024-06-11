import os

from dotenv import load_dotenv

load_dotenv()

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": os.getenv('DB_HOST'),
                "port": os.getenv('DB_PORT'),
                "user": os.getenv('DB_USER'),
                "password": os.getenv('DB_PASSWORD'),
                "database": os.getenv('DB_NAME'),
            }
        },
    },
    "apps": {
        "models": {
            "models": ["src.db.models.task", "aerich.models"],
            "default_connection": "default",
        }
    },
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://codeforces.com/apiHelp/methods',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

cookies = {
    '_gid': 'GA1.2.1159149947.1717993772',
    'JSESSIONID': '38EAAE7205DB1D335BA8D9E57F2983FA',
    '39ce7': 'CFkrrMjl',
    'evercookie_etag': 'zbdwspgt5frh0iu2j2',
    'evercookie_cache': 'zbdwspgt5frh0iu2j2',
    'evercookie_png': 'zbdwspgt5frh0iu2j2',
    '70a7c28f3de': 'zbdwspgt5frh0iu2j2',
    'nocturne.language': 'ru',
    'X-User': '',
    'X-User-Sha1': 'f2c73ae9b74dc698c3e08c6ca722b6460a7a213a',
    'lastOnlineTimeUpdaterInvocation': '1718121235498',
    '_gat_gtag_UA_743380_5': '1',
    '_ga_K230KVN22K': 'GS1.1.1718124610.11.1.1718124625.0.0.0',
    '_ga': 'GA1.1.721976061.1717603265',
    'cf_clearance': 'R0zCUA_yFx..d_5YsAo_WQtq65CI56SKAT0JH_BWQmg-1718124625-1.0.1.1-UTBQzerZ74bE2HeuibJCQ6.mq3Yxt_1EwWCt170dD8GkXO1LJ2ke.D0qa4N3MH6gUwzyoE9S0fWOmll2F6ooZw'
}
