from abc import ABC, abstractmethod


class Instruction(ABC):
    @abstractmethod
    def execute(self, syntax_tree, environment):
        pass
