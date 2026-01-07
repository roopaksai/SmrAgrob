import os
from configs.dev_config import DevConfig
from configs.prod_config import ProdConfig

ENV = os.environ.get("ENV", "dev")
if ENV == "master":
    print("Using Prod Config")
    CONFIG = ProdConfig
else:
    print("Using Dev Config")
    CONFIG = DevConfig