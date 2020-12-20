#!/usr/bin/env python3
import math
import os
import re
import sys
from typing import Dict, Iterator, List, Set, Tuple
import numpy as np


class Tile:
    CORNER_COORDS = [(0, 0), (-1, 0), (-1, -1), (0, -1)]
    BORDER_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # [right, down, left, up]
    TILE_DIRECTIONS = [BORDER_DIRECTIONS[-1]] + BORDER_DIRECTIONS[:-1]  # [up, right, down, left]

    def __init__(self, tile_id: int, bits: List[List[str]]) -> None:
        self.id = tile_id
        self.bits = bits
        self.length = len(bits)
        self.checksums = list(map(self.calculate_checksum, range(4)))
        self.inverse_checksums = list(map(self.calculate_inverse_checksum, range(4)))

    def calculate_checksum(self, border: int) -> int:
        return int(''.join(self.iterate_border_bits(border)), base=2)

    def calculate_inverse_checksum(self, border: int) -> int:
        return int(''.join(self.iterate_border_bits(border))[::-1], base=2)

    def iterate_border_bits(self, border: int) -> Iterator[str]:
        # Note: Can also be implemented by numpy indexing but it seems to require more distinction of cases.
        x, y = self.CORNER_COORDS[border]
        dx, dy = self.BORDER_DIRECTIONS[border]
        for _ in range(self.length):
            yield self.bits[y][x]
            x += dx
            y += dy


