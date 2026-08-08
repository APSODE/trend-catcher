import logging

# 시끄러운 서드파티 로거들
NOISY_LOGGERS = ("httpx", "httpcore", "aiosqlite", "sqlalchemy.engine", "urllib3", "asyncio")


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    for name in NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)