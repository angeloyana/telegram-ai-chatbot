import logging

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logger = logging.getLogger('chatbot')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

debug_handler = logging.FileHandler('debug.log', mode='a')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

errors_handler = logging.FileHandler('errors.log', mode='a')
errors_handler.setLevel(logging.ERROR)
errors_handler.setFormatter(formatter)

root_logger.addHandler(console_handler)
root_logger.addHandler(debug_handler)
root_logger.addHandler(errors_handler)
