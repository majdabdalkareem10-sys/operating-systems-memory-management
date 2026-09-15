# Operating Systems Memory Management Simulator

A Python project that demonstrates two fundamental operating-system memory management techniques:

1. Contiguous Memory Allocation
2. Paging

The project was originally developed for the ENCS3390 Operating System Concepts course and later reviewed and refactored for portfolio documentation.

## Contiguous Memory Allocation

The allocator simulates a contiguous memory region and supports:

- First Fit
- Best Fit
- Worst Fit
- Process allocation
- Process release
- Adjacent-hole merging
- Memory compaction
- Memory status reporting

### Run

```bash
python allocator.py 1048576