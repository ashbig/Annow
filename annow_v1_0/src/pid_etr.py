# Created By Ashkan Bigdeli 2016
# pid_etr.py
#
# A repository housing all required methods for updating sequences id's
# with new reference annotations 

import os, gzip, glob, traceback
from ftplib import FTP


#set internal blast paths
script_dir =os.path.dirname(__file__)
blastn = os.path.join(script_dir, "blastn")
makeblastdb = os.path.join(script_dir, "makeblastdb")


# download
#
# @param1 = file_id: suffix of files ot be downloaded.
# @param2 = ftp_url: ftp from which to download
# @param3 = ftp_dir: directory from ftp to download
# @param4 = run_name: for naming scheme
# @param5 = run_dir: the directory to download to 
#
# return = a message that the operation is complete
#
# Will download all specified files to a designated folder.
def download(file_id,ftp_url, ftp_dir, run_name, run_dir):
    
    try:
        ftp = FTP(ftp_url)
        ftp.login()    
        # Change directory in ftp to navigate to desired genome
        ftp.cwd(ftp_dir)
        filenames = ftp.nlst()
    
        for filename in filenames:
            if filename.endswith(file_id):
                local_filename = os.path.join(run_dir, filename)
                file = open(local_filename, 'wb')
                ftp.retrbinary('RETR ' + filename, file.write)
                file.close()
        return "Downloading Complete!"
    except:
        return "Download Failed! Check the error below.\n" + traceback.format_exc()


# unzip
#
# @param1 = the directory to find files for decompression
#
# return = a message that the operation is complete
#
# Method will unzip all compressed files in given directory
def unzip(run_dir):
    try:
        # for each file in the directory
        for gzip_path in glob.glob(run_dir + "/*"):
            if os.path.isdir(gzip_path) == False:
                in_file = gzip.open(gzip_path, 'rb')            
                temp = in_file.read()
                in_file.close()
                
                # get original filename and remove the extension
                gzip_filename = os.path.basename(gzip_path)            
                filename = gzip_filename[:-3]
                uncompressed_path = os.path.join(run_dir, filename)
                
                open(uncompressed_path, 'w').write(temp)
                os.chmod(uncompressed_path, 0775)
                return "Unzip Complete!"
    except:
        return "The downloaded files could not be decompressed! Check the error blow. \n" + traceback.format_exc()

# remove
#
# @param1 = suffix: file type to be removed.
# @param2 = download_to: folder to remove downloaded files.
#
# return = a message the operation is complete
#
# Removes all given file types from folder.
def remove(suffix, run_dir):
    try:
        files_in_path = run_dir + "/*" + suffix
        files = glob.glob(files_in_path)
        for f in files:
            os.remove(f)
        return "Intermmediate Files Removed!"
    except :
        return "We failed to remove intermmediate files! Check the error below.\n" + traceback.format_exc()
                         
# concat fasta
#
# @param1 = filenames: all files to be concatenated.
# @param2 = download_to: folder to concatenate files.
#
# return = a message the operation is complete
#
# Opens ALL files in folder and writes them to one .fasta file.
def concat_fasta(run_name, run_dir):
    # create file list of all files to concatenate
    files_in_path = run_dir + '/*'
    filenames = glob.glob(files_in_path)
    fasta_path = os.path.join(run_dir,(run_name + '.fasta'))
    try:
        with open(fasta_path, 'w') as outfile:
            for filename in filenames:
                with open(filename) as infile:
                    for line in infile:
                        outfile.write(line)
                        
                infile.close()
                os.remove(filename)        
        outfile.close()
        return ("Concatentation Complete! Intermediate Files Removed!", fasta_path)
    except:
        return ("FASTA files could not be concatenated! Check the error blow. \n" + traceback.format_exc(), "", "")
            
# create_db
#
# @param1 = run_dir:  the directory of operation
# @param2 = fasta: the file for database creation
# @param3 = run_name: for file naming the operation
#
# return = tuple = message, summary of database compilation, location of blast database
#
# Makes an external call to local blast program and creates desired blast database.
def create_db(run_dir, fasta, run_name):
    try:
        db_summary = os.path.join(run_dir, (run_name + '.db_summary.txt'))
        db_location = os.path.join(run_dir, run_name)
        os.popen(makeblastdb + ' -in ' + fasta + ' -dbtype nucl -out ' + db_location+ ' > ' + db_summary)
        files_tuple = ("The database has been created!", db_location, db_summary)
        return files_tuple
    except:
        return ("The Database could not be created! Check the error below. \n" + traceback.format_exec(), "", "")
    
# perform_blast
#
# @param1 = query_db: the fasta used for comparison
# @param2 = blast_db: the blast database
# @param3 = run_dir: the directory of operation
# @param4 = run_name: for file naming operation
# @param5 = evalue: the likely hood of randomness value
# @param6 = hits : the number of hits returned per sequence
# 
# return = tuple = an operation message, a tab delimited file of hits in the subject_db
#
# Performs NCBI local alignment blast and returns a bare tab delimited results file
def perform_blast(query_db, blast_db, run_dir, run_name, evalue, hits):
    try:
        results = os.path.join(run_dir, (run_name + '.blast.raw.txt')) 
        os.popen( blastn + ' -db ' + blast_db + ' -query ' + query_db + ' -out ' + results + 
              ' -max_target_seqs ' + hits + ' -evalue ' + evalue + ' -outfmt "6 qgi qacc qstart qend sseqid sstart send evalue pident nident mismatch gapopen"')
        return ("BLAST Results are ready!",results)
    except:
        return ("BLAST Failed to execute! Check the error below.\n" + traceback.format_exc(), "")
    
