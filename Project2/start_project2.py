import json
from multiprocessing import Manager
from multiprocessing import Process, Lock
from multiprocessing import Array
import time
import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc
import sys
import Global
from Customer import Customer
from Branch import Branch
import collections
import pprint
import pdb

mutex = Lock()
# from json2xml import json2xml
# from json2xml.utils import readfromjson

def worker(obj,readyQueue,returnDict):
    # Unique Process id
    id = obj['id']
    # Set the type (Branch, Customer) for the Process
    type = obj['type']
    # get the list of addresses of the branch
    branches = obj['branches']
    # Pointer for Customer
    customer = None
    # Pointer for Branch
    branch = None

    # if the type of the process is a Customer
    if type == 'customer':
        # create customer instance
        customer = Customer(int(id), obj['customer-requests'])
        # set the customer process to ready
        readyQueue[len(branches) + customer.id - 1] = Global.READY
        print("DEBUG: In customer ", id, " readyQueue: ", readyQueue)
        # wait until all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)
        # create a gRPC stub for customer
        customer.createStub()
        # execute all the events from the input
        customer.executeEvents()
        # set the customer process to finish
        time.sleep(1)
        mutex.acquire(1)
        readyQueue[len(branches) + int(id)-1] = Global.FINISH
        mutex.release()

    # if the type of the process is a Branch
    elif type == 'branch':
        # get the replica of the balance of the Branch
        balance = obj['balance']
        # create a gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        # create a branch instance
        branch = Branch(int(id), balance, branches)
        # extend the branch instance with the gRPC server
        example_pb2_grpc.add_RPCServicer_to_server(branch, server)
        # set the server port
        print('Starting server. Listening on port 5005'+str(id))
        server.add_insecure_port('[::]:5005'+str(id))
        # start the server
        server.start()
        # set the status of the branch process to ready
        readyQueue[int(id) - 1] = Global.READY
        print("DEBUG: In Branch ", id, " readyQueue: ", readyQueue)
        # wait until all the other processes are ready
        Global.waitWorker(Global.READY, readyQueue)
        # set the branch process to finish
        time.sleep(1)
        mutex.acquire(1)
        readyQueue[int(id)-1] = Global.FINISH
        mutex.release()

    # wait until all the other processes are finished
    Global.waitWorker(Global.FINISH, readyQueue)
    # print function used for debugging purposes
    # print("DEBUG",id,type, branch.recvMsg if type == 'branch' else customer.recvMsg)
    # print("DEBUG",id, customer.recvMsg if type == 'customer' else branch.balance)
    if type == 'branch':
        time.sleep(1)
        returnDict[id] = branch.recvMsg
    if type == 'customer':
        time.sleep(1)
        returnDict[len(branches)+id] = customer.recvMsg

