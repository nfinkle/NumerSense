import subprocess

# Define the command to run the script and redirect output to a file
command = "python myscript.py > output.txt"

# # Use subprocess to run the command
# subprocess.run(command, shell=True)
file_names = ["bert-base.test.new.output.jsonl",
           "bert-base.test.new.output.only_numerals.jsonl",
           "bert-base.test.new.output_with_numerals.jsonl",
           "bert-large.test.new.output.jsonl",
           "bert-large.test.new.output.only_numerals.jsonl",
           "bert-large.test.new.output_with_numerals.jsonl",
           "ft_bert_large_6464642.test.new.output.jsonl",
           "ft_roberta_large_6464642.test.new.output.jsonl",
           "gpt.test.new.output.jsonl",
           "gpt.test.new.output.only_numerals.jsonl",
           "gpt.test.new.output_with_numerals.jsonl",
           "roberta-base.test.new.output.jsonl",
           "roberta-base.test.new.output.only_numerals.jsonl",
           "roberta-base.test.new.output_with_numerals.jsonl",
           "roberta-large.test.new.output.jsonl",
           "roberta-large.test.new.output.only_numerals.jsonl",
           "roberta-large.test.new.output_with_numerals.jsonl"]

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
    is_numeral = "numeral" in results_path
    numeral_addition = "True" if is_numeral else ""
    truth_file = "test.new.answers.txt"
    subprocess.run(f"python src/evaluator.py test_results/{results_path} data/{truth_file} {numeral_addition} > evaluated_test_results/{results_path}", shell=True)