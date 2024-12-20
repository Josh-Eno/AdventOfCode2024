from functools import cache

class Matcher:
    def __init__(self, strings):
        self.strings = strings
    
    # This effetively memo-izes the call, so we only compute any given string or substring once.
    @cache
    def match(self, string) -> int:
        match_count = 0
        if len(string) > 0:
            for pattern in self.strings:
                if pattern == string:
                    match_count += 1
                    continue
                if string.startswith(pattern):
                    new_str = string[len(pattern):]
                    remainder_match_cnt = self.match(new_str)
                    if remainder_match_cnt > 0:
                        match_count += remainder_match_cnt

        return match_count
                
input_file = open("./advent_of_code_2024/josh/day19/input.txt").read().splitlines()
input_test = [
    "r, wr, b, g, bwu, rb, gb, br",
    "",
    "brwrr",
    "bggr",
    "gbbr",
    "rrbgbr",
    "ubwu",
    "bwurrg",
    "brgr",
    "bbrgwb",
]

input = input_file
strings = set(input[0].split(", "))
targets = input[2:]

matches = []
match_count = 0
misses = []
matcher = Matcher(strings)
for target in targets:
    target_cnt = matcher.match(target)
    if target_cnt > 0:
        matches.append(target)
        match_count += target_cnt
    else:
        misses.append(target)

print(f"Match count: {len(matches)}, miss count: {len(misses)}, variations: {match_count}")