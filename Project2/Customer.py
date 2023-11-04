import grpc
#import example_pb2
from example_pb2 import BranchRequest
import example_pb2_grpc
import time

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id

        # events from the input
        self.events = events

        # a list of received messages used for debugging purpose
        self.recvMsg = list()

        # pointer for the stub
        self.stub = None

        # local clock
        self.clock = 0
        self.type = "customer"

    def createStub(self):
        # set the address to the branch (processID of the Customer + 1)
        channel = grpc.insecure_channel('localhost:5005' + str(self.id))

        # create the stub for the Customer
        stub = example_pb2_grpc.RPCStub(channel)

        # set the stub to the pointer
        self.stub = stub
    
    # TODO: Student's implementation
    def eventSend(self,request):
        self.clock += 1
        request.clock = self.clock
        stmt = {"id": self.id, "type":"customer","customer-request-id": request.id, "logical_clock": self.clock, "interface": request.interface, "comment":"event_sent from customer {}".format(self.id)}
        print(stmt)
        return stmt

    # TODO: Student's implementation
    def eventRecv(self,response):
        #print("DEBUG:: local : ",self.clock," remote : ",response.clock)
        self.clock = max(self.clock, response.clock) + 1
        response.clock = self.clock
        #stmt = {"id": self.id, "type":"customer","customer-request-id": response.id, "logical_clock": self.clock, "interface": response.interface,"comment":"event_recv"}
        #print(stmt)
        #return stmt

    # # TODO: Student's implementation
    # def eventExecute(self,request):
    #     self.clock += 1
    #     #stmt = {"id": self.id, "customer-request-id": request.id, "logical_clock": self.clock, "interface": request.interface, "comment":"request_recv"}
    #     #print(stmt)


    def executeEvents(self):
        # Execute all events to customer's branch, and write results.
        # To execute events in the order of the event ID, we need to sort.
        events = sorted(self.events, key=lambda x: x["customer-request-id"])
        # Create client stub for branch if does not exist
        #if self.stub is None:
        #    self.createStub()
        # Execute each event.
        for event in events:
            # Create request object:
            request = BranchRequest(interface=event["interface"], id=event["customer-request-id"], branch_id=self.id, type=self.type)
            stmt = self.eventSend(request)
            self.recvMsg.append(stmt)
            request.clock = self.clock
            if event["interface"] != "query":
                request.money = event["money"]
            # Make request to customer's branch.
            response = self.stub.MsgDelivery(request)
            #print(response)
            # Store the result in recvMsg.
            result = {}
            result["interface"] = response.interface
            result["type"] = "customer"
            result["customer-request-id"] = response.id
            result["logical_clock"] = response.clock
            if response.interface != "query":
                result["result"] = response.result
            else:
                result["balance"] = response.balance
            #self.recvMsg.append(result)
            # NEHA comment to satisfy new document requirement
            #self.eventRecv(response)

