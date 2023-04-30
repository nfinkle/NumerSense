import argparse
import json

parser = argparse.ArgumentParser(description='Compare model results')
parser.add_argument('new_results', type=str,
                    help='Path to newer model results file')
parser.add_argument('orig_results', type=str,
                    help='Path to original model results file')
parser.add_argument('--output_file', type=str, required=False,
                    help='Path to output file (optional)')
parser.add_argument('--print', action='store_true',
                    help='Print the whole output')

args = parser.parse_args()

# Access the parsed arguments
new_results = args.new_results
orig_results = args.orig_results

def score_replacement(results_dict, probe, to_be_added_to, score, replacement):
    if replacement in to_be_added_to:
      old_score = to_be_added_to[replacement]
      del to_be_added_to[replacement]
      results_dict[probe][replacement] = score + old_score
    elif replacement in results_dict[probe]:
      old_score = results_dict[probe][replacement]
      results_dict[probe][replacement] = score + old_score
    else:
      to_be_added_to[replacement] = score


def get_scores_with_replacements(replacements, filename):
    results_dict = {}
    with open(filename) as f:
        for line in f.read().splitlines():
            if not line:
                continue
            data = json.loads(line)
            data["probe"] = data["probe"].strip().lower()
            probe = data["probe"]
            results_dict[probe] = {}
            to_be_added_to = {}
            for result_dict in data["result_list"]:
              word = result_dict["word"]
              score = result_dict["score"]
              replacement = replacements.get(word)
              if replacement:
                # print("in replacement", word, replacement)
                score_replacement(results_dict, probe, to_be_added_to, score, replacement)
              else:
                results_dict[probe][word] = score
            for word, score in to_be_added_to.items():
              results_dict[probe][word] = score
    return results_dict

orig_dict = get_scores_with_replacements(
    {"no": "zero"}, orig_results)

new_dict = get_scores_with_replacements(
    {"0": "zero", "no": "zero", "1": "one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven","8":"eight", "9":"nine", "10":"ten"}, new_results)

combined = {}
biggest_abs_diff = 0
biggest_abs_diff_probe = None
assert orig_dict.keys() == new_dict.keys()
for probe in orig_dict:
  orig_scores = orig_dict[probe]
  new_scores = new_dict[probe]
  combination = []
  assert sorted(new_scores.keys()) == sorted(orig_scores.keys())
  for word in orig_scores:
    diff = new_scores[word] - orig_scores[word]
    if diff != 0.:
      combination.append((word, new_scores[word] - orig_scores[word]))
  if combination:
    combined[probe] = sorted(combination, key=lambda x: x[1], reverse=True)
    if abs(combined[probe][0][1]) > biggest_abs_diff:
      biggest_abs_diff = combined[probe][0][1]
      biggest_abs_diff_probe = probe

output_file_path = args.output_file
if output_file_path:
  with open(output_file_path, 'w') as f:
    f.write(json.dumps(combined))

if args.print:
  from pprint import pprint
  pprint(combined)

print("Biggest difference:", biggest_abs_diff)
print("Biggest difference probe:", biggest_abs_diff_probe)
