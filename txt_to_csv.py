from collections import defaultdict
import pandas as pd

def converter():
  # change path to txt file here
  with open("data.txt", "r") as f:
    data = f.read()
    blocks = data.split("*** Circuit ***") # splits the data into a list of blocks for each unique circuit

    stats = defaultdict(list)  # list of lists for each statistic that grows as needed
    i = 0  # tracks index of each statistic

    for block in blocks[1:]:
      index = block.find("Communication time (s)")
      block = block[index:-2]

      lines = block.split('\n')
      block = [line.lstrip() for line in lines]

      for statistic in block:
        colon_index = statistic.find(":")
        open_bracket_index = statistic.find(" (", colon_index, len(statistic))

        if open_bracket_index == -1:
          statistic = statistic[colon_index + 1:]
        else:
          statistic = statistic[colon_index + 1:open_bracket_index]
          
        stats[i].append(statistic)
        i += 1

      i = 0

    df_list = []
    
    while True:
      name = input("Variable Parameter: ") 
      if name == "":
        break
      else:
        start = int(input("Start: "))
        end = int(input("End: "))
        table = buildTable(stats, start, end, name)
        df_list.append(table)
  
  with open("data.csv", "w") as f:
    plain_text = toPlainText(df_list)
    f.write(plain_text)

# generates table for given variable parameter and its data block indexes
def buildTable(stats, start, end, name):
  table = {
      name : "",
      "Communication time (s)": stats[0][start:end + 1],
      "EPR pair generation time (s)": stats[1][start:end + 1],
      "EPR pair distribution time (s)": stats[2][start:end + 1],
      "Pre-processing time (s)": stats[3][start:end + 1],
      "Classical transfer time (s)": stats[4][start:end + 1],
      "Post-processing time (s)": stats[5][start:end + 1],
      "Computation time (s)": stats[6][start:end + 1],
      "Fetch time (s)": stats[7][start:end + 1],
      "Decode time (s)": stats[8][start:end + 1],
      "Dispatch time (s)": stats[9][start:end + 1],
      "Execution time (s)": stats[10][start:end + 1],
      "Coherence (%)": stats[11][start:end + 1]
  }
  
  df = pd.DataFrame(table)
  return df

# converts dataframes to plain text for csv file
def toPlainText(df_list):
  plain_text = ""
  for df in df_list:
    text = df.to_csv(index=False)
    plain_text += "\n" + text + "\n"
  return plain_text

if __name__ == "__main__":
  converter()