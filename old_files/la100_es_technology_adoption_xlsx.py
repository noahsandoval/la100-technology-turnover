def technology_adoption():
    # Import statements
    import pandas as pd
    
    
    # Read in buildstock file
    buildstock = pd.read_csv('buildstock.csv')
    
    # Input file to be 
    technology_file = input("Input technology adoption file name:")
    
    # Read in the different sheets from the technology adoption file which just has the name of the .tsv technology that we are adjusting
    technology_df = pd.read_excel(technology_file, sheet_name=0) # tsv name
    saturation_2035 = pd.read_excel(technology_file, sheet_name=1) # Technology saturations for 2035
    replacement_2035 = pd.read_excel(technology_file, sheet_name=2) # Distribution matrix
    
    # Create a new buildstock dataframe which will serve as the basis for the new_buildstock.csv file
    new_buildstock = pd.DataFrame()
    
    # Create the variable technology, which is a string which will be used to access the correct housing characteristics column in buildstock.csv
    technology_df = technology_df.astype({'technology':'string'})
    technology = technology_df.iat[0,0]
    
    # Determine the original technology saturations from the buildstock.csv
    original_percent = []
    for option in saturation_2035.iloc[:,0]:
        partial_df = buildstock.loc[buildstock[technology] == option]
        partial_df_size = partial_df.shape[0]/buildstock.shape[0]
        original_percent.append(partial_df_size)
    
    # Use new percent to determine the number of houses which will get a replacement
    total = buildstock.shape[0]
    for option, percent in zip(saturation_2035["option"], saturation_2035["goal percent"]):
        original = buildstock.loc[buildstock[technology] == option]
        original_size = original.shape[0]
        if original_size == 0: 
            continue 
            
        # Use new percent to determine the number of houses which will get a replacement
        goal = total*percent
        if goal >= original_size:
            keep = original_size
            keep = int(keep)
            replace = 0 
            replace = int(replace)
        else: 
            keep = goal
            keep = int(keep)
            replace = original_size-keep
            replace = int(replace)
        
        # New technology distribution
        new_option = []
        # The number of households which do not change
        new_option.extend(repeat(option, keep))
        # The number of the households which get a replacement, using the distribution matrix
        for replacement, dist in zip(replacement_2035['replacement'], replacement_2035[option]):
            new_tech = dist*replace
            new_tech = int(new_tech)
            new_option.extend(repeat(replacement, new_tech))
        
        # Ensure the new option size matches the size of the original dataframe
        diff = original_size - len(new_option)
        if diff < 0: 
            del new_option[diff:]
        elif diff > 0:
            new_option.extend(repeat(replacement_2035['replacement'][:-1], diff))
    
        # To check that code above added/removed the necessary number of entries
        new_diff = original_size - len(new_option)
        #print(new_diff)
        
        # Remove final datapoint with information about the dataframe
        new_option[-1] = option
        
        
        # Delete original existing technology column and add in the new column
        del original[technology]
        original[technology] = new_option
        new_buildstock = new_buildstock.append(original)
    
    # Test -> Can be removed if necessary
    # Create new technology_adoption dataframe 
    new_technology_test = pd.DataFrame()
    new_technology_test["options"] = saturation_2035.iloc[:,0] # Add options to test dataframe
    new_technology_test["original percent"] = original_percent  # Add original percent to test dataframe
    new_technology_test["goal percent"] = saturation_2035.iloc[:,1] # Add goal percent to test dataframe
    
    # Determine the new percent of each option
    new_percent = []
    for option in saturation_2035.iloc[:,0]:
        count = 0 
        for row in new_buildstock[technology]:
            if str(row) == str(option):
                count +=1
        percentage = count/total
        new_percent.append(percentage)
        

    new_technology_test["new percent"] = new_percent # Add new percent to test dataframe
    new_technology_test.to_csv("new_technology_test.csv")
    
    # Resort buildstock by building number
    new_buildstock = new_buildstock.sort_values(by="Building", axis=0, ascending=True)
    
    new_buildstock.to_csv("new_buildstock.csv") 
     
technology_adoption()
