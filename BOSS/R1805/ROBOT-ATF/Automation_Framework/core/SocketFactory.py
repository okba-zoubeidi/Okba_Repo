import socket
class SocketFactory:
    socket = socket.socket()
    # Socket Factory is a class to dynamically create sockets
    def __init__(self, logger):
        # constructor flow
        # import all modules/classes from acceptable/supported list of sockets
        # Create class reference for each socket type so that socket object can be generated automatically
        # if new socket or transport methods are to be added , the class must be written and class name added to socketList attribute
        # Logger object is passed on a dependency and shared
        self.logger=logger
        self.socketList = ['StafRawSocket']       
        self.sockets = {}
        for socket in self.socketList:
            module = __import__(socket)
            print(module)
            self.logger.debug("module is"+str(module))
            self.sockets[socket] = getattr(module, socket)
            print(self.sockets[socket])
            self.logger.debug("Socket Class is "+str(self.sockets[socket]))
    def create_socket(self, socket_type, port, logger):
        self.logger.debug("Called Create_socket method with socket_type ,port and logger arguments ")
        if socket_type in self.socketList:
            print("Socket type is " + socket_type)
            self.logger.info("Socket type is "+socket_type)
            print("Class is " + str(self.sockets[socket_type]))
            self.logger.info("Class is " + str(self.sockets[socket_type]))
            socketInList=self.sockets[socket_type](port, logger)         
            return socketInList
            
        else :
            self.logger.error("Socket "+socket_type+"not yet implemented in STAF")
            return "Error:Socket" + socket_type + "not yet implemented in STAF"
            
