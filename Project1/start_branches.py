import json
from Branch import Branch
import multiprocessing

def main():
    input = json.load(open("input.json"))
    branches = list()
    ids = list()
    for entry in input:
        if entry["type"] == "branch":
            branch = Branch(entry["id"], entry["balance"], ids)
            branches.append(branch)
            # ids are passed by reference to Branch, so all branches will have
            # all the ids by the time we actually start the branches.
            ids.append(entry["id"])
    # Start branches in their own process.
    for branch in branches:
        process = multiprocessing.Process(target=branch.start)
        process.start()

if __name__ == "__main__":
    main()