from enum import Enum
from itertools import repeat
from typing import Tuple
from src.common.file_utils import read_lines
import re
from pydantic import BaseModel
import concurrent.futures


class FileSegment(BaseModel):
    position: int
    size: int
    file_id: int


class DiskFileSystem:
    def __init__(self):
        self.files: dict[int, list[FileSegment]] = {}
        self.disk_size = 0

    def parse_input(self, input: str):
        pos = 0
        file_id = 0

        numbers = [int(n) for n in re.findall(r"\d", input)]

        for i in range(0, len(numbers)):
            if i % 2 == 0:
                # new file
                self.files.setdefault(file_id, [])
                self.files[file_id].append(
                    FileSegment(position=pos, size=numbers[i], file_id=file_id)
                )

                pos += numbers[i]
                file_id += 1
            else:
                # free space
                pos += numbers[i]

        max_file_id = max(self.files.keys())
        self.disk_size = max([s.position + s.size for s in self.files[max_file_id]])

    def position_is_free(self, position: int):
        for f in self.files:
            for s in self.files[f]:
                if s.position <= position < s.position + s.size:
                    return False

        return True

    # def file_at_position(self,position:int):
    #     for f in self.files:
    #         for s in self.files[f]:
    #             if s.position <= position < s.position + s.size:
    #                 return s.file_id

    #     return -1

    def get_max_file_segment_block(self) -> int:
        return max(s.size + s.position for f in self.files for s in self.files[f])

    def compress_file(self, file_id: int, start_at: int = 0) -> int:

        total_file_len = sum(s.size for s in self.files[file_id])

        absolute_max = self.get_max_file_segment_block()

        can_copy = False
        i = start_at
        while i < absolute_max:
            if self.position_is_free(i):
                # free space
                if not can_copy:
                    copy_start = i
                can_copy = True
                i += 1

            else:
                # already a file here, copy if we can in the previous free space
                if can_copy:
                    can_copy = False
                    free_space = i - copy_start

                    while free_space > 0:
                        if total_file_len <= free_space:
                            # farthest segment only
                            last_file_segment = max(
                                self.files[file_id], key=lambda x: x.position
                            )
                            last_file_segment.position = copy_start
                            return i - free_space

                        else:
                            # split the file and continue
                            last_file_segment = max(
                                self.files[file_id], key=lambda x: x.position
                            )
                            last_file_segment.size -= free_space
                            last_file_segment.position += free_space
                            total_file_len -= free_space
                            self.files[file_id].append(
                                FileSegment(
                                    position=copy_start,
                                    size=free_space,
                                    file_id=file_id,
                                )
                            )
                            free_space = 0
                            copy_start += free_space
                            i += free_space

                else:
                    i += 1
        return i

    def get_file_checksum(self, file_id: int) -> int:
        checksum_positions = 0
        for segments in self.files[file_id]:
            for i in range(segments.size):
                checksum_positions += segments.position + i

        return checksum_positions * file_id

    # def print_disk(self):
    #     for i in range(self.disk_size):
    #         file_id = self.file_at_position(i)
    #         if file_id >= 0:
    #             print(file_id,end="")
    #         else:
    #             print(".",end="")
    #     print()

    def compress_with_fragmentation(self) -> int:

        files = sorted(self.files.keys(), reverse=True)
        checksum = 0

        last_processed = 0
        for f in files:
            max_segment = max(self.files[f], key=lambda x: x.position)
            if max_segment.position + max_segment.size < last_processed:
                file_checksum = self.get_file_checksum(f)
                # print(f"File {f} cannot be compressed, checksum is {file_checksum}")
                checksum += file_checksum

                # self.print_disk()
                continue

            last_processed = self.compress_file(f, last_processed)
            file_checksum = self.get_file_checksum(f)
            # print(f"File {f} compressed, resuming at {last_processed}/{self.disk_size}, checksum is {file_checksum}")
            checksum += file_checksum
            # self.print_disk()

        return checksum

    def compact(self) -> int:
        files = sorted(self.files.keys(), reverse=True)
        nb_files = len(files)
        checksum = 0

        # by definition, all files will only have one segment

        for f in files:
            f_pos = self.files[f][0].position
            f_size = self.files[f][0].size

            sorted_files = sorted(
                self.files.keys(), key=lambda x: self.files[x][0].position
            )

            for i in range(1, nb_files):

                prev_file = sorted_files[i - 1]
                next_file = sorted_files[i]

                prev = self.files[prev_file][0].position + self.files[prev_file][0].size

                if f_pos < prev:
                    break

                next = self.files[next_file][0].position
                gap = next - prev

                if f_size <= gap:
                    self.files[f][0].position = prev
                    # self.print_disk()
                    break

            file_checksum = self.get_file_checksum(f)
            checksum += file_checksum

        return checksum


def solve_part1() -> int:
    # 6283404590840

    # input = read_lines("input/day09/example.txt")[0][:-1]
    input = read_lines("input/day09/part1.txt")[0][:-1]

    fs = DiskFileSystem()
    fs.parse_input(input)
    checksum = fs.compress_with_fragmentation()

    return checksum


def solve_part2() -> int:
    # 6304576012713

    # input = read_lines("input/day09/example.txt")[0][:-1]
    input = read_lines("input/day09/part1.txt")[0][:-1]

    fs = DiskFileSystem()
    fs.parse_input(input)
    checksum = fs.compact()

    return checksum