# perform_blast_align
#
# @param1 = query_db: the fasta used for comparison
# @param2 = blast_db: the blast database
# @param3 = run_dir: the directory of operation
# @param4 = run_name: for file naming operation
# @param5 = evalue: the likely hood of randomness value
# @param6 = hits : the number of hits returned per sequence
# 
# return = tuple = an operation message, a tab delimited file of hits in the subject_db
#
# Performs NCBI local alignment blast and returns a file containg alignments
def perform_blast_align(query_db, blast_db, run_dir, run_name, evalue, hits):
    results = os.path.join(run_dir, (run_name + '.alignments.txt')) 
    try:
        os.popen(blastn + ' -db ' + blast_db + ' -query ' + query_db + ' -out ' + results + 
                  ' -num_descriptions ' + hits + ' -num_alignments ' + hits + ' -evalue ' + evalue + ' -outfmt 0')
        return (("Your alignments are complete! " + results  + " Has been generated."), results)
    except:
        return ("BLAST Failed to execute. Check the below error!\n" + traceback.format_exc())
 


# summarize results
#
# @param1 = results: a file of tab delimited blast results
# @param2 = % criteria: for determining an imperfect match
# @param3 = the number: of hits returned. 
#
# return = tuple = a message of operation a summary file of the hits and their metrics, dictionary of updated id's
#
# This method takes in the results file from perform_blast and summarizes the results
def summarize_results(results, cut_off, hits):
    try:
        summary = results.replace('txt', 'blast.summary.tsv')
        new_id = {}
        count_below = 0
        count_above = 0
        avg_float = 1
        with open(results, 'r') as results_in:
            with open(summary, 'w+') as summary_out:
                summary_out.write('Input ID\tUpdated ID\tE-Value\t% Identity\t# Matches\t# Mismatches\t# Gaps\tReference Start\tReference End\n')
                for line in results_in:
                    line = line.strip('\n')
                    metrics = line.split('\t')
                    summary_out.write(metrics[1] + '\t' + metrics[4] + '\t' + metrics[7] + '\t' + metrics[8] + '\t' + metrics[9] + '\t' +
                                    metrics[10] + '\t' + metrics[11] + '\t' + metrics[5] + '\t' + metrics[6] + '\n')
                    if (float(cut_off) > float(metrics[8])):                
                        new_id[metrics[1]] = metrics[4]
                        count_below +=1
                    else:
                        count_above +=1
                    avg_float = avg_float + float(metrics[8])
        count_below = count_below/int(hits)
        avg_float = avg_float/(float(count_below) + float(count_above))
        message = ("Summerization Complete!\n" + str(count_below) + " Sequences require updates\n" + str(count_above) + " exceeded the % match cut off for updating.\n" + 
                   "Your query had a " + "{0:.2f}".format(avg_float) + " % identity to the subject\n" + "Your detailed summary is located in " + summary)
        if (len(new_id) <1):
            new_id = "There was 100 % Concordance. No Updates Required!"
        return (message, summary, new_id)
    except:
        return(("Your results could not be summerized! Check the error below.\n" + traceback.format_exc()), "", "")

# updated_fasta
#
# @param1 = run_dir: the directory of operation
# @param2 = run_name: for file naming operation
# @param3 = dictionary of updated annotations corresponding to the user id's
# @param4 = the user input FASTA file
#
# returns a fasta with updated annotations
def update_fasta(run_dir, run_name, new_id, query_db):
    try:
        new_fasta_name = run_name + '.updated.hits.only.fasta'
        new_fasta = os.path.join(run_dir, new_fasta_name)
        # This array records annotations that are not updated, it has no current use
        # but will be a necessary feature for future development (i.e global alignment)
        no_anno = []
        with open (query_db, 'r') as query_in:
            with open (new_fasta, 'w+') as fasta_out:
                updated = False           
                for line in query_in:
                    if line.startswith('>'):
                        def_line = line.strip('>')
                        def_line = def_line.strip('\n')
                        #if this sequence in the user input db has been updated, add new annotation, record this information in a dictionary
                        if new_id.has_key(def_line):
                            fasta_out.write('>' + def_line + '|' + new_id[def_line] + '\n')
                            updated = True
                            continue
                        #if no match is found, simply record it in a dictionary
                        else:
                            no_anno.append(def_line)
                            updated = False
                            #fasta_out.write(line)
                            #continue
                    if updated:
                        fasta_out.write(line)
        return (("A new FASTA file has been generated! It can be found in " + new_fasta + "\n"), new_fasta, no_anno)
    except:
        ("Your results could not be summerized! Check the error below.\n" + traceback.format_exc(), "", "")
