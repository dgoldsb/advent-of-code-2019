"""Intcode emulator for Advent of Code 2019."""
import asyncio
import logging
import typing
from copy import copy


class IntcodeEmulator:
    def __init__(self, program, inputs=None, name="default"):
        self._pointer: int = 0
        self._program: typing.List[int] = copy(program)
        self._relative_base = 0
        self._state: typing.List[int] = copy(program)

        self.inputs: asyncio.Queue = inputs
        self.name = name
        self.outputs = asyncio.Queue()
        self.terminated = False
        self.waiting = False

    @property
    def state(self):
        return self._state

    def reset(self):
        self._pointer = 0
        self._relative_base = 0
        self._state = self._program
        self.terminated = False

    async def run(self):
        while not self.terminated:
            output = await self._run_next_opcode()
            if output is not None:
                logging.debug("%s: PUT %s", self.name, output)
                self.outputs.put_nowait(output)

    def _extend_to(self, index):
        if index >= len(self._state):
            extension = [0] * (index - len(self._state) + 1)
            self._state = self._state + extension

    def _get_command_string(self) -> str:
        command = str(self._state[self._pointer])

        while len(command) < 5:
            command = "0" + command

        return command

    def _get_mode(self, index: int) -> int:
        """
        Get the mode for the parameter that is that is <index> away from the pointer.
        """
        return int(self._get_command_string()[3 - index])

    def _get_opcode(self):
        return int(self._get_command_string()[-2:])

    def _get_parameter(self, index: int) -> int:
        """Get the parameter that is <index> away from the pointer."""
        self._extend_to(self._pointer + index)
        p = self._state[self._pointer + index]

        if self._get_mode(index) == 0:
            self._extend_to(p)
            return self._state[p]
        elif self._get_mode(index) == 1:
            return p
        elif self._get_mode(index) == 2:
            self._extend_to(self._pointer + self._relative_base)
            return self._state[self._relative_base + p]
        else:
            raise ValueError(f"Invalid get mode: {self._get_mode(index)}")

    def _store_parameter(self, index: int, value):
        self._extend_to(self._pointer + index)
        p = self._state[self._pointer + index]

        logging.debug("%s: STORE TO %s", self.name, p)
        logging.debug("%s: STORE VALUE %s", self.name, value)

        if self._get_mode(index) == 0:
            self._extend_to(p)
            self._state[p] = value
        elif self._get_mode(index) == 2:
            self._extend_to(self._pointer + self._relative_base)
            self._state[self._relative_base + p] = value
        else:
            raise ValueError(f"Invalid store mode: {self._get_mode(index)}")

    async def _run_next_opcode(self):
        opcode = self._get_opcode()

        if opcode == 1:
            # addition
            result = self._get_parameter(1) + self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 2:
            # multiplication
            result = self._get_parameter(1) * self._get_parameter(2)
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 3:
            # input
            inp = await self.inputs.get()
            logging.debug("%s: GET %s", self.name, inp)
            self._store_parameter(1, inp)
            self._pointer += 2
        elif opcode == 4:
            # output
            result = self._get_parameter(1)
            self._pointer += 2
            return result
        elif opcode == 5:
            # jump-if-true
            if bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 6:
            # jump-if-false
            if not bool(self._get_parameter(1)):
                self._pointer = self._get_parameter(2)
            else:
                self._pointer += 3
        elif opcode == 7:
            # less-than
            result = int(self._get_parameter(1) < self._get_parameter(2))
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 8:
            # equals
            result = int(self._get_parameter(1) == self._get_parameter(2))
            self._store_parameter(3, result)
            self._pointer += 4
        elif opcode == 9:
            # adjust-relative-base
            self._relative_base += self._get_parameter(1)
            self._pointer += 2
        elif opcode == 99:
            # terminate
            logging.debug(f"%s: TERM", self.name)
            self.terminated = True
        else:
            raise ValueError(
                f"{opcode} is not an intcode operator (pointer={self._pointer})"
            )


class AsciiComputerExit(Exception):
    pass


class AsciiComputer:
    def __init__(self, program):
        self._emulator = None
        self._io_history = []
        self._program = program

    async def give_input(self, inputs: str):
        assert isinstance(self._emulator, IntcodeEmulator)

        if inputs == "exit":
            raise AsciiComputerExit
        else:
            self._io_history.append(inputs)

            for char in inputs:
                self._emulator.inputs.put_nowait(ord(char))

            await self._emulator.inputs.put(ord("\n"))

    def render(self):
        assert isinstance(self._emulator, IntcodeEmulator)

        outputs = []
        while not self._emulator.outputs.empty():
            outputs.append(self._emulator.outputs.get_nowait())

        image = [chr(x) for x in outputs]
        print("".join(image))
        return image

    async def io_loop(self, instructions):
        last_render = self.render()

        while not self._emulator.terminated:
            if last_render:
                try:
                    i = next(instructions)
                except StopIteration:
                    i = input("Give a command: ")

                await self.give_input(i)
            else:
                await asyncio.sleep(1)

            last_render = self.render()

    async def run(self, instructions=None):
        self._emulator = IntcodeEmulator(self._program, asyncio.Queue())

        # TODO: make this an iterable that is iterated over...
        # TODO: make the thing raise an error if the door test is failed.
        # TODO: use itertools to try all drop combinations, see where no error is
        #  raised by following with an exit.

        instructions = instructions or iter([])
        tasks = [self._emulator.run(), self.io_loop(instructions)]

        try:
            await asyncio.gather(*tasks)
        except AsciiComputerExit:
            pass

        return self._io_history
