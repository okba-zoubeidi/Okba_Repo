import sys
import os

sys.path.append( '..\core' )
sys.path.append( '..\lib' )
sys.path.append('..\log')

from SocketFactory import SocketFactory
from StafLogger import StafLogger
class StafServer:
    def  __init__(self, port, log_path, socket_type):
        # constructor flow
        # Init logger handle
        # Set default transport if not defined
        # Create socket server using transport
        # checks if Logging directory exists, if not then it will create that 
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        
        self.logger =StafLogger(log_path).logger
        
        if not socket_type:
            socket_type = "StafRawSocket"
        if not port:
            port = 9999

        self.logger.info("Starting Staf Server type "+ socket_type +" on port "+str(port))
        socketFactory =SocketFactory(self.logger)
        self.logger.debug("Created socket factory")
        self.server = socketFactory.create_socket(socket_type, port, self.logger)
        self.logger.debug("Staf server created")
        self.server.start()
        self.logger.info("Staf server listening for new requests on port "+port)
        return
    def logger(self, message, level):
        # Wrapper logging method
        self.logger.logger(message, level)
    


stafserverObj = StafServer(9999, "C:\\StafAutomation\\Logs\\", "StafRawSocket")






