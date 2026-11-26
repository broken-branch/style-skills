# Google Python: explicit deletion of unused callback parameters, module
# imports, lazy logging arguments, and documented exceptions [GOOGLE-PYTHON].
"""Provide on_message(message, context) for a text event callback."""

import logging


def on_message(message: str, context: object) -> None:
    """Logs a nonblank message at info level.

    Args:
        message: Text to log unchanged, including any surrounding whitespace.
        context: Callback metadata required by the interface but not used here.

    Raises:
        ValueError: The message contains no non-whitespace characters.
    """
    # The callback signature includes metadata that this handler does not need.
    del context
    if not message.strip():
        raise ValueError('message must not be blank')
    logging.info('Received message: %s', message)
