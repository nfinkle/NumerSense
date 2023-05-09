import json
import sys
filepath = sys.argv[1]
truth_file = sys.argv[2]
assert len(sys.argv) >= 3 
use_numerals = False if len(sys.argv) < 4 else True
if use_numerals:
    print("Using numerals")

NUMERALS = [str(i) for i in range(11)]
NUMERIC_WORDS = ["one", "two", "three", "four", "five",
                 "six", "seven", "eight", "nine", "ten", "no", "zero"]
truth_dict = {}
with open(truth_file) as f:
    for line in f.read().splitlines():
        ls = line.split("\t")
        truth_dict[ls[0].strip().lower()] = ls[1]

correct_cnt = 0
correct_top2_cnt = 0
correct_top3_cnt = 0
num_probes = 0
pos_correction = 0
neg_correction = 0
pos_correction_top2 = 0
pos_correction_top3 = 0
neg_correction_top2 = 0
neg_correction_top3 = 0

number_word_count_top1 = 0
number_word_count_top2 = 0
number_word_count_top3 = 0
numeral_count_top1 = 0
numeral_count_top2 = 0
numeral_count_top3 = 0

def make_replacement_results(results, old_word, new_word):
    if old_word in results:
        results[new_word] = results[old_word] + \
            results.get(new_word, 0.0)
        del results[old_word]

import copy
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
        results = {item["word"]: item["score"] for item in data["result_list"]}
        make_replacement_results(results, "no", "zero")
        copy_results = copy.copy(results)
        sorted_results = sorted(list(results.keys()), key=lambda x, a=results: a[x], reverse=True)

        if sorted_results[0] in NUMERALS:
            numeral_count_top1 += 1
        else:
            number_word_count_top1 += 1
        if sorted_results[0] in NUMERALS or sorted_results[1] in NUMERALS:
            numeral_count_top2 += 1
        else:
            number_word_count_top2 += 1
        if sorted_results[0] in NUMERALS or sorted_results[1] in NUMERALS or sorted_results[2] in NUMERALS:
            numeral_count_top3 += 1
        else:
            number_word_count_top3 += 1


        sorted_results = list(filter(lambda x,a=NUMERIC_WORDS: x in a, sorted_results))
        non_numerals_sorted_results = []
        if use_numerals:
            non_numerals_sorted_results = sorted_results
            for i, item in enumerate(data["result_list"]):
                d = item["word"]
                if d == "no":
                    make_replacement_results(results, "no", "zero")
                elif d == "0":
                    make_replacement_results(results, "0", "zero")
                elif d == "1":
                    make_replacement_results(results, "1", "one")
                elif d == "2":
                    make_replacement_results(results, "2", "two")
                elif d == "3":
                    make_replacement_results(results, "3", "three")
                elif d == "4":
                    make_replacement_results(results, "4", "four")
                elif d == "5":
                    make_replacement_results(results, "5", "five")
                elif d == "6":
                    make_replacement_results(results, "6", "six")
                elif d == "7":
                    make_replacement_results(results, "7", "seven")
                elif d == "8":
                    make_replacement_results(results, "8", "eight")
                elif d == "9":
                    make_replacement_results(results, "9", "nine")
                elif d == "10":
                    make_replacement_results(results, "10", "ten")
                
            sorted_results = sorted(list(results.keys()), key=lambda x, a=results: a[x], reverse=True)

        if truth == sorted_results[0]:  # hit@1
            correct_cnt += 1
            if non_numerals_sorted_results and truth != non_numerals_sorted_results[0]: # positive correction
                # print("\nPOSITIVE CORRECTION")
                # print(data["probe"], truth)
                # print(copy_results)
                # print(non_numerals_sorted_results)
                # print(results)
                # print(sorted_results)
                pos_correction += 1
        elif non_numerals_sorted_results and truth == non_numerals_sorted_results[0]: # negative correction
            # print("\nNEGATIVE CORRECTION")
            # print(data["probe"], truth)
            # print(copy_results)
            # print(non_numerals_sorted_results)
            # print(results)
            # print(sorted_results)
            neg_correction += 1
        if truth in sorted_results[:2]:  # hit@2
            correct_top2_cnt += 1
            if non_numerals_sorted_results and truth not in non_numerals_sorted_results[:2]:
                # print("\nPOSITIVE CORRECTION")
                # print(data["probe"], truth)
                # print(copy_results)
                # print(non_numerals_sorted_results)
                # print(results)
                # print(sorted_results)
                pos_correction_top2 += 1
        elif non_numerals_sorted_results and truth in non_numerals_sorted_results[:2]: # negative correction
            neg_correction_top2 += 1
            # print("\nNEGATIVE CORRECTION")
            # print(data["probe"], truth)
            # print(copy_results)
            # print(non_numerals_sorted_results)
            # print(results)
            # print(sorted_results)
        if truth in sorted_results[:3]:  # hit@3
            correct_top3_cnt += 1
            if non_numerals_sorted_results and truth not in non_numerals_sorted_results[:3]:
                pos_correction_top3 += 1
        elif non_numerals_sorted_results and truth in non_numerals_sorted_results[:3]: # negative correction
            neg_correction_top3 += 1

print(filepath)
print("num_probes:", num_probes)
print("top1-acc:", correct_cnt/num_probes)
print("top2-acc:", correct_top2_cnt/num_probes)
print("top3-acc:", correct_top3_cnt/num_probes)
if use_numerals:
    print("positive corrections top1:", pos_correction/num_probes)
    print("positive corrections top2:", pos_correction_top2/num_probes)
    print("positive corrections top3:", pos_correction_top3/num_probes)
    print("negative corrections top1:", neg_correction/num_probes)
    print("negative corrections top2:", neg_correction_top2/num_probes)
    print("negative corrections top3:", neg_correction_top3/num_probes)
    print("Number word count top1:", number_word_count_top1/num_probes)
    print("Number word count top2:", number_word_count_top2/num_probes)
    print("Number word count top3:", number_word_count_top3/num_probes)
    print("Numeral count top1:", numeral_count_top1/num_probes)
    print("Numeral count top2:", numeral_count_top2/num_probes)
    print("Numeral count top3:", numeral_count_top3/num_probes)
# print(truth_dict)
