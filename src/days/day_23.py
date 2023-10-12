import asyncio

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import IntcodeEmulator
from src.module.io import ints

puzzle = Puzzle(year=2019, day=23)


class NodeQueue(asyncio.Queue):
    async def get(self):
        await asyncio.sleep(0.1)  # allow for context switching

        if self.empty():
            return -1
        else:
            return self.get_nowait()


class Listener:
    def __init__(self, target: IntcodeEmulator, network):
        self._network = network
        self._target = target

    async def run(self):
        while not self._target.terminated:
            # Do not want to mess with a sentinel, so a dirtier loop without await.
            try:
                # No interruption.
                r = self._target.outputs.get_nowait()
                x = self._target.outputs.get_nowait()
                y = self._target.outputs.get_nowait()
                await self.send(x, y, r)
            except asyncio.QueueEmpty:
                await asyncio.sleep(0.1)

    async def send(self, x, y, r):
        if r == 255 and self._network.nat is None:
            puzzle.answer_a = y
            raise SystemExit
        elif r == 255:
            self._network.nat.receive(x, y)
        else:
            # No interruption.
            print(f"Paging {r} (x={x}, y={y})")
            self._network.nodes[r].inputs.put_nowait(x)
            self._network.nodes[r].inputs.put_nowait(y)


class Network:
    def __init__(self, size, nat=None):
        self._listeners = []
        self._size = size

        self.nat = nat
        self.nodes = []

    @property
    def is_idle(self):
        return min([x.outputs.empty() for x in self.nodes]) and min(
            [x.inputs.empty() for x in self.nodes]
        )

    async def _create_listeners(self):
        for node in self.nodes:
            self._listeners.append(Listener(node, self))

    async def _create_nodes(self):
        for i in range(self._size):
            node = IntcodeEmulator(
                ints(Puzzle(year=2019, day=23).input_data), NodeQueue()
            )
            node.inputs.put_nowait(i)
            self.nodes.append(node)

    async def run(self):
        await self._create_nodes()
        await self._create_listeners()
        if self.nat:
            self.nat.set_network(self)

        nodes = [x.run() for x in self.nodes]
        listeners = [x.run() for x in self._listeners]
        nat = [self.nat.run()] if self.nat else []

        await asyncio.gather(*nodes, *listeners, *nat)


# PART 1

network = Network(50)
asyncio.run(network.run())


# PART 2


class Nat:
    def __init__(self):
        self._network = None
        self._x = None
        self._y = None

        self._last_y = None

    def receive(self, x, y):
        self._x = x
        self._y = y

    async def run(self):
        while True:
            if self._network.is_idle and self._x is not None:
                print(f"NAT transmits (x={self._x}, y={self._y})")
                self.send()
            else:
                await asyncio.sleep(1)

    def send(self):
        if self._last_y == self._y:
            puzzle.answer_b = self._y
            raise SystemExit
        else:
            self._network.nodes[0].inputs.put_nowait(self._x)
            self._network.nodes[0].inputs.put_nowait(self._y)
            self._last_y = self._y

    def set_network(self, n):
        self._network = n


network = Network(50, Nat())
asyncio.run(network.run())
