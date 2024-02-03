code = """
def add(x, y):
    return x - y
"""

class testCase:
    def __init__(self, funName, tests, code):
        self.funcName = funName
        self.tests = tests # list of tuples. first is list of args, second is desired output
        self.code = code
    def getArgs(self, index):
        cur = str(self.tests[index][0][0])
        for i in range(1, len(self.tests[index][0])):
            cur += f", {self.tests[index][0][i]}"
        return cur
    def generateCode(self):
        cur = """
ret = ""
try:
"""
        for i in range(len(self.tests)):
            cur += f"""
    if {self.funcName}({self.getArgs(i)}) == {self.tests[i][1]}:
        ret += "hooray\\n"
    else:
        ret += "you failed\\n"
        ret += "{self.funcName}({self.getArgs(i)}) = {self.tests[i][1]}\\n"
        """
        cur += """
except Exception as e:
    ret = e
        """
        return self.code + cur
        
    def returnMessage(self):
        loc = {}
        try:
            exec(self.generateCode(), globals(), loc)
        except Exception as e:
            loc["ret"] = str(e)
        retValue = loc["ret"]
        return retValue