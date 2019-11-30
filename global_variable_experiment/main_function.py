from global_variable_experiment import globals
from global_variable_experiment import usage

if __name__ == "__main__":
    globals.initialize()
    print(globals.var)
    usage.add(5)
    print(globals.var)
    usage.add(10)
    print(globals.var)
    usage.add(20)
    print(globals.counter())