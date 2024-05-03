'''
Population.py
C. Harrington, P. Nguyen
Last Updated 5/2/2024
This modules contains data from the world census as found on wikipedia
and combines that information with world caloric information and 
basic population modeling provide a interesting measurement of suffering.
[https://github.com/charrington1521/PopulationDynamicsModeling]
'''

#====================================[IMPORTS]=================================

import numpy as np

from os.path import basename, exists

def download(url):
    '''
    Downloads a file found at the given url
        Provided by ??????
    '''
    filename = basename(url)
    if not exists(filename):
        from urllib.request import urlretrieve
        local, _ = urlretrieve(url, filename)
        print('Downloaded ' + local)

download('https://github.com/AllenDowney/ModSimPy/raw/master/' +
         'modsim.py')

from modsim import *

#===============================[CONSTANTS]===================================

DAYS_IN_YEAR = 365

#==================================[DATA]=====================================

#The data collected from Wikipedia is done in accordance with the following
#resource: https://allendowney.github.io/ModSimPy/
#Particularly Chapters 5-8
filename = 'https://en.wikipedia.org/wiki/Estimates_of_historical_world_population'
tables = pd.read_html(filename, header=0, index_col=0, decimal='M')

world_census_table = tables[2] #The table with the census data in it
world_census_table.columns = ['census', 'prb', 'un', 'maddison',
                              'hyde', 'tanton', 'biraben', 'mj',
                              'thomlinson', 'durand', 'clark']
census = world_census_table.census / 1e9

t_0 = census.index[0] #The first year in the census
t_f = census.index[-1] #The last year in the census

p_0 = census[t_0]

alpha = 25 / 1000   #Value provided by above resource
beta = -1.8 / 1000  #Value provided by above resource

#Calorie information is taken from the following sources:
#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6198966/
#https://www.fao.org/faostat/en/#data/CL 

cal_per_day = 2200
cal_per_year = cal_per_day * DAYS_IN_YEAR #Calories per person per year

#Calories availble per person per day in 2016 as in above resource
measured_cal_per_day_2016 = 2750 
measured_cal_per_year_2016 = measured_cal_per_day_2016 * DAYS_IN_YEAR

year_2016 = census.index[2016 - t_0]
people_2016 = census[year_2016] * 10 ** 9
measured_cal_total_2016 = measured_cal_per_year_2016 * people_2016

'''
Here a system object is created for the module. Module users may edit the 
system to change parameters of the simulations.
'''
system = System(t_0 = t_0,
                t_f = t_f,
                p_0 = p_0,
                alpha = alpha,
                beta = beta,
                cal_per_day = cal_per_day,
                total_calories = measured_cal_total_2016)

#=================================[METHODS]====================================

def carrying_capacity(system):
    '''
    Calculates the carrying capacity of a system which has 
        an alpha and beta
        resource: https://allendowney.github.io/ModSimPy/
    '''
    K = -system.alpha / system.beta
    return K

def growth_func_quad(t, pop, system):
    '''
    Logisitc growth model for population, requires 'alpha' and 'beta'
        in the given system. 
        resource: https://allendowney.github.io/ModSimPy/
    '''
    return system.alpha * pop + system.beta * pop**2

def calculate_suffering(system, population):
    '''
    Given a system and the current population (not in billions), uses calorie 
    information to calculate what percentage of calories people are missing 
    from the assumed baseline everyday diet
    '''
    cal_per_person_for_year = system.total_calories / population
    cal_per_person_per_day = cal_per_person_for_year / DAYS_IN_YEAR

    if (cal_per_person_per_day < system.cal_per_day):
        return 1 - (cal_per_person_per_day / system.cal_per_day)
    else:
        return 0
    
def run_simulation(system, growth_func):
    '''
    Given a system and a model for growth, runs a simulation 
    modified from: https://allendowney.github.io/ModSimPy/
    '''
    population_results = TimeSeries()
    suffering_results = TimeSeries()

    #Initial values for the results series
    population_results[system.t_0] = system.p_0
    suffering_results[system.t_0] = calculate_suffering(system, system.p_0)

    #Simulate one year at a time
    for t in range(system.t_0, system.t_f):
        growth = growth_func(t, population_results[t], system)

        current_population = population_results[t] + growth 

        population_results[t+1] = current_population #In Billions

        suffering = calculate_suffering(system, current_population * 10 ** 9)

        suffering_results[t+1] = suffering

    
    return population_results, suffering_results

#====================================[EOF]=======================================