# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import random

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        #creates variable "header" which contains the column titles
        #below, use these headers to find out index position to use (1, 2, 3)
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
                #create dictionary for city, within dictionary of raw data
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
                #create dictionary for year within dictionary of city
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
                #create dictionary for month within dictionary of year
            self.rawdata[city][year][month][day] = temperature
            #add temperature within {CHICAGO:{1961:{May:{1:7.5,2:7}}},NEW YORK: }
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    #sum of squares; estimated y minus actual y, squared and summed
    var_x = ((x - x.mean())**2).sum()
    #variance of x; x minus the mean, squared and summed
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    #this is the standard error of the SLOPE not the mean, so a diff formula
    #square root of sum of squares over n-2, divided by variance of x
    return SE/model[0]
    #return standard error of slope divided by the slope (position 0 in model)

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for d in degs:
        mod = pylab.polyfit(x,y,d)
        models.append(mod)
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    
    numerator = sum((y - estimated)**2)
    denom = sum((y - (sum(y)/len(y)))**2)
    
    return 1 - (numerator/denom)



def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    
    for model in models:
        predict_y = pylab.polyval(model,x)
        r2 = str(round(r_squared(y,predict_y),4))
        deg = str(len(model)-1)
        seos = str(round(se_over_slope(x, y, predict_y, model),4))
        
        
        pylab.plot(x,y,'.b',label="data")
        pylab.plot(x,predict_y,'r',label="predicted")
        pylab.xlabel("Time (years)")
        pylab.ylabel("Temperature (Deg Celsius)")
        
        if len(model)-1 == 1:
            pylab.title("Model of degree: " + deg + "\n" +
                        "R-Squared: " + r2 + "\n" + "SE over Slope :" + seos)
        
        else:
            pylab.title("Model of degree: " + deg + "\n" +
                        "R-Squared: " + r2)       
        pylab.show()
        pylab.close()
        

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """

    
    avg_yearly_temps = pylab.array([])
    
    for year in years:
        avg_multi_city_temps = pylab.array([])
        
        day_length = 0
        for month in range(1,13):
            day_length += len(climate.rawdata[multi_cities[0]][year][month])
    
        for city in multi_cities:
            avg_temp = sum(climate.get_yearly_temp(city,year))/day_length
            avg_multi_city_temps = pylab.append(avg_multi_city_temps,avg_temp)
        avg_year = sum(avg_multi_city_temps)/len(avg_multi_city_temps)
        avg_yearly_temps = pylab.append(avg_yearly_temps, avg_year)
    
    return avg_yearly_temps


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """

    moving_avg_result = pylab.array([])
    for i in range(len(y)):
        numerator = 0
        if (i+1) < window_length:
            for x in range(i+1):
                numerator += y[x]
            denominator = i + 1
        else:
            for x in range(1,window_length+1):
                numerator += y[i-x+1]
            denominator = window_length
        moving_avg_result = pylab.append(moving_avg_result,numerator/denominator)
    
    return moving_avg_result


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return (sum((y-estimated)**2)/len(y))**0.5


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """

    stdev_all_years = pylab.array([])
    
    for year in years:
        
        day_length = 0
        for month in range(1,13):
            day_length += len(climate.rawdata[multi_cities[0]][year][month])
            
        dailytemps_thisyear = pylab.array([0]*day_length)
        yearly_avg = gen_cities_avg(climate,multi_cities,[year])
        
        for city in multi_cities:
            this_city_temps = climate.get_yearly_temp(city,year)
            dailytemps_thisyear = dailytemps_thisyear + this_city_temps
        stdev_this_year = (sum(((dailytemps_thisyear/len(multi_cities))-yearly_avg)**2)
                           / (day_length))**0.5
        stdev_all_years = pylab.append(stdev_all_years,stdev_this_year)
    
    return stdev_all_years



def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        predict_y = pylab.polyval(model,x)
        root_mean_sq_er = str(round(rmse(y, predict_y),4))
        deg = str(len(model)-1)
        
        pylab.plot(x,y,'.b',label="data")
        pylab.plot(x,predict_y,'r',label="predicted")
        pylab.xlabel("Time (years)")
        pylab.ylabel("Temperature (Deg Celsius)")
        pylab.title("Model of degree: " + deg + "\n" +
                        "RMSE: " + root_mean_sq_er)       
        pylab.show()
        pylab.close()

if __name__ == '__main__':

    pass 


"""Part A.4"""

thisclimate = Climate('data.csv')

def temp_one_day(climate,month,day,city,interval,degs):

    """if we were making it random"""
    #    months_w_31 = [1,3,5,7,8,10,12]
    #    months_w_30 = [4,6,9,11]
    #    
    #    month = random.randint(1,13)
    #    
    #    if month in months_w_31:
    #        day = random.randint(1,32)
    #    elif month in months_w_30:
    #        day = random.randint(1,31)
    #    else:
    #        day = random.randint(1,29)
    
    years = pylab.array(interval)
    daily_temps = pylab.array([])
    for year in years:
        daily_temps = pylab.append(daily_temps,
                      climate.get_daily_temp(city.upper(), month, day, year))
    model = generate_models(years,daily_temps,degs)
    evaluate_models_on_training(years,daily_temps, model)
    return daily_temps

#temp_one_day(thisclimate,1,10,"NEW YORK",TRAINING_INTERVAL,[1])  

def temp_one_year(climate,city,interval,degs):
    years = pylab.array(interval)
    avg_yearly_temps = pylab.array([])
    for year in years:
        day_length = 0
        for month in range(1,13):
            day_length += len(climate.rawdata[city][year][month])
        avg_yearly_temps = pylab.append(avg_yearly_temps,
                          sum(climate.get_yearly_temp(city,year))/day_length)
    model = generate_models(years,avg_yearly_temps,degs)
    evaluate_models_on_training(years,avg_yearly_temps,model)  
    return avg_yearly_temps

#temp_one_year(thisclimate,"NEW YORK",TRAINING_INTERVAL,[1]) 
    
"""Part B"""

def national_yearly_temp(climate,multi_cities,interval,degs):
    years = pylab.array(interval)
    national_temps = gen_cities_avg(climate,multi_cities,years)
    model = generate_models(years,national_temps,degs)
    evaluate_models_on_training(years,national_temps,model)
    return national_temps

#national_yearly_temp(thisclimate,CITIES,TRAINING_INTERVAL,[1])

"""Part C"""
def moving_temp_avg_train(climate,multi_cities,interval,window_length,degs):
    years = pylab.array(interval)
    temps = national_yearly_temp(climate,multi_cities,interval,degs)
    train_moving_avgs = moving_average(temps,window_length)
    model = generate_models(years,train_moving_avgs,degs)
    evaluate_models_on_training(years,train_moving_avgs,model)

#moving_temp_avg_train(thisclimate,CITIES,TRAINING_INTERVAL,5,[1])

"""Part D.2"""
#moving_temp_avg_train(thisclimate,CITIES,TRAINING_INTERVAL,5,[1,2,20])

"""Part E"""
def moving_temp_avg_test(climate,multi_cities,test_interval,train_interval,
                         window_length,degs):
    
    test_years = pylab.array(test_interval)
    test_temps = gen_cities_avg(climate,multi_cities,test_years)
    test_moving_avgs = moving_average(test_temps,window_length)
    
    train_years = pylab.array(train_interval)
    train_temps = gen_cities_avg(climate,multi_cities,train_years)
    train_moving_avgs = moving_average(train_temps,window_length)
    
    model = generate_models(train_years,train_moving_avgs,degs)
    evaluate_models_on_testing(test_years,test_moving_avgs,model)

#moving_temp_avg_test(thisclimate,CITIES,TESTING_INTERVAL,TRAINING_INTERVAL,
#                     5,[1,2,20])

def moving_temp_stdev_train(climate,multi_cities,interval,window_length,degs):
    years = pylab.array(interval)
    stdevs = gen_std_devs(climate,multi_cities,years)
    stdevs_moving_avgs = moving_average(stdevs,window_length)
    model = generate_models(years,stdevs_moving_avgs,degs)
    evaluate_models_on_training(years,stdevs_moving_avgs,model)  

#moving_temp_stdev_train(thisclimate,CITIES,TRAINING_INTERVAL,5,[1])
