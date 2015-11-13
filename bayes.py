import sys
import fileinput
import itertools
import collections
import os

number_of_diseases=''
number_of_patients=''
diseases = []
symptoms = {}
dict_prob_disease = {}
dict_symptom_disease = {}
dict_symptom_not_disease = {}
dict_not_symptom_disease = {}
dict_not_symptom_not_disease = {}
dict_bayes_result = {}
dict_bayes_min_max_result = {}
dict_bayes_inc_dec_result = {}
#dict_symptom_disease {'celiac': [0.78, 0.72, 0.65, 0.68, 0.26, 0.69], 'alzheimer': [0.95, 0.45, 0.44, 0.39], 'ALS': [0.42, 0.67, 0.76, 0.81, 0.23], 'parkinson': [0.31, 0.88, 0.74, 0.23, 0.29], 'leukemia': [0.88, 0.52, 0.38, 0.49, 0.65, 0.55, 0.38, 0.66]}
#dict_symptom_not_disease {'celiac': [0.29, 0.22, 0.45, 0.32, 0.78, 0.32], 'alzheimer': [0.12, 0.81, 0.13, 0.08], 'ALS': [0.26, 0.42, 0.34, 0.09, 0.83], 'parkinson': [0.76, 0.08, 0.32, 0.65, 0.74], 'leukemia': [0.15, 0.34, 0.22, 0.34, 0.14, 0.11, 0.21, 0.32]}
#dict_not_symptom_disease {'celiac': [0.21999999999999997, 0.28, 0.35, 0.31999999999999995, 0.74, 0.31000000000000005], 'alzheimer': [0.050000000000000044, 0.55, 0.56, 0.61], 'ALS': [0.5800000000000001, 0.32999999999999996, 0.24, 0.18999999999999995, 0.77], 'parkinson': [0.69, 0.12, 0.26, 0.77, 0.71], 'leukemia': [0.12, 0.48, 0.62, 0.51, 0.35, 0.44999999999999996, 0.62, 0.33999999999999997]}
#dict_not_symptom_not_disease {'celiac': [0.71, 0.78, 0.55, 0.6799999999999999, 0.21999999999999997, 0.6799999999999999], 'alzheimer': [0.88, 0.18999999999999995, 0.87, 0.92], 'ALS': [0.74, 0.5800000000000001, 0.6599999999999999, 0.91, 0.17000000000000004], 'parkinson': [0.24, 0.92, 0.6799999999999999, 0.35, 0.26], 'leukemia': [0.85, 0.6599999999999999, 0.78, 0.6599999999999999, 0.86, 0.89, 0.79, 0.6799999999999999]}

def bayes_algo(patient_id,line_of_patient):
	global dict_prob_disease,dict_symptom_disease,dict_symptom_not_disease,dict_not_symptom_disease,dict_not_symptom_not_disease,number_of_diseases,number_of_patients,diseases
	dict_patient_diseases = {}
	for k in range(0,int(number_of_diseases)):
		disease_name = diseases[k]
		#['T', 'U', 'F', 'U', 'T']
		numerator = dict_prob_disease[disease_name]
		denominator = 1-float(dict_prob_disease[disease_name])
		result_list = eval((input[int(line_of_patient)+k]))
		for j in range(0,len(result_list)):
			if(result_list[j] == 'T'):
				symptom_list = dict_symptom_disease[disease_name]
				symptom_list_not_disease = dict_symptom_not_disease[disease_name]
				numerator = float(numerator)*symptom_list[j]
				denominator = float(denominator)*symptom_list_not_disease[j]
			if(result_list[j] == 'F'):
				symptom_list = dict_not_symptom_disease[disease_name]
				symptom_list_not_disease = dict_not_symptom_not_disease[disease_name]
				numerator = float(numerator)*symptom_list[j]
				denominator = float(denominator)*symptom_list_not_disease[j]

		denominator = denominator+numerator
		final_value = float('inf') if denominator==0 else '{0:.4f}'.format(round(numerator/denominator,4))
		dict_patient_diseases[disease_name] = str(final_value)
	dict_bayes_result[patient_id]=dict_patient_diseases

