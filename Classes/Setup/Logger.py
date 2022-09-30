import logging
import logging.config

class Logger:
    def createLogger(self):
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })

        log = logging.getLogger("League of Poro")
        log.setLevel('DEBUG')
        ch = logging.StreamHandler()
        ch.setLevel('DEBUG')
        formatter = logging.Formatter('%(levelname)s: %(asctime)s - %(message)s', '%Y/%m/%d %H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)

        return log
