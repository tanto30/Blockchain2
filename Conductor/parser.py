from manager import Manager
from cmd import Cmd
from sys import exit

class Parser(Cmd):
    intro = "Welcome to conductor. Use '?' command to get help"
    prompt = "Conductor > "

    def __init__(self):
        super(Parser, self).__init__()
        self.manager = Manager()

    def do_run(self, arg):
        '''
        Runs x instances of nodes
        :param arg: number of nodes to run
        '''
        if arg.isdigit():
            num = int(arg)
            self.manager.run(num)

    def do_stop(self, arg):
        '''
        Stops all current node instances
        '''
        self.manager.stop()

    def do_mine(self, arg):
        '''
        Sends a mine request to all nodes
        '''
        self.manager.mine()

    def do_register(self, arg):
        '''
        Sends a register request from each node to all others
        '''
        self.manager.register_all()

    def do_kgraph(self, arg):
        '''
        Builds the graph that represents which node registered which
        '''
        self.manager.kgraph()

    def do_resolve(self, arg):
        '''
        Demonstrates resolving algorithm by mining a block on all nodes
        and another one on one of them then resolves
        '''
        self.manager.mine()
        self.manager.mine_one()
        self.manager.resolve()

    def do_exit(self, arg):
        '''
        exit the CLI tool
        '''
        self.manager.stop()
        exit(0)


Parser().cmdloop()
