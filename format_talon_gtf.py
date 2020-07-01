import argparse 
def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-gtf', dest='gtffile',
		help='TALON gtf file to reformat')
	parser.add_argument('-o', dest='oprefix',
		help='output file prefix')
	args = parser.parse_args()
	return args

# creates a dictionary of the last field of a gtf
# adapted from Dana Wyman
def get_fields(fields):

    attributes = {}

    description = fields.strip()
    description = [x.strip() for x in description.split(";")]
    for pair in description:
        if pair == "": continue

        pair = pair.replace('"', '')
        key, val = pair.split()
        attributes[key] = val

    # put in placeholders for important attributes (such as gene_id) if they
    # are absent
    if 'gene_id' not in attributes:
        attributes['gene_id'] = 'NULL'

    return attributes  

def format_field_dict_for_gtf(d):
	fields = ''
	for k, v in d.items():
		fields += '{} "{}"; '.format(k, v)
	return fields

def main():
	args = get_args()
	oname = args.oprefix+'_lrgasp.gtf'
	ofile = open(oname, 'w')

	with open(args.gtffile, 'r') as infile:
		for line in infile: 
			line = line.strip().split('\t')
			if line[2] == 'exon':
				fields = get_fields(line[-1])
				new_fields = dict()

				# add reference transcript ID if the transcript
				# is known
				if fields['transcript_status'] == 'KNOWN':
					new_fields['reference_transcript_id'] = fields['transcript_id']

				# add reference gene ID if the gene is known
				if fields['gene_status'] == 'KNOWN':
					new_fields['reference_gene_id'] = fields['gene_id']

				# add talon gene and transcript ids
				new_fields['transcript_id'] = fields['talon_transcript']
				new_fields['gene_id'] = fields['talon_gene']

				new_fields = format_field_dict_for_gtf(new_fields)
				line[-1] = new_fields
				line = '\t'.join(line)+'\n'
				ofile.write(line)
	ofile.close()

if __name__ == '__main__':
	main()
