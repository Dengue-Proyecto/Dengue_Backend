from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `evaluaciones` ADD `precision_prediccion` DECIMAL(3,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `evaluaciones` DROP COLUMN `precision_prediccion`;"""


MODELS_STATE = (
    "eJztmlFv2joUgP8K4qmTWLWy0k57SynV2FqYgN47raoik5hgNbEzx1mHJv77bCchieNkZI"
    "M7cscbHPvYPp/tc+zjfG97xIZucHofhIAi0n7b+t7GwIP8h1rUabWB76cFQsDA3JV1w6iS"
    "FIJ5wCiwGJcvgBtALrJhYFHkM0Qwl+LQdYWQWLwiwk4qCjH6EkKTEQeyJaS84OGRixG24T"
    "cYJH/9J3OBoGvnRots0beUm2zlS9kQsxtZUfQ2Ny3ihh5OK/srtiR4UxthJqQOxJACBkXz"
    "jIZi+GJ0saWJRdFI0yrREDM6NlyA0GUZc7dkYBEs+PHRBNJAR/Tysnt2fnn+5vXF+RteRY"
    "5kI7lcR+altkeKksBo1l7LcsBAVENiTLnh0IOUCDbQQYCFFBQ59peA6kHqtRWw3BwVbILx"
    "j5L1wDfThdhhS/73ooLiP8ak/86YnFy8EHYQvrijVT+KC7qiRGDOYCXenMKgFstUZTcAE0"
    "FKMN2P+0B49urVFhB5rVKMsiwPEvjQdZFNTJ9bTjGpQ1Sn20y0vW3I9srB9sq5er/B1Tty"
    "VblahFJYi2aq0US/uZdNz3vkHQYQ1wpGea1mLshur7cFTl6rFKcsW6/FQWnxlAn5QjAH1t"
    "MzoLaZK0m5w6/ADYHFLdCFrqtY++bDBLpA2lnkHJ8aB5uWDpP6Olk8iTTeJ5Ib6ZIycMUi"
    "r+upEoCBI0ct+hY9FaFoDtp5ZOVnbXWSjuftJp23LWIjh5gwN9nbeziNchOjRhXDxMldlr"
    "q4SzVeUAQDp1bQTTWaGSfOtou6FUFXZehTMgdzxM91QLO1b1wCSja3qqgAXQjNw0RagfB6"
    "fH91O2h9nAz6w+lwPBIGeKvgi5sWChEXICbNnAyMW3VVwoCPEtj1FmZW6ZfWZrxx/1dLE1"
    "oo4IMy+S8bWXq3ec0recAtW6T6JhTCdtTGadzWQdKuWrV8td4ZtyevO90X+eWZcD8vwGUI"
    "ej4xEUYWiixWsHLbGfKgnmtRWyUaq58mPxrnCmbDu8F0Ztx9lD4gSHyAMRuIkm7eM8TSQq"
    "po00jr3+HsXUv8bX0ej6QT8UnAHCp7TOvNPrfFmEDIiInJswnsrNmJOBHpZnSB8C/P50b3"
    "OJt/ejYX0FpqrsHV07hRaub88SgI7DF2V7GDbch8xrGgcjrjlxKz1v0pr/Tze9SBzOIOrl"
    "KFNEaBpOasSihEDv4AV5LmkA8KYAuWJysyT1yHR7EsU8HFFDxvbubKGuFGctNgFPz7xrRv"
    "XA/a63o5IDPgvREP7CwVNI3aaxbnvWaEEiKadFAGVnkuKDtDxzzQoTmvTtW7q3ztq/8+2N"
    "SMz25eWn4zq330aP9hjrvCt2kBbpPxNvfn8B7a+bRq3FP78egJ9+sJM7NbC2FB7286F2ev"
    "FPFKrUcvr/Q3oau4UlS9ytS+VTT1CbSjXCwK+0x/t9CsyB1AbGSAVQnm91rdq9k+o7UBKb"
    "KWuhAdl1TGZZDWOd49DszLVUXcr5AGNV+eMyrNfDDd2Yc1+Y/o/DoQ4+rNBLi3D71gtAfz"
    "EN9Px6Pyr7xiFQXkPeYGPtjIYp2WiwL2eJhYKygKq3N57ATeyZ3xSeXavx1fqQlq0cBVvX"
    "vy7sPL+gdIsZ97"
)
