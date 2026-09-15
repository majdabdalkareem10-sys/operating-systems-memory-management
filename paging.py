import sys


class Frame:
    """Represents one fixed-size physical memory frame."""

    def __init__(self):
        self.pid = None
        self.page = None

    @property
    def is_free(self):
        return self.pid is None

    def clear(self):
        self.pid = None
        self.page = None


class PagingSystem:
    """
    Simulates a paging system with fixed-size frames.
    """

    def __init__(self, num_frames, frame_size):
        self.frames = [
            Frame()
            for _ in range(num_frames)
        ]

        self.frame_size = frame_size

        # Keeps track of the next page number
        # for each process.
        self.next_page = {}

    def allocate(self, pid, page_count):
        if page_count <= 0:
            print(
                "Error: Number of pages must "
                "be greater than zero"
            )
            return

        free_frames = [
            index
            for index, frame
            in enumerate(self.frames)
            if frame.is_free
        ]

        if len(free_frames) < page_count:
            print(
                f"Error: Not enough free frames "
                f"for {pid}"
            )
            return

        first_page = self.next_page.get(
            pid,
            0
        )

        for offset in range(page_count):
            frame_index = free_frames[offset]
            frame = self.frames[frame_index]

            frame.pid = pid
            frame.page = first_page + offset

        self.next_page[pid] = (
            first_page + page_count
        )

    def release(self, pid):
        found = False

        for frame in self.frames:
            if frame.pid == pid:
                frame.clear()
                found = True

        if not found:
            print(
                f"Warning: Process {pid} not found"
            )
            return

        self.next_page.pop(pid, None)

    def status(self):
        for index, frame in enumerate(self.frames):
            if frame.is_free:
                print(
                    f"Frame {index}: Free"
                )
            else:
                print(
                    f"Frame {index}: "
                    f"Process {frame.pid}, "
                    f"Page {frame.page}"
                )

    def translate(self, pid, page, offset):
        if page < 0:
            print(
                "Error: Page number cannot "
                "be negative"
            )
            return

        if offset < 0 or offset >= self.frame_size:
            print(
                f"Error: offset {offset} "
                f"out of range "
                f"(0-{self.frame_size - 1})"
            )
            return

        for frame_index, frame in enumerate(
            self.frames
        ):
            if (
                frame.pid == pid
                and frame.page == page
            ):
                physical_address = (
                    frame_index
                    * self.frame_size
                    + offset
                )

                print(
                    f"Physical address = "
                    f"{physical_address}"
                )
                return

        print(
            f"Error: Process {pid} "
            f"has no page {page}"
        )


def print_usage():
    print(
        "Usage: python paging.py "
        "<num_frames> <frame_size>"
    )


def main():
    if len(sys.argv) != 3:
        print_usage()
        return

    try:
        num_frames = int(sys.argv[1])
        frame_size = int(sys.argv[2])

        if num_frames <= 0 or frame_size <= 0:
            raise ValueError

    except ValueError:
        print(
            "Error: num_frames and frame_size "
            "must be positive integers"
        )
        return

    paging = PagingSystem(
        num_frames,
        frame_size
    )

    while True:
        try:
            command_line = input(
                "paging> "
            ).strip()

        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not command_line:
            continue

        parts = command_line.split()
        command = parts[0].upper()

        try:
            if command == "RQ" and len(parts) == 3:
                pid = parts[1]
                pages = int(parts[2])

                paging.allocate(
                    pid,
                    pages
                )

            elif command == "RL" and len(parts) == 2:
                paging.release(parts[1])

            elif command == "STAT" and len(parts) == 1:
                paging.status()

            elif command == "TR" and len(parts) == 4:
                pid = parts[1]
                page = int(parts[2])
                offset = int(parts[3])

                paging.translate(
                    pid,
                    page,
                    offset
                )

            elif command == "X" and len(parts) == 1:
                break

            else:
                print("Invalid command.")

        except ValueError:
            print(
                "Error: Numeric values must "
                "be valid integers"
            )


if __name__ == "__main__":
    main()