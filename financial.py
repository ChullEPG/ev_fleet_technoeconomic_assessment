import numpy as np
import matplotlib.pyplot as plt

def get_cost_of_charging(load_profile: np.ndarray, time_of_use_tariffs: dict, time_periods: dict):
    
    # Obtain energy costs for each time period of the day
    peak_cost = time_of_use_tariffs['peak']
    standard_cost = time_of_use_tariffs['standard']
    off_peak_cost = time_of_use_tariffs['off-peak']
    
    # Obtain time periods for each time period of the day
    peak_times = time_periods['peak_times']
    standard_times = time_periods['standard_times']
    off_peak_times = time_periods['off_peak_times']
    
    # Initialize total cost variables
    total_cost = np.zeros(len(load_profile))
    
    # Calculate total cost of energy consumption with time of use tariffs 

    for i in range(len(total_cost)):
        curr_hour_of_day = i % 24
        curr_hour_of_week = i % 168
        
        
        # Morning
        if curr_hour_of_week > 120:
            total_cost[i] = load_profile[i] * off_peak_cost
        elif curr_hour_of_day in peak_times:
            total_cost[i] = load_profile[i] * peak_cost
        # Afternoon 
        elif curr_hour_of_day in standard_times:         
            total_cost[i] = load_profile[i] * standard_cost
        # Evening 
        else:        
            total_cost[i] = load_profile[i] * off_peak_cost     
 
                      
    return sum(total_cost)
