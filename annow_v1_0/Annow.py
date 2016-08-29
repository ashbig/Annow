# Created by Ashkan Bigdeli 2016
# Annow.py
# Main UI and calls for data processing

# wx is external UI module
import wx, os
from src import pid_etr
from time import strftime
script_dir =os.path.dirname(__file__)


class ManualWindow(wx.Frame):
      #for manual page display
      def __init__(self):
           """Constructor"""
           wx.Frame.__init__(self, None, title="Annow User Manual", size=(720, 500))
           panel = wx.Panel(self)
           txt =wx.TextCtrl(panel, size=(700,450), style=wx.TE_MULTILINE | wx.TE_READONLY |wx.EXPAND)
           man = os.path.join(script_dir, "src/README.txt")
           with open(man) as readme:
             for line in readme:
                txt.AppendText(line)
           

class MainWindow(wx.Frame):
    
    def __init__(self,parent, title):
        wx.Frame.__init__(self,parent,title = title, size = (1300,650))        
        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('#ABABAB')

        #set up standard menu options
        filemenu= wx.Menu()
        menuManual= filemenu.Append(wx.NewId(), "Manual"," Usage Guide")
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        #creating and binding the menu
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Menu") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnManual, menuManual)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        #fonts
        entry_font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL)
        header_font = wx.Font(12,wx.MODERN, wx.NORMAL, wx.BOLD)
        
        
        #set up UI for all run information including event binding, sizing
        run_info = wx.StaticText(panel, label = "Enter Your Run Information")
        run_info.SetFont(header_font)
        
        #run name layout and bindings
        lblrun = wx.StaticText(panel, label = "Run Name: ", size=(175, -1))
        lblrun.SetFont(entry_font)
        self.editrun = wx.TextCtrl(panel, value="", size=(326, -1))
        ri_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ri_sizer.AddSpacer(10)
        ri_sizer.Add(lblrun)
        ri_sizer.Add(self.editrun)
        
        #run directory layout and bindings
        lblrun_dir = wx.StaticText(panel, label = "Run Directory: ", size=(175, -1))
        lblrun_dir.SetFont(entry_font)
        self.editrun_dir = wx.TextCtrl(panel, value = "", size=(326, -1))
        self.dir_button = wx.Button(panel, label="Directory")
        self.dir_button.Bind(wx.EVT_BUTTON, self.opendir)
        rd_sizer=wx.BoxSizer(wx.HORIZONTAL)
        rd_sizer.AddSpacer(10)
        rd_sizer.Add(lblrun_dir)
        rd_sizer.Add(self.editrun_dir)
        rd_sizer.AddSpacer(10)
        rd_sizer.Add(self.dir_button)
                
        #ftp layout and bindings
        ftp_info = wx.StaticText(panel, label = "Enter FTP Information")
        ftp_info.SetFont(header_font)
        
        self.ftp_site = wx.StaticText(panel, label = "FTP Site: ", size=(175, -1))
        self.ftp_site.SetFont(entry_font)
        self.edit_ftp = wx.TextCtrl(panel, value = "", size=(326, -1))
        ftp_sizer=wx.BoxSizer(wx.HORIZONTAL)
        ftp_sizer.AddSpacer(10)
        ftp_sizer.Add(self.ftp_site)
        ftp_sizer.Add(self.edit_ftp)
        
        ftp_dir = wx.StaticText(panel, label = "FTP Directory: ", size=(175, -1))
        ftp_dir.SetFont(entry_font)
        self.edit_ftp_dir = wx.TextCtrl(panel, value = "", size=(326, -1))
        ftp_dir_sizer=wx.BoxSizer(wx.HORIZONTAL)
        ftp_dir_sizer.AddSpacer(10)
        ftp_dir_sizer.Add(ftp_dir)
        ftp_dir_sizer.Add(self.edit_ftp_dir)
        
        ftp_suffix = wx.StaticText(panel, label = "FASTA Suffix: ", size=(175, -1))
        ftp_suffix.SetFont(entry_font)
        self.edit_suffix = wx.TextCtrl(panel, value = "", size=(326, -1))
        ftp_suffix_sizer=wx.BoxSizer(wx.HORIZONTAL)
        ftp_suffix_sizer.AddSpacer(10)
        ftp_suffix_sizer.Add(ftp_suffix)
        ftp_suffix_sizer.Add(self.edit_suffix)
        
        
        #local fasta layout and bindings
        fasta_info = wx.StaticText(panel, label = "Or Select a Subject Database")
        fasta_info.SetFont(header_font)
        local_fasta = wx.StaticText(panel, label = "Local FASTA: ", size=(175, -1))
        local_fasta.SetFont(entry_font)
        self.edit_fasta = wx.TextCtrl(panel, value = "", size=(326, -1))
        self.subject_button = wx.Button(panel, label="Subject")        
        self.subject_button.Bind(wx.EVT_BUTTON, self.openfile)


        local_fasta_sizer=wx.BoxSizer(wx.HORIZONTAL)
        local_fasta_sizer.AddSpacer(5)
        local_fasta_sizer.Add(local_fasta)
        local_fasta_sizer.Add(self.edit_fasta)
        local_fasta_sizer.AddSpacer(10)
        local_fasta_sizer.Add(self.subject_button)
        
        
        # query fasta layout and bindings
        query_info = wx.StaticText(panel, label = "Local Query Database")
        query_info.SetFont(header_font)
        query = wx.StaticText(panel, label = "Local FASTA: ", size=(175, -1))
        query.SetFont(entry_font)
        self.edit_query = wx.TextCtrl(panel, value = "", size=(326, -1))
        self.query_button = wx.Button(panel, label="Query")
        self.query_button.Bind(wx.EVT_BUTTON, self.openfile)
        query_sizer=wx.BoxSizer(wx.HORIZONTAL)
        query_sizer.AddSpacer(5)
        query_sizer.Add(query)
        query_sizer.Add(self.edit_query)
        query_sizer.AddSpacer(10)
        query_sizer.Add(self.query_button)
        
        
        #add all run, ftp, local/remote, query to a single sizer for UI
        info_sizer=wx.BoxSizer(wx.VERTICAL)
        info_sizer.Add(run_info)
        info_sizer.AddSpacer(10)      
        info_sizer.Add(ri_sizer)
        info_sizer.AddSpacer(10)
        info_sizer.Add(rd_sizer)
        info_sizer.Add(ftp_info)
        info_sizer.AddSpacer(10)
        info_sizer.Add(ftp_sizer)
        info_sizer.AddSpacer(10)
        info_sizer.Add(ftp_dir_sizer)
        info_sizer.AddSpacer(10)
        info_sizer.Add(ftp_suffix_sizer)
        info_sizer.AddSpacer(10)
        info_sizer.Add(fasta_info)
        info_sizer.Add(local_fasta_sizer)

        sbox = wx.StaticBox(panel, -1, 'Query Info:') 
        sboxSizer = wx.StaticBoxSizer(sbox, wx.VERTICAL)
        sboxSizer.Add(info_sizer,0,wx.EXPAND, 200)
        
        
        # set up run options including sizing, event bindings
        eval_in = wx.StaticText(panel,label ='E-Value:')
        self.edit_eval= wx.TextCtrl(panel,value="0.001",size=(50,-1))
        eval_box = wx.BoxSizer(wx.HORIZONTAL)
        eval_box.AddSpacer(10)
        eval_box.Add(eval_in)
        eval_box.Add(self.edit_eval)
                
        self.num_hits = wx.StaticText(panel,label ='# Hits:')
        self.hits = wx.SpinCtrl(panel, 1, min=1, max = 5,size=(50,-1))
        self.hits.SetValue(1)
        hits_box = wx.BoxSizer(wx.HORIZONTAL)
        hits_box.AddSpacer(10)
        hits_box.Add(self.num_hits)
        hits_box.Add(self.hits)
 
        self.percent_match = wx.StaticText(panel,label ='% Match:')
        self.match= wx.TextCtrl(panel,value="0.001",size=(50,-1))
        self.match.SetValue("99.0")
        match_box = wx.BoxSizer(wx.HORIZONTAL)
        match_box.AddSpacer(10)
        match_box.Add(self.percent_match)
        match_box.Add(self.match)
        
        self.update = wx.CheckBox(panel, -1, 'Update Fasta')
        self.show_align= wx.CheckBox(panel,-1, 'Show Alignments')
        self.show_align.Bind(wx.EVT_CHECKBOX, self.alignment_warning)

        
        # add run options to a sizer for layout managment                                          
        options = wx.BoxSizer(wx.HORIZONTAL)
        options.AddSpacer(10)
        options.Add(eval_box)
        options.AddSpacer(25)
        options.Add(match_box)
        options.AddSpacer(25)
        options.Add(hits_box)
        options.AddSpacer(25)
        options.Add(self.update)
        options.AddSpacer(25)
        options.Add(self.show_align)
        
        #aggreagate query info and options into one sizer for layout managment
        sbox2 = wx.StaticBox(panel, -1, 'Subject Info:') 
        sboxSizer2 = wx.StaticBoxSizer(sbox2, wx.VERTICAL)
        sboxSizer2.Add(query_info)
        sboxSizer2.AddSpacer(10)
        sboxSizer2.Add(query_sizer)
        sboxSizer2.AddSpacer(10)
        sboxSizer2.Add(options)
        
        
        #aggregate all run panels and results panel and options into single panel
        
        run_sizer= wx.BoxSizer(wx.VERTICAL)
        run_sizer.Add(sboxSizer, wx.ALIGN_CENTER)
        run_sizer.AddSpacer(10)
        run_sizer.Add(sboxSizer2)
        run_sizer.AddSpacer(10)
        self.run_button = wx.Button(panel, label="Run",size=(100,50))
        self.run_button.Bind(wx.EVT_BUTTON,self.run)
        run_sizer.Add(self.run_button,0,wx.ALIGN_CENTRE)        
        self.result_box = wx.TextCtrl(panel, size=(600,450), style=wx.TE_MULTILINE | wx.TE_READONLY |wx.HSCROLL)
        
        
        #set layout for run and result panels
        main_sizer=wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.AddSpacer(25)
        main_sizer.Add(run_sizer,0,wx.ALIGN_LEFT,wx.EXPAND)
        main_sizer.AddSpacer(25)
        main_sizer.Add(self.result_box,0,wx.ALIGN_RIGHT,wx.EXPAND)

        
        layout_sizer=wx.BoxSizer(wx.VERTICAL)
        layout_sizer.AddSpacer(50)
        layout_sizer.Add(main_sizer,1,wx.EXPAND)
        layout_sizer.AddSpacer(50)

          
        #set layout and display UI
        self.SetSizer(layout_sizer)
        self.Centre()                    
        self.Show()
    
    # Menu Item events        
    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, "Annow version 1.0 Gene Annotation Software\nCreated and maintained by Ashkan Bigdeli\nFree to use and distribute\nSource code and the latest version can be found on Github\nhttps://github.com/ashbig/Annow/", "Annow", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.
        
    def OnManual(self,e):
        # Create a message dialog box
        man_page = ManualWindow()
        man_page.Show()
        
               
    def OnExit(self,e):
        self.Close(True)  # Close the frame.
    
    # GUI Events
    def openfile(self, event):
       dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
       label = event.GetEventObject().GetLabel()
       if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if label == "Subject":
                    self.edit_fasta.SetValue(path)
                if label == "Query":
                    self.edit_query.SetValue(path)
       dlg.Destroy()
        
    def opendir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        label = event.GetEventObject().GetLabel()
        if dlg.ShowModal() == wx.ID_OK:
            if label == "Directory":
                self.editrun_dir.SetValue(dlg.GetPath())
        dlg.Destroy()
    
        
    def alignment_warning(self,e):
        if self.show_align.IsChecked():
            dlg = wx.MessageDialog(self, 'Generating Alignments Will Increase Run Time 2x !', 'Annow 1.0', wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
           
    # Data processing event
    def run(self, event):
        run_name = self.editrun.GetValue()
        run_name = run_name.replace(" ", "_")
        run_dir = self.editrun_dir.GetValue()
        ftp_url = self.edit_ftp.GetValue()
        ftp_dir = self.edit_ftp_dir.GetValue()
        ftp_suffix = self.edit_suffix.GetValue()
        local_subject = self.edit_fasta.GetValue()
        query_db = self.edit_query.GetValue()
        evalue = self.edit_eval.GetValue()
        hit_val = self.hits.GetValue()
        alignments = self.show_align.GetValue()
        update_fasta = self.update.GetValue()
        match_val = self.match.GetValue()
        
        #check to see if we have input from the user
        if len(run_name) < 1:
            self.editrun.SetValue("You Must Enter A Run Name!")
            return
        if len(run_dir) < 1:
            self.editrun_dir.SetValue("You Must Enter An Output Directory!")
            return                
        if len(ftp_url) <1 or len(ftp_dir) <1 or len(ftp_suffix) < 1:
            if len(local_subject) < 1:
                self.edit_ftp.SetValue("You Must Enter Remote or Subject Database Completely!")
                return
        if len(query_db) < 1:
            self.edit_query.SetValue("You Must Enter A Query FASTA!")
            return        
        
        
        #display run params for user
        self.result_box.AppendText("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.result_box.AppendText("\n\nRUN PARAMETERS:\n")
        self.result_box.AppendText("Run Name: " + run_name +"\n")
        self.result_box.AppendText("Run Directory: " + run_dir +"\n")
        self.result_box.AppendText("FTP Site: " + ftp_url + "\n")
        self.result_box.AppendText("FTP Directory: " + ftp_dir + '\n')
        self.result_box.AppendText("FTP File Suffix: " + ftp_suffix + '\n')
        self.result_box.AppendText("Local Subject DB: " + local_subject + '\n')
        self.result_box.AppendText("Query Database: " + query_db + '\n')
        self.result_box.AppendText("Blast E-Value: " + evalue + '\n')
        self.result_box.AppendText("Match Criteria for Updating: " + str(match_val) + '\n')        
        self.result_box.AppendText("Sequence Hits: " + str(hit_val) + '\n')
        self.result_box.AppendText("Generate Alignments: " + str(alignments) + '\n')               
        self.result_box.AppendText("Update Input Query: " + str(update_fasta) + '\n\n')        
        self.result_box.AppendText("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

        # make run specific directory
        time = strftime("-%m-%d-%H-%M")
        new_run_path = os.path.join(run_dir,(run_name + time))
        os.mkdir(new_run_path, 0755)
        
        #if ftp, download, unzip, concatenate and generate a file fasta file
        if len(local_subject) < 1:
            
            self.result_box.AppendText("Downloading FASTA files...\n")
            dwnld_msg = pid_etr.download(ftp_suffix, ftp_url, ftp_dir, run_name, new_run_path)
            self.result_box.AppendText(dwnld_msg + "\n")
            if "error" in dwnld_msg:
                return
            
            self.result_box.AppendText("Unzipping Downloaded FASTA's...\n") 
            unzip_msg = pid_etr.unzip(new_run_path)
            self.result_box.AppendText(unzip_msg + "\n")
            if "error" in unzip_msg:
                return
            
            self.result_box.AppendText("Removing Intermmediate Files...\n") 
            remove_msg = pid_etr.remove(ftp_suffix, new_run_path)
            self.result_box.AppendText(remove_msg + "\n")
            if "error" in remove_msg:
                return
                
            self.result_box.AppendText("Concatinating Files...\n") 
            concat = pid_etr.concat_fasta(run_name, new_run_path)
            concat_msg = concat[0]
            self.result_box.AppendText(concat_msg + "\n")
            if "error" in concat_msg:
                return
            local_subject= concat[1]
            
            self.result_box.AppendText("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        #create blast database and update user
        self.result_box.AppendText("\n\nMaking BLAST Database...\n") 
        make_blast_db = pid_etr.create_db(new_run_path, local_subject, run_name)
        blast_db_msg = make_blast_db[0]
        self.result_box.AppendText(blast_db_msg)
        if "error" in blast_db_msg:
            return
            
        blast_db = make_blast_db[1]
        blast_db_summary = make_blast_db[2]
        with open(blast_db_summary) as summary:
            for line in summary:
                self.result_box.AppendText(line)
                
        self.result_box.AppendText(blast_db_msg)
                
        # perform blast and update user
        self.result_box.AppendText("\n\nPerforming blast...\n\n")
        results_tuple = pid_etr.perform_blast(query_db, blast_db, new_run_path, run_name, evalue, str(hit_val))
        result_msg = results_tuple[0]
        self.result_box.AppendText(result_msg)
        if "error" in result_msg:
            return
        results = results_tuple[1]
        self.result_box.AppendText("Blast complete! Raw Results are located in " + results + "\n\n")
        
        self.result_box.AppendText("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        # summarize results and update user
        self.result_box.AppendText("\nSummarizing results...")
        summarize_tuple = pid_etr.summarize_results(results, match_val,str(hit_val))
        summarize_msg = summarize_tuple[0]
        self.result_box.AppendText(summarize_msg)
        if "error" in summarize_msg:
            return
        summary = summarize_tuple[1]
        new_annotation = summarize_tuple[2]
        if "Concordance" in new_annotation:
            update_fasta=False
            self.result_box.AppendText("\n" + new_annotation + "\n")

        # update fasta is asked
        if update_fasta:
            self.result_box.AppendText("\n\n\nGenerating a new FASTA with updated annotations...\n\n")
            update_tuple = pid_etr.update_fasta(run_dir, run_name, new_annotation, query_db)
            update_message = update_tuple[0]
            self.result_box.AppendText(update_message)
            if "error" in update_message:
                return
                
            self.result_box.AppendText("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        # provide alignments if asked
        if alignments:
            self.result_box.AppendText("\nGenerating an alignments file...")
            alignments_tuple = pid_etr.perform_blast_align(query_db, blast_db, new_run_path, run_name, evalue, str(hit_val))
            align_message = alignments_tuple[0]
            self.result_box.AppendText(align_message)
            if "error" in align_message:
                return

        self.result_box.AppendText("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        self.result_box.AppendText("\n\nYour run is complete! Check " + run_dir + " for your results!\n\n\n")
     
        
        
#run app
app = wx.App(False)
frame = MainWindow(None, "Annow 1.0")
app.MainLoop()