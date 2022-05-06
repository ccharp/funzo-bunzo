from re import I
import interpreter as fbi # <-- funzo bunzo interpreter
import json

def test_execute():
    inpt = """
    {
        "entry_point": "hello_world",
        "tasks": {
            "hello_world": {
                "output": "hello world!"
            }
        }
    }
    """

    actual = fbi.execute(json.loads(inpt), {})
    expected = "hello world!"
    assert actual == expected

    inpt_steps = """
    {
        "entry_point": "name_classifier",
        "tasks": {
        "name_is_long_or_short": {
            "steps": [
            {
                "length": "@{name}"
            },
            {
                "gt": [
                "@{0}",
                7
                ]
            },
            {
                "if": {
                "condition": "@{0}",
                "true": "long name",
                "false": "short name"
                }
            }
            ]
        },
        "name_classifier": {
            "output": "@{name} is a ${name_is_long_or_short}"
        }
        }
    }
    """
    actual = fbi.execute(json.loads(inpt_steps), {"name": "BunzFunz"})
    expected = "BunzFunz is a long name"
    assert actual == expected


    # TODO: test weight
    # TODO: test 
    # TODO: test error cases! 


"""
def test_parse():
    print(fb.parse_statement(r'Hello: foo @{name} is a ${name_is_long_or_short} !!!'))
"""




