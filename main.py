#! usr/bin/env python2

"""
Analyze the computer inventory data released by the Department of Energy
by Allan Lasser (@allanlasser) for MuckRock (@muckrock)
2016-08-02
"""

import datetime
import json
import operator

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

def sort_reduce(histogram, limit):
    """Sorts and reduces a histogram to only include items up to the "limit,"
    and combining all the rest into an "Other" bucket."""
    sorted_histogram = sorted(histogram.items(), key=operator.itemgetter(1))
    sorted_histogram.reverse()
    if len(sorted_histogram) > limit:
        # if more items than our limit allows, combine all the trailing values
        # since we sorted the histogram, we're dealing with an array of arrays
        combined_value = 0
        for bucket in sorted_histogram[limit:]:
            combined_value += bucket[-1]
        sorted_histogram = sorted_histogram[:limit]
        sorted_histogram.append(["Other", combined_value])
    return dict(sorted_histogram)

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
        manufacturer = computer.get(u'Manufacturer', u'').title()
        if manufacturer:
            if manufacturer in histogram:
                histogram[manufacturer] += 1
            else:
                histogram[manufacturer] = 1
    return histogram

def index_manufacturer_by_year(data):
    """First indexes aquisitions by manufacturer, then counts them by year."""
    _index = {}
    for computer in data:
        # For each manufacturer, we list the computers with that type
        manufacturer = computer.get(u'Manufacturer', u'').title()
        if manufacturer:
            if manufacturer in _index:
                _index[manufacturer].append(computer)
            else:
                _index[manufacturer] = [computer]
    for manufacturer in _index:
        _index[manufacturer] = count_by_year(_index[manufacturer])
    return _index

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
    # sort and reduce the histogram before recording it
    mfg_count = count_by_manufacturer(data)
    mfg_count = sort_reduce(mfg_count, 5)
    write_json('./output/doe.mfg.json', mfg_count)
    # index manufacturer by year
    type_index = index_manufacturer_by_year(data)
    write_json('./output/doe.mfg.year.json', type_index)
    # index type of computer by manufacturer
    type_index = index_acquisitions(data)
    write_json('./output/doe.index.json', type_index)

