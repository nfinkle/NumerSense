import matplotlib.pyplot as plt
import os
import re
import matplotlib.colors as mcolors


directory = "evaluated_test_results/"

results = []

bert_base = []
bert_large = []
roberta_base = []
roberta_large = []

only_numerals_suffix = "O.N."
with_numerals_suffix = "W.N."

for filename in sorted(os.listdir(directory)):
    if "ft_" in filename: continue
    if "gpt" in filename: continue
    if filename.endswith(".jsonl"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            contents = f.read()
            # num_probes = re.search(r"num_probes: (\d+)", contents).group(1)
            top1_acc = float(re.search(r"top1-acc: ([\d.]+)", contents).group(1))
            top2_acc = float(re.search(r"top2-acc: ([\d.]+)", contents).group(1))
            top3_acc = float(re.search(r"top3-acc: ([\d.]+)", contents).group(1))
            results.append({
                "filename": os.path.basename(filename).replace(".jsonl", "").replace(".test.new.", ".").replace(".output", '').replace(".only_numerals", " " + only_numerals_suffix).replace("_with_numerals", " " + with_numerals_suffix),
                "acc": [top1_acc, top2_acc, top3_acc],
                "top1_acc": top1_acc,
                "top2_acc": top2_acc,
                "top3_acc": top3_acc
            })

for f in results:
  filename = f['filename']
  # acc = f['acc']
  if "bert-base" in filename: bert_base.append(f)
  if "bert-large" in filename: bert_large.append(f)
  if "roberta-base" in filename: roberta_base.append(f)
  if "roberta-large" in filename: roberta_large.append(f)


def build_horiz_bars(results):
  hit1 = [0.0] * 4
  hit2 = [0.0] * 4
  hit3 = [0.0] * 4
  for res in results:
    acc = res['acc']
    acc = [i * 100 for i in acc]
    if only_numerals_suffix in res['filename']:
      hit1[2] = acc[0]
      hit2[2] = acc[1]
      hit3[2] = acc[2]
    elif with_numerals_suffix in res['filename']:
      hit1[1] = acc[0]
      hit2[1] = acc[1]
      hit3[1] = acc[2]
    else:
      hit1[0] = acc[0]
      hit2[0] = acc[1]
      hit3[0] = acc[2]
  return hit1, hit2, hit3 


# plot each line
for f in results:
    filename = f['filename']
    acc = f['acc']
    print(filename, acc)
#     ax.plot(value``, label=key)
fig, ax = plt.subplots()

def plot_model(results, ax, model_title):
  return build_horiz_bars(results)
  # for f in results:
  #   filename = f['filename']
  #   acc = f['acc']
  #   ax.plot(acc, label=filename)
  #   ax.set_title(model_title)

  # ax.legend()
  # ax.set_xticks(range(0,3), ['Hit@1', 'Hit@2', 'Hit@3'], fontsize=14)

# def build_bar(filename, )

h1, h2, h3 = plot_model(bert_base, ax, "bert_base")
j1, j2, j3 = plot_model(roberta_base,ax , "roberta_base")
h1.extend(j1)
h2.extend(j2)
h3.extend(j3)
j1, j2, j3 = plot_model(bert_large, ax,  "bert_large")
h1.extend(j1)
h2.extend(j2)
h3.extend(j3)
j1,j2,j3 = plot_model(roberta_large, ax, "roberta_large")
h1.extend(j1)
h2.extend(j2)
h3.extend(j3)
h1 = h1[:-1]
h2 = h2[:-1]
h3 = h3[:-1]

plt.bar(range(15), h3, label='Hit@3', color=mcolors.CSS4_COLORS['plum'])
for i, v in enumerate(h3):
   if v > 0:
    plt.text(i, v + 1, str(round(v, 2)), ha='center', fontsize=6)
plt.bar(range(15), h2, label='Hit@2',
        color=mcolors.CSS4_COLORS['mediumorchid'])
plt.bar(range(15), h1, label='Hit@1', color=mcolors.CSS4_COLORS['darkviolet'])
for i, v in enumerate(h2):
   if v > 0:
    plt.text(i, v + 1, str(round(v, 2)), ha='center', fontsize=6)
  
for i, v in enumerate(h1):
   if v > 0:
    plt.text(i, v + 1, str(round(v, 2)), ha='center', fontsize=6)
plt.axhline(y=88.3, linestyle='--', color='green', label="Human Closed Book")


big_model_names = ['Bert\nBase',  'RoBERTa  \nBase ',
                   'Bert\nLarge', 'RoBERTa  \nLarge']
model_names = []
for m in big_model_names:
  for a in ['',  ' ' + with_numerals_suffix, ' ' + only_numerals_suffix]:
    if a:
      model_names.append(a)
    else: model_names.append(m)
  model_names.append('')
model_names = model_names[:-1]
# print(model_names) 
plt.xticks(range(15), model_names, rotation=0, fontsize=7)
plt.yticks([i for i in range(0,110, 10)], fontsize=7)
plt.xlabel("Model", fontsize=14)
plt.ylabel("% Accuracy", fontsize=14)
# show the plot
plt.legend(loc='lower center')
plt.title("Model Predictions by Evaluation Method", fontsize=20)
plt.show()

