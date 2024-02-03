code = """
def add(x, y):
    return x - y
"""

class testCase:
    def __init__(self, funName, tests, code="", description=""):
        self.funcName = funName
        self.tests = tests # list of tuples. first is list of args, second is desired output
        self.code = code
        self.description = description
    def getArgs(self, index):
        cur = str(self.tests[index][0][0])
        for i in range(1, len(self.tests[index][0])):
            cur += f", {self.tests[index][0][i]}"
        return cur
    def generateCode(self):
        cur = """
ret = ""
try:
    numPassed = 0
"""
        for i in range(len(self.tests)):
            cur += f"""
    if {self.funcName}({self.getArgs(i)}) == {self.tests[i][1]}:
        ret += "test {i + 1} passed<br>"
        numPassed += 1
    else:
        ret += "you failed test {i + 1}<br>"
        ret += "{self.funcName}({self.getArgs(i)}) = {self.tests[i][1]}<br>"
        """
        cur += """
    ret += f"you passed {numPassed}"""
        cur += f"""/{len(self.tests)} test cases<br>"
except Exception as e:
    ret = e
        """
        return self.code + cur
        
    def returnMessage(self):
        loc = {}
        try:
            exec(self.generateCode(), loc, loc)
        except Exception as e:
            loc["ret"] = str(e)
        retValue = loc["ret"]
        return retValue