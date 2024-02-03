def execute_code(code):
    try:
        result = exec(code) # Very risky, use with caution
        return str(result)
    except Exception as e:
        return str(e)
