import argparse 
import pandas as pd 

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', dest='abfile',
		help='TALON abundance file to reformat')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

def main():
	args = get_args()

	df = pd.read_csv(args.abfile, sep='\t')
	cols = []
	cols.append(df.columns[1])
	cols.extend(df.columns[11:-1].tolist())
	cols.append(df.columns[-1])

	df = df[cols]
	df.rename({'transcript_ID': 'ID'}, axis=1, inplace=True)

	oname = args.oprefix+'_lrgasp.tsv'
	df.to_csv(oname, sep='\t', index=False)

if __name__ == '__main__':
	main()