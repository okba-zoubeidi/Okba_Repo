from StafSocket import StafSocket
import socket
import json

class StafRawSocket(StafSocket):
    # Raw Socket listening server
    # Synchronous blocking operation
    def __init__(self, port, logger):
        super(StafRawSocket, self).__init__(port, logger)      
        self.logger.debug("Base class constructor completed")       
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.listen()
        

    def listen(self):
        self.logger.debug("Called Listen method ")
        self.socket.listen(1)
        while True:
            print("Starting to listen")           
            self.c, addr = self.socket.accept()         
            size = 4096                       
            request = self.c.recv(size).decode()           
            print("request is ...", request)
            self.logger.info("request is ..."+ request) 
            try:          
                request_string = json.loads(request)      
                self.logger.info("request string is "+str(request_string))
                if(not hasattr(request_string, "request_id")):
                   request_string['request_id'] = self.new_request_id()
                print (str(request_string))
                result = self.handle_request(request_string)
                print("Sending response "+result)
                self.c.send(bytes(result, 'UTF-8'))
                
            except ValueError as valErr:
                request={
                         "request_id":"None",
                         "response_type":"RSP",
                         "request_status":StafSocket.FAILED,                
                         "error_message":"ValueError:Expecting Value"
                         }
                print("Decoding JSON has failed", str(valErr))
                request_json=bytes(json.dumps(request),'UTF-8')
                self.c.send(request_json)             
                print("Response from the server"+str(request_json))
                self.logger.info("Response from the server"+str(request_json))
                
                pass
            except TypeError as typeErr:
                error_message=str(typeErr)
                result={
                        "request_id ": request_string['request_id'],
                        "response_type":"RSP",
                         "request_status":StafSocket.FAILED,                
                         "error_message":error_message
                        }
                self.c.send(bytes(json.dumps(result),'UTF-8'))
                print("Error in request is"+str(result))
                self.logger.info("Error in request is"+str(result))
                
                pass
             
            
    def new_request_id(self):
        self.logger.debug("Called new_request_id method")
        self.last_request_id += 1
        print(self.last_request_id)
        self.logger.debug("Exiting method with return value "+str(self.last_request_id))
        return self.last_request_id

