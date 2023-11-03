import json
from Customer import Customer
import multiprocessing

def main():
    # Delete previous contents of output.json.
    open("output.json", "w").close()
    input = json.load(open("input.json"))
    customers = list()
    for entry in input:
        if entry["type"] == "customer":
            customer = Customer(entry["id"], entry["events"])
            customers.append(customer)
    # Execute all customer evennts in their own processes. While
    # this is not necessary, the project document asks refers to
    # customer processes, hence we create a process, and wait for
    # the process to complete before executing events of the next
    # customer. It is actually not necessary to sleep after a
    # a customer executes its events, since branch propogates
    # synchronously. By the time the customer gets the response,
    # all branches would have already updated.
    for customer in customers:
        process = multiprocessing.Process(target=customer.executeEvents)
        process.start()
        process.join()

if __name__ == "__main__":
    main()