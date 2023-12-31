# distributed-and-multiprocessor-systems
Projects related to distributed systems

# CSE 531 gRPC Project

This repository contains code for the gRPC project in CSE 531. 

## Overview

The goal of this project is to build a distributed banking system that allows multiple customers to withdraw or deposit money from multiple branches. gRPC is used for communication between the customer and branch processes.
![visualization](https://github.com/dhanrajbhosale/distributed-and-multiprocessor-systems/blob/2806a936aea7f5a60525014c80f0b318eb54faa6/Project1/architecture.png?raw=true)

## Usage

1. Clone the repository

```
git clone https://github.com/dhanrajbhosale/distributed-and-multiprocessor-systems.git
```

2. Install requirements

```
pip install -r requirements.txt 
```

3. Run the branches

```
python start_branches.py
```

4. In a separate terminal, run the customers

```
python execute_customer_events.py
```

Results will be written to `output.json`

## Implementation

- `Customer.py` - Implements customer logic and communication with branch
- `Branch.py` - Implements branch server and logic
- `bank.proto` - Defines gRPC service 
- Other Python scripts handle running the processes
