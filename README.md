## ForeeTasks


### Task6

- All parts completed.
- Code is present in task6/server.py

a. Write all request + result of /calc in mongodb collection named *calculations* as:
	{
	op1: 2,
	op2: 5,
	op: '+',
	result: 7
	}

b. Create a collection in mongodb named *last_operations* which will have at most 4 documents for each op ('+', '-', '*', '/'), and will be updated based on the last request received of the operation on /calc endpoint.

c. Create an end-point [GET] /calculations, which will return all the documents from calculations collection, along with a field total_records



