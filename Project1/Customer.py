import bank_pb2_grpc
from bank_pb2 import BranchRequest
import json
import grpc

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

    def createStub(self):
        self.stub = bank_pb2_grpc.BranchStub(grpc.insecure_channel("localhost:" + str(30000 + self.id)))

    def executeEvents(self):
        # Execute all events to customer's branch, and write results.
        # To execute events in the order of the event ID, we need to sort.
        events = sorted(self.events, key=lambda x: x["id"])
        # Create client stub for branch if does not exist
        if self.stub is None:
            self.createStub()
        # Execute each event.
        for event in events:
            # Create request object:
            request = BranchRequest(interface=event["interface"], id=event["id"])
            if event["interface"] != "query":
                request.money = event["money"]
            # Make request to customer's branch.
            response = self.stub.MsgDelivery(request)
            # Store the result in recvMsg.
            result = {}
            result["interface"] = response.interface
            if response.interface != "query":
                result["result"] = response.result
            else:
                result["balance"] = response.balance
            self.recvMsg.append(result)

        # Print this customer's result:
        result = {"id": self.id, "recv": self.recvMsg}
        print(result)
        # Write this customer's result to output.json
        with open("output.json", 'a') as file:
            file.write(json.dumps(result) + "\n")
