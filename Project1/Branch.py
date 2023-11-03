from bank_pb2 import BranchRequest, BranchResponse
import bank_pb2_grpc
import grpc
from concurrent.futures import ThreadPoolExecutor

class Branch(bank_pb2_grpc.BranchServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

    def start(self):
        # Before we start the server, we need to create all other branch stubs in order to
        # propogate requests to them.
        for id in self.branches:
            # Do not create stub for own branch.
            if id != self.id:
                self.stubList.append(bank_pb2_grpc.BranchStub(grpc.insecure_channel("localhost:" + str(30000 + id))))
        # start branch server. Port is a constant port + this branch's ID.
        server = grpc.server(ThreadPoolExecutor(max_workers=4))
        server.add_insecure_port("[::]:" + str(30000 + self.id))
        bank_pb2_grpc.add_BranchServicer_to_server(self, server)
        print("Branch server: ", self.id, " has started")
        server.start()
        server.wait_for_termination()

    def InformOtherBranches(self, interface, id, money):
        # Make a new request to other branches informing them of the transaction.
        request = BranchRequest(interface=interface, id=id, money=money)
        for branchStub in self.stubList:
            branchStub.MsgDelivery(request)

    def MsgDelivery(self,request, context):
        # Accept requests from both customers and other branches, return response.
        # If request is from a customer, propogate to other branches.
        # Create response for caller.
        response = BranchResponse(interface=request.interface)
        if request.interface in ("withdraw", "propogate_withdraw"):
            # Ensure that money being withdrawn is possible, else fail.
            if  request.money > self.balance or request.money < 0:
                response.result = "fail"
            else:
                self.balance = self.balance - request.money
                response.balance = self.balance
                response.result = "success"
                if response.interface == "withdraw":
                    self.InformOtherBranches("propogate_withdraw", request.id, request.money)
        elif request.interface in ("deposit", "propogate_deposit"):
            # Ensure that money being deposit is possible, else fail.
            if request.money < 0:
                response.result = "fail"
            else:
                self.balance = self.balance + request.money
                response.balance = self.balance
                response.result = "success"
                if response.interface == "deposit":
                    self.InformOtherBranches("propogate_deposit", request.id, request.money)
        elif request.interface == "query":
            response.balance = self.balance
            response.result = "success"
        else:
            raise Exception("Interface not supported by branch: " + request.interface)
        # Keep track of request and responses received by this branch.
        result = {"interface": request.interface, "result": response.result}
        self.recvMsg.append(result)
        return response