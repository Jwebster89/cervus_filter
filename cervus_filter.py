#!/usr/bin/env python

import os
import sys
import csv
import argparse
import itertools

class Cervus_filter():
	def __init__(self, infile, genotypes):
		self.infile = infile
		self.genotypes = genotypes
		#self.outfile = outfile if os.path.splitext(outfile)[1] == '.csv' else (outfile + '.csv')
	
	
	def parentage_hits(self):
		ParentPairs=[]
		with open(self.infile) as cervus_input:
			csv_reader=csv.reader(cervus_input,delimiter=',')
			next(csv_reader)
			for row in csv_reader:
				loci=int(row[5])
				lod=float(row[6])
				loci2=int(row[12])
				lod2=float(row[13])
				if loci < 4 and lod > 0 :
					pair=[row[0],row[2]]
					ParentPairs.append(pair)
				if loci2 < 4 and lod2 > 0 :
					pair2=[row[0],row[9]]
					ParentPairs.append(pair2)
		uniq_pairs=list(ParentPairs for ParentPairs,_ in itertools.groupby(ParentPairs))
		for pair in uniq_pairs:
			print("Animals " + pair[0] + " and " + pair[1] + " have a positive LOD score and 3 or less mismatches")
		print('\n\n')
		ParentPairs.sort()
		return(list(ParentPairs for ParentPairs,_ in itertools.groupby(ParentPairs))) # Returns a list of lists of parent/progeny with duplicates removed

	# def print_pairs(self,parentage):
		# for pairing in parentage:
			# pair=[]
			# for animal in pairing:
				# pair.append(animal)
			# print("

	def find_mismatches(self,parentage):
		with open(self.genotypes) as csv_input:
			csv_reader=csv.reader(csv_input,delimiter=',')
			target_IDs=next(csv_reader)
			for pair in parentage: ### This block, for each animal ID from a parent/progeny pair, will parse through "cervus parse" output and extract the row of all traits from the animal ID.
				sample_pair=[]
				sample_names=[]
				for ID in pair:
					csv_input.seek(0)
					next(csv_reader)
					for row in csv_reader:
						if row[0]==ID:
							sample_pair.append(row[1:])
							sample_names.append(row[0])
				
				target_pairs=[] ### This block takes the rows extracted above and ..
				for traits in sample_pair:
					targets=[]
					for item in range(0, len(traits)):  ### Turns the values from the spreadsheet into integers
						traits[item] = int(traits[item]) 
					for i in range(0,len(traits),2): ### Then sums the values of the 1st and 2nd, 3rd and 4th, 5th and 6th etc entries (homozygous/heterozygous, wild type/mutant)
						target=sum(traits[i:i+2])
						targets.append(target)
					target_pairs.append(targets) ### Creates a list of summed values, in a list of the paired animals
				tuples=zip(*target_pairs) ### Creates a tuple of summed values from targets. E.g. Animal_A 1,2 and Animal_B 2,2 becomes Animal_A 3 and Animal_B 4.
				column=0
				mismatch_count=0
				for n in tuples: ### This goes through the tuples
					column+=2
					if n[0] == 2 and n[1] == 4 or n[0] == 4 and n[1] == 2:
						mismatch_count+=1
						print("Mismatch in target " + target_IDs[column] + " for samples " + sample_names[0] + " and " + sample_names[1])
				if mismatch_count==0:
					print("There were no mismatches in samples " + sample_names[0] + " and " + sample_names[1])



	def run(self):
		# self.parentage_hits()
		self.find_mismatches(self.parentage_hits())

def main():
	parser = argparse.ArgumentParser(description="Cervus_filter", formatter_class=argparse.RawTextHelpFormatter, add_help=False)
	optional = parser.add_argument_group('Optional Arguments')
	required = parser.add_argument_group('Required Arguments')

	required.add_argument('-c', '--csv', type=str, required=True, help="Output of Cervus in csv format")
	required.add_argument('-g', '--genotype', type=str, required=True, help="Output of Ion Torrent in csv format")
	optional.add_argument("-h", "--help", action="help", help="show this help message and exit")
	
	args=parser.parse_args()
	csv_input=args.csv
	genotype_input=args.genotype
	
	job=Cervus_filter(csv_input, genotype_input)
	job.run()



if __name__ == '__main__':
	main()
