from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def execute(self, syntax_tree, environment):
        pass
