import sys
import os
import time

def process(file_number):
  f_large_name = 'data/C' + file_number
  f_small_name = 'data/C' + file_number + '-OUTPUT.txt'
  blocks = {}
  notes = {}

  count = 0

  start_time = time.time()

  current_index = None
  with open(f_large_name, 'r') as f_large:
    with open(f_small_name, 'r') as f_small:
      for line in f_large.readlines():
        tokens = line.split()
        s = tokens[0]
        if s[0] == 'E' and s[1] == 'A':
          blocks[s] = line
          current_index = s
        else:
          blocks[current_index] += line

      for line in f_small.readlines():
        tokens = line.split()
        if (len(tokens) > 5 and
          tokens[1] == 'keptBest' and
          tokens[2] == '[' and
          tokens[4] == ']' and
          int(tokens[-1]) >= 8):
            count += 1
            if count % 100 == 0:
              print(str(count) + ' - ' + str(time.time() - start_time))

            if tokens[-1] not in notes:
              notes[tokens[-1]] = line
            else:
              notes[tokens[-1]] += line

            index = 'EA' + tokens[0]
            text = blocks[index]
            output_text = []
            for line in text.split('\n'):
              s = line.strip()
              if s == file_number:
                n_space = line.find(file_number)
                output_text.append(' ' * n_space + 'C\n' + ' ' * n_space + file_number)
              else:
                output_text.append(line)
            poscar_text = '\n'.join(output_text)
            output_path = ('result' +
              '/C' + file_number +
              '/C' + file_number + '-' + tokens[-1] +
              '/C' + file_number + '-' + tokens[-1] + '-EA' + tokens[0])
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            with open(output_path + '/POSCAR', 'w') as f:
              f.write(poscar_text)

  for k,v in notes.items():
    with open('result' +
      '/C' + file_number +
      '/C' + file_number + '-' + k +
      '/summary', 'w') as f:
      f.write(v)

  print(count)

if __name__ == "__main__":
  process(sys.argv[1])
