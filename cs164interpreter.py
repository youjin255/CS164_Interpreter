def eval_expression(ast, env):
    ast_type = ast[0]
    if (ast_type == 'number') or (ast_type == 'string'):
        return ast[1]
    elif ast_type == 'null':
        return 0
    elif ast_type == 'id':
        return lookup_env(ast[1], env)
    elif ast_type == 'minus':
        return -(eval_expression(ast[1], env))
    elif ast_type == 'binop':
        operator = ast[1]
        first_ele = ast[2]
        second_ele = ast[3]
        if operator == '+':
            return eval_expression(first_ele, env) + eval_expression(second_ele, env)
        elif operator == '-':
            return eval_expression(first_ele, env) - eval_expression(second_ele, env)
        elif operator == '*':
            return eval_expression(first_ele, env) * eval_expression(second_ele, env)
        elif operator == '/':
            return eval_expression(first_ele, env) / eval_expression(second_ele, env)
        elif operator == '>=':
            if eval_expression(first_ele, env) >= eval_expression(second_ele, env):
                return 1
            else:
                return 0
        elif operator == '<=':
            if eval_expression(first_ele, env) <= eval_expression(second_ele, env):
                return 1
            else:
                return 0
        elif operator == '>':
            if eval_expression(first_ele, env) > eval_expression(second_ele, env):
                return 1
            else:
                return 0
        elif operator == '<':
            if eval_expression(first_ele, env) < eval_expression(second_ele, env):
                return 1
            else:
                return 0
        elif operator == '==':
            if eval_expression(first_ele, env) == eval_expression(second_ele, env):
                return 1
            else:
                return 0
        elif operator == '!=':
            if eval_expression(first_ele, env) != eval_expression(second_ele, env):
                return 1
            else:
                return 0
    elif ast_type == 'lambda':
        return ast[1], ast[2], env
    elif ast_type == 'call':
        fname = ast[1]
        fparams = ast[2]
        closure = lookup_env(fname, env)
        if closure is None and fname == 'lambda-call':
            closure = [], ast[3], ast[4]    # for calling lambda
        new_env = (closure[2], {})
        fargvs = closure[0]
        fbody = closure[1]
        if len(fparams) != len(fargvs):
            print("ERROR: wrong number of args")
        for i in range(len(fargvs)):
            param_value = eval_expression(fparams[i], env)
            new_env[1][fargvs[i]] = param_value
        return eval_block(fbody, new_env)
    elif ast_type == 'ite':
        condition = ast[1]
        first_choice = ast[2]
        second_choice = ast[3]
        if eval_expression(condition, env) != 0:
            return eval_expression(first_choice, env)
        else:
            return eval_expression(second_choice, env)


def eval_stmt(ast, env):
    ast_type = ast[0]
    if ast_type == 'expr':
        return eval_expression(ast[1], env)
    elif ast_type == 'assign':
        new_value = eval_expression(ast[2], env)
        update_env(env, ast[1], new_value)
    elif ast_type == 'var-dec':
        # if lookup_env(ast[1], env):    fix the scope of local variable.
        if ast[1] in env[1]:
            print("The variable", ast[1], "has declared")
        env[1][ast[1]] = eval_expression(ast[2], env)
    elif ast_type == 'fun':
        fname = ast[1]
        fargvs = ast[2]
        fbody = ast[3]
        env[1][fname] = eval_expression(('lambda', fargvs, fbody), env)
    elif ast_type == 'print':
        print(eval_expression(ast[1], env))
    elif ast_type == 'if-else':
        condition = ast[1]
        first_choice = ast[2]
        second_choice = ast[3]
        lambda_call = ('call', 'lambda-call',) + eval_expression(('ite', condition, ('lambda', [], first_choice),
                                                                 ('lambda', [], second_choice)), env)
        return eval_expression(lambda_call, env)
    # elif ast_type == 'while':



def eval_block(ast, env):
    last_stmt = None
    for stmt in ast:
        if stmt[0] == 'stmt':
            last_stmt = eval_stmt(stmt[1], env)
    return last_stmt


def lookup_env(name, env):
    if env[0] is None and name not in env[1]:
        return None
    else:
        if name in env[1]:
            return env[1][name]
        else:
            return lookup_env(name, env[0])


def update_env(env, name, value):
    if env[0] is None and name not in env[1]:
        print("The variable", name, "is not defined")
    elif name in env[1]:
        env[1][name] = value
    elif not (env[0] is None):
        update_env(env[0], name, value)





