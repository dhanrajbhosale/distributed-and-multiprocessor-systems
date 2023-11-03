# distributed-and-multiprocessor-systems
Projects related to distributed systems

# CSE 531 Logical Clock Project

This repository contains code for the logical clock project in CSE 531. 

## Overview

The goal of this project is to implement Lamport's logical clock algorithm for ordering events in a distributed banking system. 

Customers and branches are implemented as separate processes. Each process maintains its own logical clock. Events are ordered using the happens-before relationship.

## Usage

1. Clone the repository

```
git clone https://github.com/dhanrajbhosale/distributed-and-multiprocessor-systems.git
```

2. Install requirements

```
pip install -r requirements.txt
```

3. Run the processes

```
python start_project2.py
```

4. The output will be written to multiple JSON files in `/output`

## Implementation 

- `Customer.py` - Implements customer process and logical clock
- `Branch.py` - Implements branch server process and logical clock
- `start_project2.py` - Starts processes and handles output
- `Global.py` - Shared utilities
- Protocol buffers handle RPC communication