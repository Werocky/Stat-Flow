import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

#calculate the weekly flow
def graphic(values):
    directory = "./static/plots/weekReport.png"
    elements = []
    for value in values:
        try:
            elements.append(value['_total'])
        except:
            elements.append(0)
    plt.plot(np.arange(7)[::-1], elements[::-1])
    plt.ylabel("Flow")
    plt.xlabel("Days ago")
    plt.title("Daily flow during the past 7 days")
    plt.savefig(directory)
    plt.clf()
    plt.cla()
    plt.close()
    return directory

#calculate the histogram of flow types with the weekly data
def histogram(values):
    directory = "./static/plots/histogram.png"
    elements = {}
    elements["invalid"] = 0
    for value in values:
        try:
            if not isinstance(value, int):
                    for key in value.keys():
                        try:
                            elements[key] += value[key]
                        except:
                            elements[key] = value[key]
                    #elements.append(value['_total'])
                    print("\n\n\n value:")
                    print(value)
                    print(value.keys())
                    print(type(value))
            else:
                elements["invalid"] += 1
        except:
            elements["invalid"] += 1
    del elements['invalid']
    #del elements['_total']
    plt.bar(elements.keys(), list(elements.values()))
    plt.ylabel("Flow")
    plt.xlabel("Types")
    plt.savefig(directory)
    plt.clf()
    plt.cla()
    plt.close()
    return directory

#calculate the vehicles of each day from db
def calculateTraffic(samples):
    try:
        individual = {}
        for key in samples.keys():  #key id of the sector (ex: 85433220-847d-4580-a946-acd8c497fd3c)
            print(samples[key])

            for k in samples[key].keys():   #key type:_total, car, truck, etc
                try:
                    individual[k] += samples[key][k]    #sum all the classes of same kind
                except KeyError:
                    individual[k] = samples[key][k]     #start to initial value if not present in keys
    except:
        individual = 0
    return individual