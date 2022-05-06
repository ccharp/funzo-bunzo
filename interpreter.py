import json
import pyparsing as pp
import numbers
import time

# TODO: consistency with kind of quote used, pref single
class _Env:
    def __init__(self, params, tasks):
        self.params = params 
        self.last_eval = ""
        self.tasks = tasks


def execute(dsl, input_params): # TODO annotate type of params (dictionary)

    # We require entry_point
    # TODO: catch and re-wrap exceptions? If there's time. For now, let the caller do it. 
    return eval_task(_Env(input_params, dsl['tasks']), dsl['entry_point'])


def eval_task(env: _Env, task_name): # TODO: annotate type of tasks (dictionary) and task
    task = env.tasks[task_name]
    output = ""
    if 'steps' in task:
        eval_step(env, task['steps']) 
        output = env.last_eval
    if 'output' in task:
        output = eval_statement(env, task['output'])
    
    return output


def eval_statement(env, statement):
    words = parse_statement(statement)

    pp(words)

    accum_str = ""
    for word in words: 
        accum_str += eval_word(env, word)

    return accum_str


# TODO: use constants for TRUE and FALSE
def eval_step(env, steps):
    # Doesn't output anything, rather we store the each Step's output in env.last_eval
    for step in steps:
        # TODO: assert that each step map only contains a single instruction
        if "length" in step:
            l = len(eval_statement(env, step['length']))
            env.last_eval = l
        elif "gt" in step: # Both operantds must be interpretable as numbers 
            gt = step['gt']
            env.last_eval = "TRUE" if as_number(env, gt[0]) > as_number(env, gt[1]) else "FALSE"
        elif "if" in step:
            ifs = step['if']
            cond = eval_word(env, ifs['condition']) 
            if cond == "TRUE":
                env.last_eval = eval_word(env, ifs['true'])
            elif cond == "FALSE":
                env.last_eval = eval_word(env, ifs['false'])
            else:
                raise("If statement incorrectly specified: " + json.dumps(ifs))
        elif "wait" in step:
            duration = as_number(env, step['wait'])
            time.sleep(duration) # TODO: verify server is still responsive while sleeping
        else:
            raise("Could not evaluate step: " + json.dumps(step))

    # Try to interpret as number or error


def as_number(env, v):
    if isinstance(v, numbers.Number):
        return float(v)

    # Otherwise try to evaluate it...
    evaled_v = eval_word(env, v)
    return float(evaled_v)


# TODO: evaluate words in parallel
def eval_word(env, word):
    if word[0] == r'@':
        ref = word[2:-1] # indexed to cut off brackerts. Probably better to do this at the parse step...
        if ref == '0':
            return env.last_eval
        return env.params[ref]
    elif word[0] == r'$':
        task_to_eval = word[2:-1] # TODO: functify
        return eval_task(env, task_to_eval)
    else:
        return word


def parse_statement(statement: str):
    # TODO: it'd be nice if  we didn't have to build up this grammar every time...
    # TODO: requires a space (' ') around subtask and reference words (e.g. @ and $)
    identifier = pp.Word(pp.printables)
    pword = pp.White() | pp.Word(pp.printables)
    psubtask = pp.Group("${" + identifier + "}") 
    pref = pp.Group("@{" + identifier + "}")
    pstatement = pp.OneOrMore(psubtask | pref | pword)

    return pstatement.parseString(statement) 