import json
import sys
filepath = sys.argv[1]
truth_file = sys.argv[2]
assert len(sys.argv) >= 3 

NUMERALS = [str(i) for i in range(11)]
WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "no", "zero"]

truth_dict = {}
with open(truth_file) as f:
    for line in f.read().splitlines():
        ls = line.split("\t")
        truth_dict[ls[0].strip().lower()] = ls[1]

numeral = [0,0,0]
words = [0,0,0]
other = [0,0,0]
total = 0
with open(filepath) as f:
    for line in f.read().splitlines():
        if not line:
            continue
        data = json.loads(line)
        data["probe"] = data["probe"].strip().lower()
        assert data["probe"] in truth_dict, data["probe"]
        assert len(data["result_list"]) == 3
        truth = truth_dict[data["probe"]]
        # deal with the ambiguitiy of no/zero
        if truth == "no":
            truth = "zero"  # always use zero
        results = [(item["word"], item["score"]) for item in data["result_list"]]
        results = sorted(results, key=lambda x: x[1], reverse=True)
        results = [i[0] for i in results]
        total += 1
        if results[0] in NUMERALS:
          numeral[0] += 1
        elif results[0] in WORDS:
          words[0] += 1
        else:
          other[0] += 1
        if results[0] in NUMERALS or results[1] in NUMERALS:
          numeral[1] += 1
        elif results[0] in WORDS or results[1] in WORDS:
          words[1] += 1
        if (results[0] not in NUMERALS and results[0] in WORDS) or (results[1] not in NUMERALS and results[1] in WORDS):
          other[1] += 1
        if results[0] in NUMERALS or results[1] in NUMERALS or results[2] in NUMERALS:
          numeral[2] += 1
        elif results[0] in WORDS or results[1] in WORDS or results[2] in WORDS:
          words[2] += 1
        if (results[0] not in NUMERALS and results[0] in WORDS) or (results[1] not in NUMERALS and results[1] in WORDS) or (results[2] not in NUMERALS and results[2] in WORDS):
          other[2] += 1

print("Percentage of numerals", [n/total for n in numeral])
print("Percentage of number words", [n/total for n in words])
print("Percentage of other", [n/total for n in other])

