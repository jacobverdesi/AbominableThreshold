import pandas as pd
"""
	File:HW02_Verdesi_Jacob_Trainer.py
	Author: Jacob Verdesi
	Email:jxv3386@rit.edu
	Description:This is a Trained program for Classifying Abominable Data
"""
def printClassified(data,bestAttribute,bestThreshold):
	for i in data[bestAttribute]:
		if (bestAttribute=="Height" and i>bestThreshold) or (bestAttribute=="Age" and i<bestThreshold):
			print(-1)
			
		else:
			print(1)
			
		
	
def main():
	"""
		Main function
	"""
	fileName="the_validation_file.csv"
	data=(pd.read_csv(fileName,sep=','))
	printClassified(data,"Height",135)
	
if __name__ == '__main__':
	main()
