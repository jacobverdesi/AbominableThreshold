import pandas as pd
import sys
"""
File:HW02_Verdesi_Jacob_Trainer.py
Author: Jacob Verdesi
Email:jxv3386@rit.edu
Description:This is a Trained program for Classifying Abominable Data
"""
def printClassified(data,bestAttribute,bestThreshold):
	"""
	given the best attribute of the data and best threshold
	print out -1 being Class A and 1 Class B
	:param data: pandas dataFrame
	:param bestAttribute: Name of attribute
	:param bestThreshold: threshold of attribute
	"""
	for i in data[bestAttribute]:
		if (bestAttribute=="Height" and i>bestThreshold) or (bestAttribute=="Age" and i<bestThreshold):
			print(-1)
			
		else:
			print(1)
			
		
	
def main():
	"""
	Main function
	"""
	fileName=sys.argv[1]
	data=(pd.read_csv(fileName,sep=','))
	printClassified(data,"Height",135)
	
if __name__ == '__main__':
	main()
