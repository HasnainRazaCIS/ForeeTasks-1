## Task 4
## Description
	- Create a decorator named as 'inverse' and place it over /calc
	  endpoint.
	- This decorator will inverse the op field of request
          i.e convert '+' to '-' and vice versa.
	- No change in actual function of /calc endpoint

#### API will works as follows

'''
POST /calc

request:
	{
		"op1":2,
		"op2":5,
		"op":'+'
	}

response:
	{
		"result": -3
	}
'''
