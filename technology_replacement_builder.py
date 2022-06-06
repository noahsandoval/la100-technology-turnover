def technology_replacement_builder():
	# Import statements
	import pandas as pd
	from itertools import repeat

	# Choose housing characteristic from buildstock to use
	technology_choice = input("Input housing characteristic (tab in LA100 Technologies file) you wish use:")
	
	# Create first sheet
	tech_choice = [technology_choice]
	tsv_df = pd.DataFrame(data=tech_choice, columns = ['technology'])
	filename = technology_choice+'.xlsx'
	filename = filename.replace(" ", "_")
	
	technology_df = pd.read_excel('LA100 Technologies.xlsx', sheet_name = technology_choice, index_col=0)
	print(technology_df)
	
	option = technology_df[technology_choice]
	print(option)

	#option = []
	#for col in technology_df.columns:
	#	option.append(col)

	

	technology_trans_df = technology_df.transpose()
	

	goal_percent = technology_trans_df.iloc[:,1]
	#print(goal_percent)

	#goal = option_df["goal_percent"] = technology_trans_df.iloc[:, 2]
	#print(goal)
	
	

	# Create replacement dataframe
	#replacement_df = pd.DataFrame(data = options, columns = ['replacement'])
	
	# Create replacement matrix
	# size = len(options)
	# for option in options:
	# 	data = []
	# 	data.extend(repeat(0,size))
	# 	new_column = pd.DataFrame(data = data, columns=[options])
	# 	replacement_df[option] = new_column

	assumptions = ['#']
	assumptions_df = pd.DataFrame(data=assumptions, columns=["Assumptions:"])

	# Create output excel file
	with pd.ExcelWriter(filename) as writer:
		tsv_df.to_excel(writer, sheet_name = 'tsv', index=False)
		#option_df.to_excel(writer, sheet_name = 'option', index=False)
		#replacement_df.to_excel(writer, sheet_name = 'replacement', index=False)
		assumptions_df.to_excel(writer, sheet_name = 'assumptions', index=False)


technology_replacement_builder()
