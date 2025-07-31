import pandas as pd

def converter():
  # change path to txt file here
  with open("data.txt", "r") as f:
    data = f.read()
    blocks = data.split("Circuit:") # splits data simulations into a list of blocks for each simulation

    # each key stores a list of statistics
    stats = {}
    for i in range(12):
      stats[i] = []

    i = 0  # reset i to track index of each statistic later

    for block in blocks[1:]:
      # filters out every line before communication_time for each block
      start_index = block.find("communication_time:")
      end_index = block.find("#   __ _  ___ ___  _ __ ___  _ __ ___")
      block = block[start_index : end_index - 2]

      # removes whitespace from each line
      lines = block.split('\n')
      block = []
      for line in lines:
        stripped_line = line.lstrip()
        block.append(stripped_line)

      # filters out heading and "percent: " lines
      for statistic in block:
        colon_index = statistic.find("e:")
        open_bracket_index = statistic.find(" #")

        if colon_index != -1 and open_bracket_index != -1:
          statistic = statistic[colon_index + 3 : open_bracket_index]
          stats[i].append(statistic)
          i += 1
        else:
          pass

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
  
  # change path to csv file here
  with open("data.csv", "w") as f:
    plain_text = toPlainText(df_list)
    f.write(plain_text)

# generates table for given variable parameter and its data block indexes
def buildTable(stats, start, end, name):
  table = {
      name : "",
      "Communication time (s)": stats[0][start : end + 1],
      "EPR pair generation time (s)": stats[1][start : end + 1],
      "EPR pair distribution time (s)": stats[2][start : end + 1],
      "Pre-processing time (s)": stats[3][start : end + 1],
      "Classical transfer time (s)": stats[4][start : end + 1],
      "Post-processing time (s)": stats[5][start : end + 1],
      "Computation time (s)": stats[6][start : end + 1],
      "Fetch time (s)": stats[7][start : end + 1],
      "Decode time (s)": stats[8][start : end + 1],
      "Dispatch time (s)": stats[9][start : end + 1],
      "Execution time (s)": stats[10][start : end + 1],
      "Coherence (%)": stats[11][start : end + 1]
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