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



def simulate_charging_load_profile(total_days, total_time,
                             time_resolution,
                             num_vehicles,
                             charging_power,
                             data_input_load_profile = None,
                             plot = True):
    '''
    This function simulates a charging load profile for a fleet of EVs at a charging station, given the number of EVs, the charging power, the total simulation time, and the desired time resolution
    
    '''
    if data_input_load_profile is not None:
        return data_input_load_profile
    
    # Generate random charging start times and durations for each EV
    np.random.seed(42)  # Set a seed for reproducibility
    start_times = np.random.uniform(low=0, high=total_time, size=(num_vehicles, total_days))
    durations = np.random.uniform(low=1, high=4, size=(num_vehicles, total_days))

    # Create the time axis
    time = np.arange(0, total_time, time_resolution)

    # Initialize the load profile
    load_profile = np.zeros_like(time)
    
    # conver load_profile to floats
    load_profile = load_profile.astype(float)

    # Calculate the EV load profile for each day
    for i in range(num_vehicles):
        for day in range(total_days):
            start_time = start_times[i, day]
            duration = durations[i, day]
            end_time = start_time + duration

            # Calculate the charging load during the charging period
            mask = (time >= start_time) & (time < end_time)
            load_profile[mask] += float(charging_power)
    if plot: 
        # Plot the EV load profile
        plt.plot(time, load_profile)
        plt.xlabel('Time (hours)')
        plt.ylabel('Power (kW)')
        plt.title('Electric Vehicle Load Profile')
        plt.grid(True)
        plt.show()
        
        
    
    
    return load_profile 


