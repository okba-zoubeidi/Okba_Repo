import json
import sys
import selenium
class StafSocket:
    # Abstract socket class that just implements the request handling method common to all sockets
    # Contains core STAF server request handling logic and method templates for other methods
    # Constants have been declared here for now.
    # They should be defined in some better module and exported cleanly
    RSP = "RSP"
    ACK = "ACK"
    SUCCESS = 1
    FAILED = 0
    def __init__(self, port, logger):
        self.logger = logger
        self.logger.debug("Base class constructor started")
        self.port = port
        self.last_request_id = 0
        self.last_component_id = 0
        self.host=''
        self.components = {}
        return self

    def listen(self):
        self.logger.info("listen method called")
        self.logger.info("Exiting listen method with return value True")
        return True
        
    def handle_request(self, request):
        try:
            self.logger.debug("Handle_request method called with request argument")           
            requestHandler = "handle_" + request['request_type']
            print("Handler is " + requestHandler)
            self.logger.info("Handler is"+requestHandler)
            response = getattr(self, requestHandler)(request)
            print("Returning response "+response)     
            return response
        except KeyError as keyErr:
            response={"request_id":"None",
                      "response_type":"RSP",
                      "request_status":StafSocket.FAILED,
                      "error_message":"Key Error"
                      }
            print("Error in request type"+str(response))
            self.c.send(bytes(json.dumps(response),'UTF-8'))
            pass
            self.logger.info("Request type"+request['request_type']+"" )
            pass
        except AttributeError as attError:
            attError=str(sys.exc_info())
            response={"request_id":"None",
                      "response_type":"RSP",
                      "request_status":StafSocket.FAILED,
                      "error_message":"Attribute Error"
                      }
            print("Error in request type"+str(response))
            self.logger.info("Error in request type"+str(response))
            self.c.send(bytes(json.dumps(response),'UTF-8'))
            pass
            
        if request['request_type'] is None:
            print("Please enter the request_type")
        else:
          print("Request Type is "+str(request['request_type']))
            
        

    def handle_action(self, request):
        self.logger.debug("Handle Action method called with request argument")
        returnObject = {}
        if(request["command"] == "create_component"):
            try:
                self.logger.debug("About to create component")
                component = self.create_component(request["params"])
                print("Component created with component id "+str(component.componentId))
                returnObject = {"request_id :": request["request_id"],
                "response_type" : StafSocket.RSP,
                "component_id" : component.componentId,
                "status" : StafSocket.SUCCESS,
                "error_message" : ""
                }
            except (TypeError,ValueError) as error:
                print("Component creation failed with error " + error)
                returnObject={
                                   "request_id :": request["request_id"],
                                   "response_type" : StafSocket.ACK,
                                   "component_id" : component.componentId,
                                   "status" : StafSocket.FAILED,
                                   "error_message" : error
                                   }
        else:
            try:
                
                
                component_id = request["params"]["component_id"]
                #print("Component id is"+component_id+" is of type "+type(component_id))
                component_object = self.components[int(component_id)]
                action_requested = request["command"]
                print ("Retrieved component object "+str(component_object)+ "to do action "+action_requested)
                self.logger.info("Retrieved component object "+str(component_object)+ "to do action "+action_requested)               
                self.logger.info("Sending hard coded action response")
                returnObject["response_type"] = self.RSP
                #returnObject["component_id"] = component_id
                status=getattr(component_object,action_requested)(request["params"])
                #returnObject["status"] = getattr(component_object,action_requested)(request["params"])
                returnObject["error_message"] = ""
                if status is False:
                    returnObject["status"]=StafSocket.FAILED
                else:
                    returnObject["status"]=StafSocket.SUCCESS
                    returnObject["value"]=status
                      
                
                
                
            except (ValueError,AttributeError) as error:
                self.logger.error("component id "+component_id+"Not available")
                returnObject={
                                   "request_id :": request["request_id"],
                                   "response_type" : StafSocket.ACK,
                                   "component_id" : component_id,
                                   "status" : StafSocket.FAILED,
                                   "error_message" : ""
                              }
                pass
        returnMessage = json.dumps(returnObject)
        self.logger.debug("Handle_action method is exiting with return value "+returnMessage)
        return returnMessage
        
    def handle_test(self, request):
        print("Called Handle_test method with request argument")
        self.returnObject = {
                      "request_id":self.request.request_id,
                      "response_type":"RSP",
                      "return":"FAILED",
                      "error_message":"ERROR:Test requests are not yet handled"
                      }   
    def create_component(self, params):
        try:
            self.logger.debug("Called create_component method with params argument")
            component_type = params["component_type"]
            module = __import__(component_type)
            componentClass = getattr(module, component_type)
            component = componentClass(params)
            component.componentId = self.new_component_id()
            print("Component is "+str(component)+"having componentID as "+str(component.componentId))
            self.logger.info("Component is "+str(component)+"having componentID as "+str(component.componentId))
            self.components[component.componentId] = component      
            return component
        except ValueError:
            self.logger.error("Component type"+component_type+"does not exist")
        
    def new_component_id(self):
        # Some logic to create random unique component ID
        self.logger.debug("Called new_component_id method")
        self.last_component_id += 1
        self.logger.debug("Exiting the new_component_id method with return value of "+str(self.last_component_id))
        return  self.last_component_id
        
    def logger(self, message, level):
        # Wrapper logging method
        self.logger.logger(message, level)

    def disconnect(self):
        print("Called disconnect method")
        print("Exiting disconnect method with return value True")
        return True
        










