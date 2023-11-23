from dotenv import load_dotenv # pip install python-dotenv
from ZWrapper import ZWrapper, gDatabase, CollectionCache, ItemCache, LastVersion, CollectionItemRel
import requests


# disable ssl warning
requests.packages.urllib3.disable_warnings()

# override the methods which you use
requests.post = lambda url, **kwargs: requests.request(
    method="POST", url=url, verify=False, **kwargs
)

requests.get = lambda url, **kwargs: requests.request(
    method="GET", url=url, verify=False, **kwargs
)
load_dotenv()


def check_db():
    gDatabase.connect()
    tables = gDatabase.get_tables()
    if tables:
        return
        print(tables)
    else:
        gDatabase.create_tables([CollectionCache, ItemCache, CollectionItemRel, LastVersion,])


if __name__ == '__main__':

    check_db()

    z = ZWrapper()
    #z.build_database('Q9KRVRM3')
    z.build_database()
