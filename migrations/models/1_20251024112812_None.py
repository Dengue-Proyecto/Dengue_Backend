from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `usuarios` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `numero_colegiatura` VARCHAR(6) NOT NULL UNIQUE,
    `nombres` VARCHAR(100) NOT NULL,
    `apellido_paterno` VARCHAR(50) NOT NULL,
    `apellido_materno` VARCHAR(50) NOT NULL,
    `correo` VARCHAR(100) NOT NULL UNIQUE,
    `contrasena` VARCHAR(255) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `evaluaciones` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `codigo_evaluacion` VARCHAR(7) NOT NULL UNIQUE,
    `riesgo` VARCHAR(10) NOT NULL,
    `probabilidad` DOUBLE NOT NULL,
    `resultado` VARCHAR(10),
    `tiempo_inicial` DATETIME(6) NOT NULL,
    `tiempo_final` DATETIME(6) NOT NULL,
    `fecha` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `usuario_id` INT NOT NULL,
    CONSTRAINT `fk_evaluaci_usuarios_ea6a15d2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `sintomas` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `nombre` VARCHAR(50) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `evaluacion_sintomas` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `evaluacion_id` INT NOT NULL,
    `sintoma_id` INT NOT NULL,
    UNIQUE KEY `uid_evaluacion__evaluac_cab49a` (`evaluacion_id`, `sintoma_id`),
    CONSTRAINT `fk_evaluaci_evaluaci_5a54558b` FOREIGN KEY (`evaluacion_id`) REFERENCES `evaluaciones` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_evaluaci_sintomas_da6fb7bc` FOREIGN KEY (`sintoma_id`) REFERENCES `sintomas` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztml9v2zYQwL+K4acOyIrGi5Nib4rjoF4Tu7CdbWgQCLR0lolQpEpRTY3C330kJVn/Na"
    "u1V2v1m3TkibwfjzzyqK9dl9lA/NcPfoA4Zt3fO1+7FLkgH/JFZ50u8rykQAkEWhBdNwgr"
    "aSFa+IIjS0j5EhEfpMgG3+LYE5hRKaUBIUrILFkRUycRBRR/CsAUzAGxAi4LHp+kGFMbvo"
    "Afv3rP5hIDsTO9xbZqW8tNsfa0bETFra6oWluYFiOBS5PK3lqsGN3WxlQoqQMUOBKgPi94"
    "oLqvehdZGlsU9jSpEnYxpWPDEgVEpMzdkYHFqOIne+NrAx3Vyq+984uri7e/XV68lVV0T7"
    "aSq01oXmJ7qKgJjOfdjS5HAoU1NMaEGw1c4EyxAQcjEXBU5DhYIV4Oslw7B1aakwcbY/yh"
    "ZF30xSRAHbGSr5c1FP80poN3xvTV5S/KDiadO/T6cVTQUyUKcworcxcc/EYsE5X9AIwFCc"
    "FkPh4C4fmbNztAlLUqMeqyLEjkASHYZqYnLeeUNSFapttOtP1dyParwfarubrfwdU9cc1z"
    "tRjn0IhmotHGdfMgk162KBv0gTYKRlmtdjpkr9/fAaesVYlTl202aqO0fE6FfCVYIOv5BX"
    "HbzJQk3OEzIgGypAVloes60r59PwWCtJ1FztGucbj90nFS38TOE0ujeaK5sR6rAlcscntu"
    "XoIocnSvVduqpSKUko12Fln1Xjs/SKf9dpv22xazscNMyAz27itciXIbo0Ydw3iRu6pc4q"
    "7y8YJj8J1GQTfRaGecON8t6tYE3TxDj7MFWmC5r0MlU/uWMFQxufOKOaBLpXmcSGsQ3kwe"
    "ru+GnQ/T4WA0G03GygB37X8iSaESSQEW2szp0LjLeyX4spfIbuaYaaVv8s1o4v6PXFNgcD"
    "1mYootjEiR5o2EIbAL5USL2jmsdqT+On5onbfOR/fD2dy4/6Dd1I/d1JgPVUkv67yRtJDN"
    "2H6k89do/q6jXjsfJ2Pt5x7zhcN1i0m9+ceu6hMKBDMpezGRnTY7FseishFdYvrN47nVPY"
    "3mjx7NJVirkpNa/TBuldo5fnKhRvaEknW04rZkPKPgUDucUTLfbLTFzyr9+1b/SEZxD7v9"
    "wkm7QLJkO8U4YIe+h7WmOZKdQtSC6vN06hbm+ChWHaalmKOX7eEx5yPSSGkahNungTEbGD"
    "fD7qZZmsL0ZWvMRXvLVszC77WL80GTFjGRkoxFClZ1uiI9QqdUxbEtXmd1V4P6Qqr5FVZb"
    "kxL7uQz4zsTraUX7D9OwNWtbKcBdkrLm4Ra8x2428xe11H06rYSHXQlTo9sIYUHvZ9oXp4"
    "8Ukac2o5dV+pnQ1Rwp6i4OGp8q2npLd5Y7WBTmWfnZosQj9wCxlQE2TzA715oezQ4ZrQ3g"
    "2FqVheiopDYuo6TO6exxZKtcXcT9DNxveDmaUmnnnd7e/v3I/uflNYEYVW8nwIP9iwThHM"
    "xC/GM2GVf/iBSp5EA+UGngo40tcdYh2BdPx4m1hqKyOpPHjuG9ujf+znMd3E2u8wlq9YHr"
    "Zufk/YeXzT83cS0O"
)
