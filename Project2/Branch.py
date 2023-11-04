import grpc
#import example_pb2
from example_pb2 import BranchRequest, BranchResponse
import example_pb2_grpc

class Branch(example_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id

        # replica of the Branch's balance
        self.balance = balance

        # the list of process IDs of the branches
        self.branches = branches

        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        #self.stubListNum = list()

        # a list of received messages used for debugging purpose
        self.recvMsg = list()

        # TODO: Students are expected to update the local clock
        # local clock
        self.clock = 0

        # iterate the processID of the branches
        for addr in self.branches:

            # if the branchID is not itself
            if addr != self.id :

                # set the address to the branch
                channel = grpc.insecure_channel('localhost:5005' + str(addr))

                # create a stub
                stub = example_pb2_grpc.RPCStub(channel)

                # append the stub to the pointer
                self.stubList.append((stub,addr))
                #self.stubListNum.append(addr)



    def eventSend(self,request, e_to):
        self.clock += 1
        request.clock = self.clock
        stmt = {"id": self.id, "type":"branch","customer-request-id": request.id, "logical_clock": self.clock, "interface": request.interface, "comment":"event_sent to branch {}".format(e_to)}
        print(stmt)
        return stmt

    # TODO: Student's implementation
    def eventRecv(self,response, e_from):
        #print("DEBUG:: local : ",self.clock," remote : ",response.clock)
        self.clock = max(self.clock, response.clock) + 1
        response.clock = self.clock
        stmt = {"id": self.id, "type":"branch","customer-request-id": response.id, "logical_clock": self.clock, "interface": response.interface,"comment":"event_recv from {} {}".format(response.type ,e_from)}
        print(stmt)
        return stmt

    # # TODO: Student's implementation
    # def eventExecute(self,request):
    #     self.clock += 1

    def InformOtherBranches(self, interface, id, money):
        # Make a new request to other branches informing them of the transaction.
        request = BranchRequest(interface=interface, id=id, money=money, type="branch", branch_id=self.id)
        #stmt = self.eventSend(request)
        #self.recvMsg.append(stmt)

        for branchStub,addr in self.stubList:
            #print(addr)
            stmt = self.eventSend(request, addr)
            self.recvMsg.append(stmt)
            branchStub.MsgDelivery(request)


    def MsgDelivery(self,request, context):
        stmt = self.eventRecv(request,request.branch_id)
        self.recvMsg.append(stmt)
        response = BranchResponse(interface=request.interface)
        response.id = request.id
        response.clock = stmt["logical_clock"]
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
        return response