if __name__ == "__main__":
    # receive a json file as an input
    with open('input/input.json', 'r') as f:
        jsonObj = json.load(f)

    # set up the shared hashmap for output
    manager = Manager()
    returnDict = manager.dict()

    # shared counter that checks the status of the running processes
    readyQueue = Array("i", len(jsonObj))

    # get the process ID of the branches
    branches = list()
    for i in range(0, len(jsonObj)):
        if jsonObj[i]['type'] == 'branch':
            branches.append(jsonObj[i]['id'])

    # iterate the json file
    for i in range(0, len(jsonObj)):
        # create the Branch process
        if jsonObj[i]['type'] == 'branch':
            jsonObj[i]['branches'] = branches
            proc = Process(target=worker, args=(jsonObj[i], readyQueue, returnDict))
        # create the Customer process
        elif jsonObj[i]['type'] == 'customer':
            jsonObj[i]['branches'] = branches
            proc = Process(target=worker, args=(jsonObj[i], readyQueue, returnDict))
        # initiate the process
        proc.start()

    # wait until the all the output from the customers are collected
    rtnArray = list()
    hashmap = collections.defaultdict(list)
    raw = list()
    while True:
        time.sleep(1)
        if len(returnDict.items()) == len(jsonObj):
            for key in returnDict:
                #print(key)
                #print(returnDict[key])
                for events in returnDict[key]:
                    raw.append(events)                    
                    #hashmap[events['id']].append(events)
                # print({'id' : key, 'recv' : returnDict[key]})
            break

    #print(raw,len(raw))
    #raw1 = json.dumps(raw)
    #print(raw1)

    # Dictionary to store output data
    output_data = {}

    # Process input JSON data
    for event in raw:
        if(event["type"]=="branch"):
            branch_id = event["id"]
            customer_request_id = event["customer-request-id"]
            logical_clock = event["logical_clock"]
            interface = event["interface"]
            comment = event["comment"]

            # If branch_id is not in output_data, initialize it with an empty events list
            if branch_id not in output_data:
                output_data[branch_id] = {
                    "id": branch_id,
                    "type": "branch",
                    "events": []
                }

            # Add the current event to the events list of the respective branch_id
            output_data[branch_id]["events"].append({
                "customer-request-id": customer_request_id,
                "logical_clock": logical_clock,
                "interface": interface,
                "comment": comment
            })
    # Convert the output_data dictionary to JSON
    output_json = json.dumps(list(output_data.values()), indent=4)
    # Printing the formatted JSON
    print(output_json)
    with open("output/branch_output.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4)

    # Dictionary to store output data
    output_data = {}
    # Process input JSON data
    for event in raw:
        if event["type"]=="customer":
            branch_id = event["id"]
            customer_request_id = event["customer-request-id"]
            logical_clock = event["logical_clock"]
            interface = event["interface"]
            comment = event["comment"]

            # If branch_id is not in output_data, initialize it with an empty events list
            if branch_id not in output_data:
                output_data[branch_id] = {
                    "id": branch_id,
                    "type": "customer",
                    "events": []
                }

            # Add the current event to the events list of the respective branch_id
            output_data[branch_id]["events"].append({
                "customer-request-id": customer_request_id,
                "logical_clock": logical_clock,
                "interface": interface,
                "comment": comment
            })

    # Convert the output_data dictionary to JSON
    output_json = json.dumps(list(output_data.values()), indent=4)

    # Printing the formatted JSON
    print(output_json)
    with open("output/customer_output.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4)


    # PART-3
    print("PART-3")
    # Dictionary to store output data
    output_data = {}
    # Process input JSON data
    for event in raw:
        customer_request_id = event["customer-request-id"]

        # If customer_request_id is not in output_data, initialize it with an empty list
        if customer_request_id not in output_data:
            output_data[customer_request_id] = []

        # Add the current event to the list of the respective customer_request_id
        output_data[customer_request_id].append({
            "id": event["id"],
            "type": event["type"],
            "logical_clock": event["logical_clock"],
            "interface": event["interface"],
            "comment": event["comment"]
        })

    # Sort events within each customer_request_id group by logical_clock in ascending order
    for customer_request_id, events in output_data.items():
        output_data[customer_request_id] = sorted(events, key=lambda x: x["logical_clock"])

    # Convert the output_data dictionary to JSON
    output_json = json.dumps(list(output_data.values()), indent=4)
    #output_json = json.dumps(output_data, separators=(",", ":"))

    # Printing the formatted JSON
    print(output_json)

    output_json = json.dumps(output_data)
    with open("output/events_output.json", "w") as outfile:
        json.dump(output_data, outfile, indent=4)

    #branch_output = dict()
    #for event in raw:
    #    if(event["type"]=="branch"):
    #        branch_output["id"]=event["id"]
    #        branch_output["type"]=event["type"]
    #        event_out = {}
    #        event_out["customer-request-id"]=event["customer-request-id"]
    #        event_out["logical_clock"]=event["logical_clock"]
    #        branch_output["events"] = event_out

    #pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(branch_output)


    for id,events in hashmap.items():
        print("Branch {0} events".format(id))
        print(events, len(events))
        print("--")
    # iterate the events according to id
    for id,events in hashmap.items():
        # sort the events with names and clock
        clock = dict()
        for event in events:
            clock[event['name']] = event['logical_clock']
        temp = [(key,val) for key,val in clock.items()]
        print(temp)
        rtnArray.append(('eventId:{}'.format(str(id)),sorted(temp, key=lambda x: x[1])))


    # write the output file
    #filename = sys.argv[1].split('.')[0]
    filename="result"
    with open(f"output/{filename}_output.json", "w") as outfile:
        json.dump(rtnArray,outfile)
