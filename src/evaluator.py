import json
import sys
filepath = sys.argv[1]
truth_file = sys.argv[2]
assert len(sys.argv) >= 3 
use_numerals = False if len(sys.argv) < 4 else True
if use_numerals:
    print("Using numerals")

truth_dict = {}
with open(truth_file) as f:
    for line in f.read().splitlines():
        ls = line.split("\t")
        truth_dict[ls[0].strip().lower()] = ls[1]

correct_cnt = 0
correct_top2_cnt = 0
correct_top3_cnt = 0
num_probes = 0
mismatches = 0
mismatches_top2 = 0
mismatches_top3 = 0
with open(filepath) as f:
    for line in f.read().splitlines():
        if not line:
            continue
        data = json.loads(line)
        data["probe"] = data["probe"].strip().lower()
        assert data["probe"] in truth_dict, data["probe"]
        num_probes += 1
        assert len(data["result_list"]) >= 1
        truth = truth_dict[data["probe"]]
        # deal with the ambiguitiy of no/zero
        if truth == "no":
            truth = "zero"  # always use zero
        result_list = ["zero" if item["word"] == "no" else item["word"]
                       for item in data["result_list"]]
        non_numerals_result_list = []
        if use_numerals:
            non_numerals_result_list = result_list
            result_list = [""] * len(data["result_list"])
            for i, item in enumerate(data["result_list"]):
                d = item["word"]
                if d == "no" or d == "0":
                    d = "zero"
                elif d == "1":
                    d = "one"
                elif d == "2":
                    d = "two"
                elif d == "3":
                    d = "three"
                elif d == "4":
                    d = "four"
                elif d == "5":
                    d = "five"
                elif d == "6":
                    d = "six"
                elif d == "7":
                    d = "seven"
                elif d == "8":
                    d = "eight"
                elif d == "9":
                    d = "nine"
                elif d == "10":
                    d = "ten"

                result_list[i] = d

        if truth == result_list[0]:
            if non_numerals_result_list and truth != non_numerals_result_list[0]:
                mismatches += 1
            correct_cnt += 1
        if truth in result_list[:2]:
            if non_numerals_result_list and truth not in non_numerals_result_list[:2]:
                mismatches_top2 += 1
            correct_top2_cnt += 1
        if truth in result_list[:3]:
            if non_numerals_result_list and truth not in non_numerals_result_list[:3]:
                mismatches_top3 += 1
            correct_top3_cnt += 1

print(filepath)
print("num_probes:", num_probes)
print("top1-acc:", correct_cnt/num_probes)
print("top2-acc:", correct_top2_cnt/num_probes)
print("top3-acc:", correct_top3_cnt/num_probes)
if use_numerals:
    print("mismatches top1:", mismatches/num_probes)
    print("mismatches top2:", mismatches_top2/num_probes)
    print("mismatches top3:", mismatches_top3/num_probes)
# print(truth_dict)