class Solver:
    sea_monster_description = ["                  # ",
                               "#    ##    ##    ###",
                               " #  #  #  #  #  #   "]

    def __init__(self, filepath: str) -> None:
        with open(filepath, 'r') as text_file:
            self.groups = list(map(lambda data: data.split('\n'), text_file.read().rstrip().split('\n\n')))
        self.tiles = {}  # type: Dict[int, Tile]
        self.corners = {}  # type: Dict[int, Set[int]]
        self.placements = {}  # type: Dict[int, Tuple[int, int]]
        self.arrangements = {}  # type: Dict[int, Tuple[int, bool]]
        self.image_tile_count = 0
        self.image_tile_ids = []  # type: List[List[int]]

    @staticmethod
    def calculate_match_direction(direction: int, flip: bool) -> int:
        return (2 - direction if direction % 2 == 0 else direction) if flip else (direction + 2) % 4

    @staticmethod
    def convert_array_to_lines(image: np.ndarray) -> List[str]:
        return [''.join(columns) for columns in image.tolist()]

    @classmethod
    def convert_image_to_string(cls, image: np.ndarray) -> str:
        return ''.join(cls.convert_array_to_lines(image))

    @classmethod
    def compose_monster_hunter_regex(cls, image_length: int) -> str:
        padding = '.' * (image_length - len(cls.sea_monster_description[0]))
        return padding.join(line.replace(' ', '.') for line in cls.sea_monster_description)

    def parse_tiles(self, groups: List[List[str]]) -> None:
        for lines in groups:
            match_result = re.search(r'\d+', lines[0])
            if match_result:
                tile_id = int(match_result.group(0))
            else:
                sys.tracebacklimit = 0
                raise ValueError("No ID found for:\n{}".format('\n'.join(lines)))

            bits = np.array([['1' if char == '#' else '0' for char in line] for line in lines[1:]])
            self.tiles[tile_id] = Tile(tile_id, bits)
        self.image_tile_count = int(math.sqrt(len(self.tiles)))
        self.image_tile_ids = [[0] * self.image_tile_count for _ in range(self.image_tile_count)]

    def find_non_matching_borders(self, tile: Tile) -> Set[int]:
        borders = set(range(4))
        for check in self.tiles.values():
            if check != tile:
                for border in borders:
                    checksum = tile.checksums[border]
                    if checksum in check.checksums or checksum in check.inverse_checksums:
                        borders.remove(border)
                        break
        return borders

    def arrange_top_left_tile(self, tile_id: int) -> None:
        borders = self.corners[tile_id]
        self.placements[tile_id] = (0, 0)
        self.arrangements[tile_id] = (0 if borders == {0, 3} else max(borders), False)
        self.image_tile_ids[0][0] = tile_id

    def get_rearranged_checksums(self, tile_id: int) -> List[int]:
        tile = self.tiles[tile_id]
        rotate, flip = self.arrangements[tile_id]
        # Note: First rotate counter-clockwise, then flip left-right.
        results = tile.checksums[rotate:] + tile.checksums[:rotate]
        if flip:
            results[1:] = results[:0:-1]
        return results

    def match_tile(self, tile_id: int, direction: int) -> int:
        x, y = self.placements[tile_id]
        dx, dy = Tile.TILE_DIRECTIONS[direction]
        x += dx
        y += dy
        checksum = self.get_rearranged_checksums(tile_id)[direction]
        _, flip = self.arrangements[tile_id]
        for check in self.tiles.values():
            if check.id != tile_id:
                if checksum in check.checksums:
                    matched_tile = check
                    flip = not flip
                    match_direction = self.calculate_match_direction(direction, flip)
                    rotate = (check.checksums.index(checksum) - match_direction) % 4
                    break

                if checksum in check.inverse_checksums:
                    matched_tile = check
                    match_direction = self.calculate_match_direction(direction, flip)
                    rotate = (check.inverse_checksums.index(checksum) - match_direction) % 4
                    break
        else:
            sys.tracebacklimit = 0
            raise ValueError(f"Cannot match tile {tile_id} in direction {direction}!")

        self.placements[matched_tile.id] = (x, y)
        self.arrangements[matched_tile.id] = (rotate, flip)
        self.image_tile_ids[y][x] = matched_tile.id
        return matched_tile.id

    def get_arranged_bits(self, tile_id: int) -> np.ndarray:
        results = np.array(self.tiles[tile_id].bits)
        rotate, flip = self.arrangements[tile_id]
        results = np.rot90(results, k=rotate)
        if flip:
            for index, columns in enumerate(results):
                results[index] = np.array(columns[::-1])
        return results

    def get_cut_tile(self, tile_id: int) -> np.ndarray:
        bits = self.get_arranged_bits(tile_id)
        bits = np.delete(np.delete(np.delete(np.delete(bits, 0, 0), -1, 0), 0, 1), -1, 1)
        bits = np.array([['#' if bit == '1' else '.' for bit in columns] for columns in bits])
        return bits

    def write_arrangement(self, cut: bool=False) -> None:
        lines = [''] * (96 if cut else 120)
        with open("arrangement.txt", 'w') as text_file:
            for i in range(self.image_tile_count):
                line_index = 0
                for j in range(self.image_tile_count):
                    tile_id = self.image_tile_ids[j][i]
                    bits = self.get_cut_tile(tile_id) if cut else self.get_arranged_bits(tile_id)
                    for line in self.convert_array_to_lines(bits):
                        if i > 0 and not cut:
                            lines[line_index] += ' '
                        lines[line_index] += line
                        line_index += 1
            text_file.write('\n'.join(lines))

    def extract_image(self) -> np.ndarray:
        image = self.get_cut_tile(self.image_tile_ids[0][0])
        for j in range(1, self.image_tile_count):
            image = np.concatenate((image, self.get_cut_tile(self.image_tile_ids[j][0])), axis=0)
        for i in range(1, self.image_tile_count):
            sub_image = self.get_cut_tile(self.image_tile_ids[0][i])
            for j in range(1, self.image_tile_count):
                sub_image = np.concatenate((sub_image, self.get_cut_tile(self.image_tile_ids[j][i])), axis=0)
            image = np.concatenate((image, sub_image), axis=1)
        return image

    def get_sea_monster_count(self, image: np.ndarray) -> int:
        pattern = re.compile(self.compose_monster_hunter_regex(len(image)))
        sea_monster_length = len(self.sea_monster_description[0])
        sea_monster_count = 0
        for flip_count in range(2):
            if flip_count > 0:
                for index, columns in enumerate(image):
                    image[index] = np.array(columns[::-1])
            for rotate_count in range(4):
                if rotate_count > 0:
                    image = np.rot90(image)
                string = self.convert_image_to_string(image)
                while True:
                    # Note: This may actually count "sea monsters" which protrude over the one side
                    #   of the image into the next line. Hopefully you didn't get such an image.
                    match_result = re.search(pattern, string)
                    if match_result:
                        sea_monster_count += 1
                        sea_monster_position, _ = match_result.span()
                        string = string[sea_monster_position + sea_monster_length:]
                    else:
                        break
        return sea_monster_count

    def solve_part1(self) -> int:
        self.parse_tiles(self.groups)
        for tile_id, tile in self.tiles.items():
            borders = self.find_non_matching_borders(tile)
            if len(borders) == 2:
                self.corners[tile_id] = borders
        return math.prod(self.corners)

    def solve_part2(self) -> int:
        self.solve_part1()
        row_tile_id = list(self.corners.keys())[0]
        self.arrange_top_left_tile(row_tile_id)
        for row in range(self.image_tile_count):
            if row > 0:
                row_tile_id = self.match_tile(row_tile_id, 2)
            column_tile_id = row_tile_id
            for _ in range(1, self.image_tile_count):
                column_tile_id = self.match_tile(column_tile_id, 1)
        # Note: self.write_arrangement(cut=False) writes the arrangement of tiles to file 'arrangement.txt'.
        image = self.extract_image()
        sea_monster_count = self.get_sea_monster_count(image)
        sea_monter_size = ''.join(self.sea_monster_description).count('#')
        water_roughness = self.convert_image_to_string(image).count('#') - sea_monster_count * sea_monter_size
        return water_roughness


if __name__ == "__main__":
    solver = Solver(os.path.join(os.path.dirname(__file__), "input.txt"))
    print(solver.solve_part1())
    print(solver.solve_part2())
