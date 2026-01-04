import os
from configs.dev_config import DevConfig
from configs.prod_config import ProdConfig

ENV = os.environ.get("ENV", "dev")
if ENV == "master":
    print("Using Prod Config")
    Config = ProdConfig
else:
    print("Using Dev Config")
    Config = DevConfig