#
def bayes_algo_max_min(patient_id,line_of_patient):
	global dict_prob_disease,dict_symptom_disease,dict_symptom_not_disease,dict_not_symptom_disease,dict_not_symptom_not_disease,number_of_diseases,number_of_patients,diseases

	dict_patient_diseases = {}
	unknown_substitutions = []
	disease_list = {}
	for k in range(0,int(number_of_diseases)):
		disease_name = diseases[k]
	
		#['T', 'U', 'F', 'U', 'T']
		
		result_list = eval((input[int(line_of_patient)+k]))
		count = 0
		for item in result_list:
			if(item=='U'):
				count=count+1
		true_false = ['T','F']
		truth_permutations = list(itertools.product(true_false,repeat=count))
		new_result_list = list(result_list)
		unknown_substitutions = []
		# Case where there are no UNKNOWNS
		if(count < 1):
			patient_result = dict_bayes_result[patient_id]
			prob_disease = patient_result[disease_name]
			###### ADDED CODE FOR STORING FLOAT VALUES INSTEAD OF STR - DATED 7TH MAY 2015########
			unknown_substitutions = [float(prob_disease),float(prob_disease)]
		for j in range(0,len(truth_permutations)):
			new_result_list = list(result_list)
			item = truth_permutations[j]
			k=0
			for i in range(0,len(new_result_list)):
				if(new_result_list[i]=='U'):
					loc = new_result_list.index('U')
					new_result_list[loc]= item[k]
					k = int(k)+1
			numerator = dict_prob_disease[disease_name]
			denominator = 1-float(dict_prob_disease[disease_name])
			for j in range(0,len(new_result_list)):
				if(new_result_list[j] == 'T'):
					symptom_list = dict_symptom_disease[disease_name]
					symptom_list_not_disease = dict_symptom_not_disease[disease_name]
					numerator = float(numerator)*symptom_list[j]
					denominator = float(denominator)*symptom_list_not_disease[j]
				if(new_result_list[j] == 'F'):
					symptom_list = dict_not_symptom_disease[disease_name]
					symptom_list_not_disease = dict_not_symptom_not_disease[disease_name]
					numerator = float(numerator)*symptom_list[j]
					denominator = float(denominator)*symptom_list_not_disease[j]

			denominator = denominator+numerator
			final_value = float('inf') if denominator==0 else round(numerator/denominator,4)

			
			unknown_substitutions.append(final_value)
		unknown_substitution = [str('{0:.4f}'.format(min(unknown_substitutions))),str('{0:.4f}'.format(max(unknown_substitutions)))]
		disease_list[disease_name]=unknown_substitution
	dict_bayes_min_max_result[patient_id]=disease_list


def bayes_algo_inc_dec(patient_id,line_of_patient):
	global symptoms,dict_prob_disease,dict_symptom_disease,dict_symptom_not_disease,dict_not_symptom_disease,dict_not_symptom_not_disease,number_of_diseases,number_of_patients,diseases,dict_bayes_inc_dec_result
	diseases_list_incdec = {}
	dict_patient_diseases = {}
	unknown_substitutions = []
	
	disease_list = {}
	for m in range(0,int(number_of_diseases)):
		disease_name = diseases[m]
		symptom = symptoms[disease_name]
		final_result = {}
		new_final_list = {}
	
		#['T', 'U', 'F', 'U', 'T']
		prob_disease_patient = dict_bayes_result[patient_id]
		prob_disease = float(prob_disease_patient[disease_name])
		result_list = eval((input[int(line_of_patient)+m]))
		count = 0
		for item in result_list:
			if(item=='U'):
				count=count+1
		true_false = ['T','F']
		new_result_list = list(result_list)
		unknown_substitutions = []
		
		for j in range(0,len(true_false)):
			new_result_list = list(result_list)
			item = true_false[j]
			
			for i in range(0,len(new_result_list)):
				
				
				
				if(new_result_list[i]=='U'):
					current_symptom = symptom[i]
					
					new_result_list[i]= item
					
					numerator = dict_prob_disease[disease_name]
					denominator = 1-float(dict_prob_disease[disease_name])
					for k in range(0,len(new_result_list)):
						if(new_result_list[k] == 'T'):
							symptom_list = dict_symptom_disease[disease_name]
							symptom_list_not_disease = dict_symptom_not_disease[disease_name]
							numerator = float(numerator)*symptom_list[k]
							denominator = float(denominator)*symptom_list_not_disease[k]
						if(new_result_list[k] == 'F'):
							symptom_list = dict_not_symptom_disease[disease_name]
							symptom_list_not_disease = dict_not_symptom_not_disease[disease_name]
							numerator = float(numerator)*symptom_list[k]
							denominator = float(denominator)*symptom_list_not_disease[k]

					denominator = denominator+numerator
					final_value = float('inf') if denominator==0 else round(numerator/denominator,4)
					key = current_symptom+","+item
					final_result[key] = final_value
					new_result_list[i]= 'U'
			
		# keylist = final_result.keys()
		# keylist.sort()
		#print keylist
		# for key in keylist:
		###### ADDED CODE FOR CHECKING IF LIST IS EMPTY - DATED 7TH MAY 2015  ########
		if len(final_result) > 0 :
		##### END OF CHANGED CODE #######
			new_final_list=  collections.OrderedDict(sorted(final_result.items(), key=lambda t: t[0]))
        	#print new_final_list   
			maximum = max(data for data in new_final_list.values())
			for key, value in new_final_list.items():
		   		if value == maximum:
		   			max_key =key
			minimum = min(data for data in new_final_list.values())
			for key, value in new_final_list.items():
		   		if value == minimum:
		   			min_key =key
			
			#Check for case when the newly calculated probabilities don't increase/decrease the original probability
			if(maximum <= prob_disease ):
				max_key = "none,N"
			if(minimum >= prob_disease):
				min_key = "none,N"
			unknown_substitutions = [max_key.split(',')[0],max_key.split(',')[1],min_key.split(',')[0],min_key.split(',')[1]]
		# Case where there are no UNKNOWNS
		if(count < 1):
			unknown_substitutions = ['none','N','none','N']
		
		disease_list[disease_name]=unknown_substitutions
	dict_bayes_inc_dec_result[patient_id]=disease_list




		






