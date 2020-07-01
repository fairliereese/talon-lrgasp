import argparse 
import pandas as pd 

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='annotfile',
		help='TALON read annot file to reformat')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

def main():
	args = get_args()

	df = pd.read_csv(args.annotfile, sep='\t', usecols=[0,10])
	df.rename({'read_name':'read_id','transcript_ID':'transcript_id'},
		axis=1, 
		inplace=True)

	ofile = args.oprefix+'_lrgasp_read_annot.tsv'
	df.to_csv(ofile, sep='\t', index=False)

if __name__ == '__main__':
	main()