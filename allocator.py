import sys


class MemoryBlock:
    """Represents one contiguous block of memory."""

    def __init__(self, start, size, process=None):
        self.start = start
        self.size = size
        self.process = process

    @property
    def end(self):
        return self.start + self.size - 1

    @property
    def is_free(self):
        return self.process is None


class MemoryAllocator:
    """
    Simulates contiguous memory allocation using:
    First Fit, Best Fit, and Worst Fit.
    """

    def __init__(self, total_size):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]

    def process_exists(self, pid):
        return any(
            not block.is_free and block.process == pid
            for block in self.blocks
        )

    def allocate(self, pid, size, strategy):
        if size <= 0:
            print(f"Error: Invalid size {size} for process {pid}")
            return

        if self.process_exists(pid):
            print(f"Error: Process {pid} already allocated")
            return

        strategy = strategy.upper()

        if strategy not in {"F", "B", "W"}:
            print(f"Error: Unknown strategy {strategy}")
            return

        holes = [
            block
            for block in self.blocks
            if block.is_free and block.size >= size
        ]

        if not holes:
            print(
                f"Error: Cannot allocate {size} bytes "
                f"for process {pid}"
            )
            return

        if strategy == "F":
            chosen = holes[0]

        elif strategy == "B":
            chosen = min(
                holes,
                key=lambda block: block.size
            )

        else:
            chosen = max(
                holes,
                key=lambda block: block.size
            )

        index = self.blocks.index(chosen)

        allocated = MemoryBlock(
            chosen.start,
            size,
            pid
        )

        remaining = chosen.size - size

        if remaining == 0:
            self.blocks[index] = allocated
        else:
            free_block = MemoryBlock(
                chosen.start + size,
                remaining
            )

            self.blocks[index:index + 1] = [
                allocated,
                free_block
            ]

    def release(self, pid):
        found = False

        for block in self.blocks:
            if (
                not block.is_free
                and block.process == pid
            ):
                block.process = None
                found = True

        if not found:
            print(f"Warning: Process {pid} not found")
            return

        self.merge_adjacent_holes()

    def merge_adjacent_holes(self):
        index = 0

        while index < len(self.blocks) - 1:
            current = self.blocks[index]
            following = self.blocks[index + 1]

            if current.is_free and following.is_free:
                current.size += following.size
                del self.blocks[index + 1]
            else:
                index += 1

    def compact(self):
        allocated_blocks = [
            block
            for block in self.blocks
            if not block.is_free
        ]

        new_blocks = []
        next_address = 0

        for block in allocated_blocks:
            new_blocks.append(
                MemoryBlock(
                    next_address,
                    block.size,
                    block.process
                )
            )

            next_address += block.size

        free_size = self.total_size - next_address

        if free_size > 0:
            new_blocks.append(
                MemoryBlock(
                    next_address,
                    free_size
                )
            )

        self.blocks = new_blocks

    def status(self):
        for block in self.blocks:
            if block.is_free:
                print(
                    f"Addresses "
                    f"[{block.start}:{block.end}] "
                    f"Unused"
                )
            else:
                print(
                    f"Addresses "
                    f"[{block.start}:{block.end}] "
                    f"Process {block.process}"
                )


def print_usage():
    print(
        "Usage: python allocator.py <memory_size>"
    )


def main():
    if len(sys.argv) != 2:
        print_usage()
        return

    try:
        total_size = int(sys.argv[1])

        if total_size <= 0:
            raise ValueError

    except ValueError:
        print(
            "Error: memory_size must be "
            "a positive integer"
        )
        return

    allocator = MemoryAllocator(total_size)

    while True:
        try:
            command_line = input(
                "allocator> "
            ).strip()

        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not command_line:
            continue

        parts = command_line.split()
        command = parts[0].upper()

        try:
            if command == "RQ" and len(parts) == 4:
                pid = parts[1]
                size = int(parts[2])
                strategy = parts[3]

                allocator.allocate(
                    pid,
                    size,
                    strategy
                )

            elif command == "RL" and len(parts) == 2:
                allocator.release(parts[1])

            elif command == "C" and len(parts) == 1:
                allocator.compact()

            elif command == "STAT" and len(parts) == 1:
                allocator.status()

            elif command == "X" and len(parts) == 1:
                break

            else:
                print("Invalid command.")

        except ValueError:
            print(
                "Error: size must be an integer"
            )


if __name__ == "__main__":
    main()