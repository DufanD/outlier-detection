import pandas as pd
import numpy as np
from random import randint
import os

def change_value(values):
  new_values = list()
  for value in values:
    if value == 'A':
      new_values.append(randint(81, 100))
    elif value == 'AB':
      new_values.append(randint(71, 80))
    elif value == 'B':
      new_values.append(randint(66, 70))
    elif value == 'BC':
      new_values.append(randint(61, 65))
    elif value == 'C':
      new_values.append(randint(56, 60))
    elif value == 'D':
      new_values.append(randint(41, 55))
    elif value == 'E':
      new_values.append(randint(0, 40))
    else:
      new_values.append(randint(60, 100))
  return new_values

def find_candidate(lower, upper, values):
  candidates = pd.DataFrame()
  for idx, val in values.iterrows():
    if val['Nilai'] > upper or val['Nilai'] < lower:
      candidates = candidates.append(val)
  return candidates

def fence(lower, upper, values, diff):
  lower -= diff
  upper += diff
  return find_candidate(lower, upper, values)

def inner_fences(lower, upper, values):
  diff = (upper - lower) ** 2
  return fence(lower, upper, values, diff)

def outer_fences(lower, upper, values):
  diff = 2 * (upper - lower) ** 2
  return fence(lower, upper, values, diff)

def calculate_outlier(dataset_path):
  dataset = pd.read_csv(dataset_path)
  i = 0
  while True:
    transformed_data = change_value(dataset['Nilai'])
    median_value = np.median(transformed_data)
    lower_quantile = np.quantile(transformed_data, .25)
    upper_quantile = np.quantile(transformed_data, .75)
    df_dataset = pd.DataFrame({
      'Nama': dataset['NAMA'],
      'Nilai': transformed_data
    })
    minor_outlier = inner_fences(lower_quantile, upper_quantile, df_dataset)
    major_outlier = outer_fences(lower_quantile, upper_quantile, df_dataset)
    i += 1
    if len(major_outlier) > 0:
      break

  print("\nAll dataset : {}".format(sorted(transformed_data)))
  print("Q1 data: {}".format(lower_quantile))
  print("Q3 data: {}".format(upper_quantile))
  print("Minor Outlier : \n{}".format(minor_outlier))
  print("Major Outlier : \n{}".format(major_outlier))
  print("Stop at {}".format(i))

print("Loading ....")
calculate_outlier('dataset/DataWarehouse.csv')
calculate_outlier('dataset/GrafikaKomputer.csv')