import random
import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MultipleLocator, ScalarFormatter
import csv
import pandas as pd
from datetime import datetime
import os
import threading

autoSave = True
bubbleTimes, mergeTimes, countTimes, stoogeTimes = [], [], [], []
sizes = []



def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        mergeSort(left_half)
        mergeSort(right_half)
        
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


def countSort(arr):
    M = max(arr) if arr else 0
    count_array = [0] * (M + 1)

    for num in arr:
        count_array[num] += 1

    output_array = []
    for num, count in enumerate(count_array):
        output_array.extend([num] * count)

    return output_array


def stoogeSort(arr, l, h):
    if l >= h:
        return
    if arr[l] > arr[h]:
        arr[l], arr[h] = arr[h], arr[l]
    if h - l + 1 > 2:
        t = (h - l + 1) // 3
        stoogeSort(arr, l, h - t)
        stoogeSort(arr, l + t, h)
        stoogeSort(arr, l, h - t)
    return arr





def randomList(size, maxValue=1000, startValue=0):
    return [random.randint(0, maxValue) for _ in range(size+startValue)]

def timeSort(sortFunction, lst, *args):
    startTime = time.time()
    sortFunction(lst, *args) if args else sortFunction(lst)
    endTime = time.time()
    return (endTime - startTime)

def test(size, jump=1, maxValue=1000, startValue=0):
    global sizes, bubbleTimes, mergeTimes, countTimes, stoogeTimes, itteration, csvData, colLabels, tableData, valueSize
    valueSize = maxValue
    itteration = jump

    sizes = list(range(0+startValue, size + 1, jump))
    pastBubbleTimes, pastMergeTimes, pastCountTimes, pastStoogeTimes = [0], [0], [0], [0]

    for size in sizes:
        print("creating list....")
        lst = randomList(size, maxValue, startValue)
        print(f"Sorting {size} Numbers...")
        if pastBubbleTimes[-1] < 0:
            timing = timeSort(bubbleSort, lst.copy())
            bubbleTimes.append(timing)
            pastBubbleTimes.append(timing)
            print("Bubble Sort done sorting.")
        else:
            print("Number set too large for bubble sort to complete in a reasondable amount of time")
            bubbleTimes.append(None)

        if pastStoogeTimes[-1] < 0:
            timing = timeSort(stoogeSort, lst.copy(), 0, len(lst) - 1)
            stoogeTimes.append(timing)
            pastStoogeTimes.append(timing)
            print("Stooge Sort done sorting.")
        else:
            print("Number set too large for Stooge sort to complete in a reasondable amount of time")
            stoogeTimes.append(None)
        
        if pastMergeTimes[-1] < 0:
            timing = timeSort(mergeSort, lst.copy())
            mergeTimes.append(timing)
            pastMergeTimes.append(timing)
            print("Merge Sort done sorting.")
        else:
            print("Number set too large for Merge sort to complete in a reasondable amount of time")
            mergeTimes.append(None)
        
        if pastCountTimes[-1] < 5:
            timing = timeSort(countSort, lst.copy())
            countTimes.append(timing)
            pastCountTimes.append(timing)
            print("Count Sort done sorting.")
        else:
            print("Number set too large for Count sort to complete in a reasondable amount of time")
            countTimes.append(None)
        
        print(f"Done Sorting {size} Numbers!")

        roundedBubbleTimes = [round(x, 10) if x is not None else "NaN" for x in bubbleTimes]
        roundedMergeTimes = [round(x, 10) if x is not None else "NaN" for x in mergeTimes]
        roundedCountTimes = [round(x, 10) if x is not None else "NaN" for x in countTimes]
        roundedStoogeTimes = [round(x, 10) if x is not None else "NaN" for x in stoogeTimes]
        csvData = {
            "Size": sizes,
            "Bubble Sort": roundedBubbleTimes,
            "Merge Sort": roundedMergeTimes,
            "Count Sort": roundedCountTimes,
            "Stooge Sort": roundedStoogeTimes
        }

        colLabels = ["Size"] + sizes
        tableData = [
    ["Bubble Sort Time(s)"] + roundedBubbleTimes,
    ["Merge Sort Time(s)"] + roundedMergeTimes,
    ["Count Sort Time(s)"] + roundedCountTimes,
    ["Stooge Sort Time(s)"] + roundedStoogeTimes
]
        if autoSave:
            autoSaves()


def autoSaves():
    global autoSave, fileName
    autoSave = True

    os.makedirs("dataLists", exist_ok=True)

    os.makedirs(f"dataLists/AutoSave", exist_ok=True)
    fileName = f"dataLists/AutoSave/Data.csv"

    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = csvData.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in zip(*csvData.values()):
            writer.writerow(dict(zip(fieldnames, row)))


def savaData():
    os.makedirs("dataLists", exist_ok=True)


    timeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    saveFolderName = f"{timeStamp}, Size={sizes[-1]}, Jump={itteration}, Range={valueSize}"
    os.makedirs(f"dataLists/{saveFolderName}", exist_ok=True)

    fileName = f"dataLists/{saveFolderName}/Data.csv"
    imgFileName = f"dataLists/{saveFolderName}/Graph.png"
    tableFileName = f"dataLists/{saveFolderName}/Table.png"


    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = csvData.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in zip(*csvData.values()):
            writer.writerow(dict(zip(fieldnames, row)))


    plt.figure(figsize=(12, 3))
    plt.axis("off")
    table = plt.table(cellText=tableData, colLabels=colLabels, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    plt.title("Sorting Times for Bubble Sort, Merge Sort, Count Sort, and Stooge Sort")
    plt.savefig(tableFileName, format="png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(sizes, bubbleTimes, label="Bubble Sort")
    plt.plot(sizes, mergeTimes, label="Merge Sort", linestyle=":")
    plt.plot(sizes, countTimes, label="Count Sort", linestyle="--")
    plt.plot(sizes, stoogeTimes, label="Stooge Sort", linestyle="-.")
    plt.xlabel("List Size")
    plt.ylabel("Time (seconds)")
    plt.title("Comparison of Sorting Algorithms")
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    plt.legend()
    plt.savefig(imgFileName, format="png")
    plt.close()
    
    if os.path.exists("dataLists/AutoSave/Data.csv"):
        os.remove("dataLists/AutoSave/Data.csv")
    print("Data and graphs saved.")



test(1000000000, startValue=1000000000, jump=1, maxValue=100)

savaData()

