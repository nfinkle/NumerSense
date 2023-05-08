import subprocess

# Define the command to run the script and redirect output to a file

# # Use subprocess to run the command
# subprocess.run(command, shell=True)
file_names = ['test_results/unconstrained/bert-base.test.new.unconstrained.jsonl', 'test_results/unconstrained/bert-large.test.new.unconstrained.jsonl',
              'test_results/unconstrained/roberta-large.test.new.unconstrained.jsonl', 'test_results/unconstrained/roberta-base.test.new.unconstrained.jsonl']

# file_names = ['bert-base.test.all.output.new.jsonl',
#               'bert-base.test.core.output.new.jsonl',
#               'bert-large.test.all.output.new.jsonl',
#               'bert-large.test.core.output.new.jsonl',
#               'gpt.test.all.output.new.jsonl',
#               'gpt.test.core.output.new.jsonl',
#               'roberta-base.test.all.output.new.jsonl',
#               'roberta-base.test.core.output.new.jsonl',
#               'roberta-large.test.all.output.new.jsonl',
#               'roberta-large.test.core.output.new.jsonl']

for results_path in file_names:
    results_path = results_path.replace("test_results/", "")
    is_numeral = "numeral" in results_path
    numeral_addition = "True" if is_numeral else ""
    truth_file = "test.new.answers.txt"
    subprocess.run(f"python src/evaluator_non_words.py test_results/{results_path} data/{truth_file} {numeral_addition} > evaluated_test_results/{results_path}", shell=True)