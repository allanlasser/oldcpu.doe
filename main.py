#! usr/bin/env python2

"""
Analyze the computer inventory data released by the Department of Energy
by Allan Lasser (@allanlasser) for MuckRock (@muckrock)
2016-08-02
"""

import datetime
import json

def read_json(filename):
    """Opens a JSON file and returns the data"""
    f = open(filename)
    data = json.load(f)
    return data

def write_json(filename, data):
    """Opens a file and writes data to it in JSON format."""
    f = open(filename, 'w')
    json_data = json.dumps(data)
    f.write(json_data)
    f.close()
    return json_data

def count_by_year(data):
    """Counts the total number of computers by the year they were aquired."""
    histogram = {}
    for computer in data:
        date = computer.get(u'Acquisition Date')
        if date:
            year = datetime.datetime.strptime(date, '%m/%d/%Y').year
            if year in histogram:
                histogram[year] += 1
            else:
                histogram[year] = 1
    return histogram

def count_by_manufacturer(data):
    """Counts the total number of computers by manufacturer."""
    histogram = {}
    for computer in data:
        manufacturer = computer.get(u'Manufacturer')
        if manufacturer:
            if manufacturer in histogram:
                histogram[manufacturer] += 1
            else:
                histogram[manufacturer] = 1
    return histogram

def index_acquisitions(data):
    """Indexes the type of acquisition by category and then by manufacturer."""
    index = {}
    for computer in data:
        # For each type of item, we list the computers with that type
        name = computer.get(u'Official Name')
        if name:
            if name in index:
                index[name].append(computer)
            else:
                index[name] = [computer]
    for name in index:
        # We use the list of computers as the input for the counting method
        index[name] = count_by_manufacturer(index[name])
    return index   

if __name__ == '__main__':        
    data = read_json('./input/doe.json')
    # count computers by year
    year_count = count_by_year(data)
    write_json('./output/doe.year.json', year_count)
    # count computers by manufacturer
    mfg_count = count_by_manufacturer(data)
    write_json('./output/doe.mfg.json', mfg_count)
    # index type of computer by manufacturer
    type_index = index_acquisitions(data)
    write_json('./output/doe.index.json', type_index)

