from aiologger.loggers.json import JsonLogger

logger = JsonLogger.with_default_handlers(
        level='DEBUG',
        serializer_kwargs={'ensure_ascii': False},
    )
