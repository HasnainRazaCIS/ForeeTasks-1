# Comment (Syed Rafay): Try returning appropriate response instead of 'abort(400)' so that the developer could know the reason for API failure response
# Everything else seems to be fine and modular!!

from flask import Flask,request,jsonify
import functools

app = Flask(__name__)

# Inverse Decorator : 
#    - To reverse the incoming 'op' field in json request
#    - Example: {'op':'+', ... } should do '-' (subtraction) operation and vice versa.  

inverse_dict = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*"
}

# here 'f' is the function which is passed to this decorator
# In this case, since we are applying this decorator to /calc, so it will be calculator_api view 
def inverse(f):
    @functools.wraps(f)
    def inverse_logic(*args, **kwargs):
        # Access request object and modify incoming json request
        data = request.json
        if 'op' in data:
            operation = data['op']
            if operation in inverse_dict:
                request.json['op'] = inverse_dict[operation]
        else:
            abort(400)
        return f(*args, **kwargs)
    return inverse_logic


@app.route("/")
def hello_world():
    return 'Hello Task3 Flask API'

def calculate(op1,op2,op):
    if op == "+":
        return op1+op2
    if op == "-":
        return op1-op2
    if op == "*":
        return op1*op2
    if op == "/":
        return op1/op2
    else:
        return "Invalid Operation"


@app.route("/calc", methods=['POST'])
@inverse
def calculator_api():
    try:
        data = request.json
        print(data)
        op = data["op"]
        op1 = data["op1"]
        op2 = data["op2"]


        ans = calculate(op1,op2,op)
        resp = {"result": ans}
    
    except:
        resp = {"result": "Bad json object"}

    return jsonify(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

