import asyncio
import itertools
from copy import copy
from dataclasses import dataclass
from typing import Generator

from aocd.models import Puzzle

import src.module.io  # set the session cookie
from src.module.intcode_emulator import AsciiComputer, IntcodeState
from src.module.io import ints

puzzle = Puzzle(year=2019, day=25)


@dataclass(frozen=True)
class GameState:
    items: tuple[str]
    room: str


class GamePlayingEngine:
    def __init__(self):
        first_emulator, first_screen = AsciiComputer.process_state(
            IntcodeState(0, 0, tuple(ints(puzzle.input_data))), ""
        )
        first_room = self.__parse_room(first_screen)
        first_state = GameState(tuple(), first_room)

        self.__visited_states = set()

        # TODO: Hash might not work, use sorted items and location instead
        self.__state_pool: set[GameState] = {first_state}
        self.__state_emulator_map: dict[GameState, IntcodeState] = {
            first_state: first_emulator
        }
        self.__state_item_map: dict[GameState, set[str]] = {first_state: set()}
        self.__state_screen_map: dict[GameState, str] = {first_state: first_screen}
        self.__take_move_cache = {}
        self.__drop_move_cache = {}

    @staticmethod
    def __parse_room(screen: str):
        for line in screen.split("\n"):
            if line.startswith("=="):
                return line[3:-3]
        else:
            raise ValueError("No room found")

    def solve(self):
        while self.__state_pool:
            state = self.__state_pool.pop()
            screen = self.__state_screen_map[state]
            items = self.__state_item_map[state]
            emulator = self.__state_emulator_map[state]

            possible_moves = list(self.get_possible_moves(screen, items))

            # If there is no direction move...
            if all(move[0].startswith("drop") for move in possible_moves):
                try:
                    possible_moves = self.__take_move_cache.pop(state)
                except KeyError:
                    possible_moves = self.__drop_move_cache.pop(state)

            for move, new_items in possible_moves:
                new_emulator, new_screen = AsciiComputer.process_state(emulator, move)
                try:
                    room = self.__parse_room(new_screen)
                except ValueError:
                    room = state.room

                if room == "Pressure-Sensitive Floor":
                    if (
                        "Alert! Droids on this ship are heavier than the detected value!"
                        in new_screen
                    ):
                        pass
                    elif (
                        "Alert! Droids on this ship are lighter than the detected value!"
                        in new_screen
                    ):
                        pass
                    else:
                        print(new_screen)
                        print("\n\n\n")
                        raise ValueError("Donfdfsdfdsfe")

                new_state = GameState(tuple(sorted(new_items)), room)

                # For a take move, cache the other moves.
                if move.startswith("take"):
                    self.__take_move_cache[new_state] = [
                        (m, new_items)
                        for m, _ in possible_moves
                        if not m.startswith("take")
                    ]

                # For a drop move, cache all other moves.
                if move.startswith("drop"):
                    self.__drop_move_cache[new_state] = [
                        (m, new_items) for m, _ in possible_moves if m != move
                    ]

                if new_state not in self.__visited_states:
                    self.__state_pool.add(new_state)
                    self.__state_item_map[new_state] = new_items
                    self.__state_screen_map[new_state] = new_screen
                    self.__state_emulator_map[new_state] = new_emulator

            self.__visited_states.add(state)
            if state in self.__state_pool:
                self.__state_pool.remove(state)
                del self.__state_screen_map[state]
                del self.__state_emulator_map[state]

    @staticmethod
    def get_possible_moves(
        screen: str, items: set[str]
    ) -> Generator[tuple[str, set[str]], None, None]:
        """
        Return a list of possible moves.
        """
        parsing_doors = False
        parsing_items = False

        for line in screen.split("\n"):
            match line.split(" "):
                case ("Doors", "here", "lead:"):
                    parsing_doors = True
                case ("Items", "here:"):
                    parsing_items = True
                case ("-", item) if parsing_items:
                    new_items = copy(items)
                    new_items.add(item)
                    yield f"take {item}", new_items
                case ("-", direction) if parsing_doors:
                    yield direction, items
                case _:
                    parsing_doors = False
                    parsing_items = False

        # TODO: Remove all dropping!
        # for item in items:
        #     new_items = copy(items)
        #     new_items.remove(item)
        #     yield f"drop {item}", new_items


GamePlayingEngine().solve()
raise RuntimeError("Done")
