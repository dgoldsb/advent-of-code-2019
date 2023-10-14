from typing import TypeVar, Generic

from src.module.a_star.base_node import BaseNode

NodeType = TypeVar("NodeType", bound=BaseNode)


class BaseGraphBuilder(Generic[NodeType]):
    def __init__(self, raw_input: str):
        self._raw_input = raw_input
        self._nodes = []

    def _parse_nodes(self):
        raise NotImplementedError()

    def _get_start(self) -> NodeType:
        raise NotImplementedError()

    def build(self) -> NodeType:
        self._parse_nodes()
        return self._get_start()
