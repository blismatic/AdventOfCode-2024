from main import find_contiguous_free_space, swap

data = list("00...111...2...333.44.5555.6666.777.888899")

free_space_idx = find_contiguous_free_space(data, 2)
fb_start_idx = data.index("9")

swap(data, free_space_idx, fb_start_idx, 2)
print(data)
