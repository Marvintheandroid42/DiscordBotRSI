import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def rsi(acronym, startDate, endDate):
  stock = pd.DataFrame(yf.download(acronym, start=startDate, end=endDate))

  adjClose = np.array(stock["Close"])

  shiftedAdjClose = np.array(stock["Close"].shift(1))

  posChange = shiftedAdjClose-adjClose
  negChange = shiftedAdjClose-adjClose

  posChange[np.where(posChange < 0)] = 0
  negChange[np.where(negChange > 0)] = 0

  posChange = np.abs(posChange)
  negChange = np.abs(negChange)

  p1 = 1
  p2 = 14

  rsi = [] 

  intPosMean = np.mean(posChange[p1:p2])
  intNegMean = np.mean(negChange[p1:p2])

  currentAvgPos = intPosMean
  currentAvgNeg = intNegMean
  
  p2 = 15
  

  while p2 < np.size(posChange):
    currentAvgPos = ((currentAvgPos*13)+(posChange[p2]))/14
    currentAvgNeg = ((currentAvgNeg*13)+(negChange[p2]))/14
    rsi.append(100-(100/((currentAvgPos/currentAvgNeg)+1)))
  #avgPos.append(currentAvgPos)
  #avgNeg.append(currentAvgNeg)
    p2 += 1

  l1 = [30,30]
  l2 = [70,70]
  y1 = [stock.index[15:][0],stock.index[15:][len(stock.index[15:])-1]]
  fig, ax = plt.subplots(2, sharex=True)
  ax[0].plot(stock.index[15:], rsi)
  ax[0].set_title("RSI")
  ax[1].plot(stock.index[15:], adjClose[15:], color="tomato")
  ax[1].set_title("Close Price")
  ax[0].plot(y1,l1)
  ax[0].plot(y1,l2)
  plt.suptitle(f"RSI and Close Price for {acronym}")

  try:
    os.remove(r"rsiPlot.png")
  except:
    pass

  plt.savefig(r"rsiPlot.png")

  return list(rsi)[-1]


