import subprocess

# Define the command to run the script and redirect output to a file

# # Use subprocess to run the command
# subprocess.run(command, shell=True)
# file_names = ['test_results/unconstrained/bert-base.test.new.unconstrained.jsonl', 'test_results/unconstrained/bert-large.test.new.unconstrained.jsonl',
#               'test_results/unconstrained/roberta-large.test.new.unconstrained.jsonl', 'test_results/unconstrained/roberta-base.test.new.unconstrained.jsonl']

files_names = ['bert-large.test.new.output_with_numerals.jsonl', 'bert-base.test.new.output_with_numerals.jsonl',  'bert-large.test.new.output.only_numerals.jsonl', 'bert-base.test.new.output.only_numerals.jsonl', 'gpt.test.new.output.jsonl', 'ft_roberta_large_45en5.test.new.output.jsonl', 'inference_t5-large.test.new.jsonl', 'inference_t5-small.test.new.jsonl', 'bert-base.test.new.output.jsonl', 'roberta-base.test.new.output.jsonl', 'ft_roberta_large_6464642.test.new.output.jsonl',
               'ft_bert_large_6464642.test.new.output.jsonl', 'roberta-large.test.new.output.jsonl', 'inference_t5-base.test.new.jsonl', 'roberta-large.test.new.output.only_numerals.jsonl', 'gpt.test.new.output.only_numerals.jsonl', 'roberta-base.test.new.output_with_numerals.jsonl', 'bert-large.test.new.output.jsonl', 'roberta-large.test.new.output_with_numerals.jsonl', 'roberta-base.test.new.output.only_numerals.jsonl', 'gpt.test.new.output_with_numerals.jsonl']

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

for results_path in files_names:
    results_path = results_path.replace("test_results/", "")
    is_numeral = "numeral" in results_path
    numeral_addition = " True" if is_numeral else ""
    truth_file = "test.new.answers.txt"
    command = f"python src/evaluator.py test_results/{results_path} data/{truth_file}{numeral_addition} > evaluated_test_results/{results_path}"
    # print(command)
    out = subprocess.run(
        command, shell=True, capture_output=True)
    if out.stdout:
        print(out.stdout)
    if out.stderr:
        print(out.stderr)
