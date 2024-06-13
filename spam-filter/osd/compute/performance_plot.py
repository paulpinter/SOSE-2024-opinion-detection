import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if __name__ == "__main__":
  matplotlib.rcParams.update({'font.size': 22})
  meteo = [["B", 0.615, 0.340, 0.217, 0.807, 0.697], ["L", 0.579, 0.297, 0.190, 0.711, 0.636],
           ["I", 0.690, 0.312, 0.211, 0.597, 0.648], ["D", 0.616, 0.344, 0.219, 0.812, 0.700],
           ["All", 0.646, 0.353, 0.229, 0.785, 0.706]]

  df = pd.DataFrame(meteo)
  df.rename(columns={0: "split", 1: "A", 2: "F1", 3: "P", 4: "R", 5: "ROC AUC"}, inplace=True)

  # Setting the positions and width for the bars
  pos = list(range(len(df)))
  num_col = len(df.columns) - 1
  width = 0.95 / num_col

  fig, ax = plt.subplots(figsize=(16, 10), layout='constrained')

  # bar_colors = ['#feb24c', '#f03b20', '#ffeda0', '#43a2ca', '#a8ddb5']
  bar_labels = df.columns[1:]

  for i, (colname,  lbl) in enumerate(zip(df.columns[1:] , bar_labels)):
    delta_p = 0.125 + width * i
    plt.bar([p + delta_p for p in pos], df[colname], width, label=lbl)

  ax.set_ylabel('Score')
  ax.set_xticks(pos)


  def update_ticks(x, pos):
    return df['split'][pos]


  ax.xaxis.set_major_formatter(ticker.NullFormatter())
  ax.xaxis.set_minor_formatter(ticker.FuncFormatter(update_ticks))
  ax.xaxis.set_minor_locator(ticker.FixedLocator([p + 0.5 for p in pos]))
  for tick in ax.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0)
    tick.tick2line.set_markersize(0)
    tick.label1.set_horizontalalignment('center')
  plt.xlim(min(pos), max(pos) + 1)
  plt.ylim([0, 1])
  plt.legend()
  plt.grid()
  plt.savefig('performance_comp.pdf')
  plt.show()