filename = sys.argv[2]

#Reading the file
with open(filename) as f:
    input = f.read().splitlines()
base = os.path.basename(filename)
outputfilename = base.split('.')[0]+"_inference."+base.split('.')[1]
outputfile = open(outputfilename, 'w+')
number_of_diseases = input[0].split(' ')[0]
number_of_patients = input[0].split(' ')[1]
for i in range(1,(int(number_of_diseases)*4),4):
	disease_name = input[i].split(' ')[0]
	diseases.append(disease_name)
	number_of_symptoms = input[i].split(' ')[1]
	prob_disease = input[i].split(' ')[2]
	dict_prob_disease[disease_name] = prob_disease
	symptoms[disease_name]=  eval(input[i+1])
	prob_symptom_disease = eval(input[i+2])
	prob_symptom_not_disease = eval(input[i+3])
	prob_not_symptom_disease = [1-x for x in prob_symptom_disease]
	prob_not_symptom_not_disease = [1-x for x in prob_symptom_not_disease]
	dict_symptom_disease[disease_name] = prob_symptom_disease
	dict_symptom_not_disease[disease_name] = prob_symptom_not_disease
	dict_not_symptom_disease[disease_name] = prob_not_symptom_disease
	dict_not_symptom_not_disease[disease_name] = prob_not_symptom_not_disease


for i in range(0, int(number_of_patients)):
	line_of_patient = (int(number_of_diseases)*4)+(i*int(number_of_diseases))+1
	patient_id = "Patient-"+str(i+1)
	bayes_algo(patient_id,line_of_patient)
	bayes_algo_max_min(patient_id,line_of_patient)
	bayes_algo_inc_dec(patient_id,line_of_patient)
for i in range(0,len(dict_bayes_result)):
 	patient_id = "Patient-"+str(i+1)

 	
 	outputfile.write(patient_id +":\n")
 	outputfile.write(str(dict_bayes_result[patient_id])+"\n")
 	outputfile.write(str(dict_bayes_min_max_result[patient_id])+"\n")
 	outputfile.write(str(dict_bayes_inc_dec_result[patient_id])+"\n")

# {'celiac': 0.1245, 'alzheimer': 0.4263, 'ALS': 0.4546, 'parkinson': 0.0091, 'leukemia': 0.4573}
# {'celiac': 0.5942, 'alzheimer': 0.0728, 'ALS': 0.0326, 'parkinson': 0.4855, 'leukemia': 0.6036}
# {'celiac': 0.2169, 'alzheimer': 0.0405, 'ALS': 0.0863, 'parkinson': 0.5863, 'leukemia': 0.1481}
# {'celiac': 0.299, 'alzheimer': 0.1238, 'ALS': 0.2219, 'parkinson': 0.0082, 'leukemia': 0.8164}
# {'celiac': 0.3033, 'alzheimer': 0.3885, 'ALS': 0.0559, 'parkinson': 0.2474, 'leukemia': 0.483}
# {'celiac': 0.4919, 'alzheimer': 0.4079, 'ALS': 0.3673, 'parkinson': 0.1262, 'leukemia': 0.4899}
# {'celiac': 0.0319, 'alzheimer': 0.845, 'ALS': 0.4594, 'parkinson': 0.0076, 'leukemia': 0.1263}
# {'celiac': 0.2222, 'alzheimer': 0.4079, 'ALS': 0.2062, 'parkinson': 0.5398, 'leukemia': 0.4538}
# {'celiac': 0.4431, 'alzheimer': 0.4079, 'ALS': 0.0543, 'parkinson': 0.0029, 'leukemia': 0.0623}
# {'celiac': 0.3033, 'alzheimer': 0.5169, 'ALS': 0.025, 'parkinson': 0.3859, 'leukemia': 0.0956}