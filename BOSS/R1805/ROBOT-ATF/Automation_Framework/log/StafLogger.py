import logging
class StafLogger():
    
    def __init__(self,log_path):
        self.log_path = log_path
        self.create_logger()
        self.set_handler()
        self.set_formatter()
    # Create Logger
    def create_logger(self):
        self.logger = logging.getLogger("StafServerLogger")
        self.logger.setLevel(logging.DEBUG)

    # Create Formatter
    def set_formatter(self):
        self.formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")

    # Create Handler
    def set_handler(self):
        self.filehandler = logging.FileHandler(self.log_path+"StafServer.log","w")
        self.set_formatter();
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)






















