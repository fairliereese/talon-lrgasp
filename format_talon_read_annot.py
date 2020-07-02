import argparse 
import pandas as pd 

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='annotfile',
		help='TALON read annot file to reformat')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	parser.add_argument('-samples', dest='samples',
		default=None,
		help='comma-separated list of sample names to include. '
		'If not provided, includes all samples.')
	args = parser.parse_args()
	return args

def main():
	args = get_args()

	if args.samples:
		sample_names = args.samples.split(',')
		print(sample_names)

	df = pd.read_csv(args.annotfile, sep='\t', usecols=[0,1,10])
	df.rename({'read_name':'read_id','transcript_ID':'transcript_id'},
		axis=1, 
		inplace=True)

	if args.samples:
		df = df.loc[df.dataset.isin(sample_names)]

	df.drop('dataset', axis=1, inplace=True)

	ofile = args.oprefix+'_lrgasp_read_annot.tsv'
	df.to_csv(ofile, sep='\t', index=False)

if __name__ == '__main__':
	main()