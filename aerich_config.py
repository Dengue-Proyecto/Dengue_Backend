from config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "db.usuario",
                "db.evaluacion",
                "db.sintoma",
                "db.evaluacion_sintoma",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}
