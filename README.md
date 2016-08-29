# Annow

Annow version 1.0 Usage Manual

This software is intended to create NCBI BLAST nucleotide databases from Local and Remote Sources for local querying.
This software can be used to update FASTA files with new annotations, extract alignment metrics, and view alignments. 
USAGE:

Run Name - Used for file and directory naming (i.e FASTA files, results).  Spaces will be replaced by '_'. 
Additionally, the current Month, Day, Hour, and Minute will be added to your run name to further distinguish experiments.		   
example usage: "all_plamids_2013"


Run Directory - Select a local root directory to deposit results. A new directory containing your run name and date will
be created within and output will be directed here. 

prompted usage example: C:\Users\name\Desktop


FTP Site - If using a remote site enter the ftp url.

example usage: ftp.ncbi.nlm.nih.gov


FTP Directory - If using a remote site, enter the directory which the files you wish to download are located.

example usage: /refseq/H_sapiens/RefSeqGene/


FTP Suffix - If using a remote site a file suffix is required. The extension of this file should .gz and all 
files ending in the provided suffix will be downloaded, be specific. 

example usage for a single file: refseqgene1.genomic.fna.gz
example usage for multiple files: .genomic.fna.gz
example usage for all files: .gz


Local FASTA (subject) - You may use a local .FASTA rather than remote. The file must be conventionally formatted
to build correctly and will serve as your BLAST database (subject).		  

prompted usage example: C:\Users\name\Desktop\mysubject.fasta 

  
Local FASTA (query ) - A fasta file that you would like to compare is required and must be conventionally formatted.

prompted usage example: C:\Users\name\Desktop\myquery.fasta 


E-Value - This describes the number of hits one can expect to see by chance. Any decimal value can be entered, 
the higher values increase runtime.

default value = 0.001
usage: 0.0002


% Match - This must be a % value and will be used in conjunction with the following Update FASTA parameter. 
Any values BELOW this threshold will have annotation updated.  

default value = 99.00
usage : 75.00

		  
Hits - This must be an whole number and will determine how many results to return while running BLAST. 
A greater number of hits requested increases run time. 	 

default value = 1
usage = 2


Update FASTA - When this box is checked a FASTA file containing only updated sequences will be generated 
in the results directory. They will be annotated by > OLD ANNOTATION | NEW ANNOTATION 

default = unchecked


Alignments - This process will run blast again, this time generating a text file withlocal sequence alignments. 
Selecting this will increase run by 2 fold.  

default = unchecked



RUNNING Annow:

When all parameters are entered correctly press RUN to begin. This process is done concurrently 
and the UI may become unresponsive during data processing. However any errors will be reported in screen, 
and absent of this you may assume the process is ongoing. Depending on usage operations may take several hours or longer. 
	

Version 1.0 is a stable release and new version can be found at https://github.com/ashbig/Annow/

Copyright (C) <2016>  <Ashkan Bigdeli>

<ashbigdeli@gmail.com>


This program is free software: you can redistribute it and/or modify it under the terms of the GNU General 
Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
See <http://www.gnu.org/licenses/>
