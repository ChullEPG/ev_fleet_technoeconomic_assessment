


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




def simulate_fixed_charging_load(start_time, end_time, battery_capacity, charger_rating, initial_soc):
    '''Simulate fixed charging profile (for Zimi fleets)'''
    
    # Initialize an empty daily profile for the charging load
    
    charging_profile = np.zeros(24)
    level_of_charge = initial_soc * battery_capacity #kWh

    if end_time > start_time: # for daytime charging
        for idx in range(start_time, end_time):
            if level_of_charge < battery_capacity:
                if (level_of_charge + charger_rating) > battery_capacity:
                    charging_profile[idx] = battery_capacity - level_of_charge # the difference between the two 
                    level_of_charge = battery_capacity #kWh
                else: 
                    level_of_charge += charger_rating # charges at rating
                    charging_profile[idx] = charger_rating 
            else:
                break 
    else: # for overnight charging 
        
        for idx in range(start_time, 24): # charge until end of day
            if level_of_charge < battery_capacity:
                if level_of_charge + charger_rating > battery_capacity:
                    level_of_charge = 100 #kWh
                    charging_profile[idx] = battery_capacity - level_of_charge # the difference between the two 
                else: 
                    level_of_charge += charger_rating # charges at rating
                    charging_profile[idx] = charger_rating 
            else: 
                break 
                    
        for idx in range(0, end_time): # charge starting from beginning of day
            if level_of_charge < battery_capacity:
                if level_of_charge + charger_rating > battery_capacity:
                    level_of_charge = 100 #kWh
                    charging_profile[idx] = battery_capacity - level_of_charge # the difference between the two 
                else: 
                    level_of_charge += charger_rating # charges at rating
                    charging_profile[idx] = charger_rating 
                    
            else: 
                break 
            
    return charging_profile 
    