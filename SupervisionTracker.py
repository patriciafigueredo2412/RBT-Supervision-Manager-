from ast import main
from calendar import c
from itertools import count
from pickle import TRUE
from re import S
import tkinter as tk 
from tkinter import CENTER, SEL, ttk
from dataclasses import dataclass
import sqlite3
from tkinter.tix import PopupMenu
from tkinter import filedialog


#My GIU CLASS 
class MyGUI :

        def __init__(self) :
            #we make the connection of the app with the database
            self.db= DatabaseManager("records.db")
            self.db.create_table()
            #define within my class my window , which includes a title and a geometry , then i have the components of it 
            self.window = tk.Tk()
            self.window.title("Supervision Tracker")
            self.window.geometry("1000x1000")
            # i will be using the notebook widget to create two tabs , one for managing the students and the other for the records , i need to import ttk.Notebook
            self.notebook=ttk.Notebook(self.window)
            #each tab its its own frame , and then i add the frames to the notebook with a text for each tab
            self.tab1=tk.Frame(self.notebook)
            self.tab2=tk.Frame(self.notebook)
            #add my tabs to my notebook that is in my window 
            self.notebook.add(self.tab1, text= "Manage")    
            self.notebook.add(self.tab2, text = "Records")
            self.notebook.pack(expand=True, fill="both")
           #-------------------------------------------------------------------------------------------------------------------------------------
           #------------------------------------------------TAB # 1- SCHEDULE-------------------------------------------------------------------
           #----------------------------------------------------------------------------------------------------------------------------------------
            #Lets start working on the first tab , which is the manage tab , here i will add a label and a button that when clicked will call a function
            self.titleT1=tk.Label(self.tab1, text="Welcome to the Supervision Tracker", font=("Arial", 16) )
            self.titleT1.grid(row=0, column=0 , columnspan=4 , pady=10)

            '''
            1-Create the GUI 
            Create a dropdown box , when you click on the dropdown box it shows you the names of the RBTs that you have in your database, when you select one of the names it shows you the schedule of that RBT, and then you can edit the schedule and save it again to the database
            Create a button that says "Add RBT" when you click on it it opens a new window where you can add the name of the RBT, the client, the start date and the end date, and then when you click on submit it saves that information to the database and shows it in the records tab
            Create a button that deletes a record, when you click on it it opens a new window where you can enter the name of the RBT that you want to delete, and then when you click on submit it deletes that record from the database and updates the records tab
            Create two entry boxes , one to put the total hours , and one to put the amount of the month so far 
            2-Create the database
            3-Create the functions for the buttons and the dropdown box
            4-Create the email connection 
           
            '''
            #Grid layout Tab 1 
            self.tab1.rowconfigure(0, weight=1)
            self.tab1.rowconfigure(1, weight=1)
            self.tab1.rowconfigure(2, weight=1)
            self.tab1.rowconfigure(3, weight=1)
            self.tab1.columnconfigure(0, weight=1)
            self.tab1.columnconfigure(1, weight=1)
            self.tab1.columnconfigure(2, weight=1)
            self.tab1.columnconfigure(3, weight=1)
            #----BUTTONS AND LABELS FOR TAB 1------------------------------------------------------------------------------------

            #Label  
            self.labelt1= tk.Label(self.tab1, text="Select an RBT to see their schedule", font=("Arial", 12) )
            self.labelt1.grid(row=1, column=0 , columnspan=4 , pady=10)

            #Dropped Down box
            self.clicked = tk.StringVar()
            rbt_list=self.db.get_names()   #get the names of the RBTs from the database)
            self.drop = ttk.Combobox(self.tab1, textvariable=self.clicked )
            self.drop['values'] = rbt_list
            self.clicked.set("Select an RBT") 
            self.drop.grid(row=2, column=0 , columnspan=4 ,sticky= "ew",  pady=10)

            #Entry box for total hours
            self.entry_hours= tk.Entry(self.tab1 , text = "Enter the ammount of hours ")
            self.entry_hours.grid(row=3 , column=0 )

            #Button to add hours
            self.addhours= tk.Button(self.tab1, text="Add Hours", command = self.add_hours )
            self.addhours.grid(row=3, column=1 , pady=10)

            #refresh month button (TEMPORAL)
            self.reset=tk.Button(self.tab1, text="Reset Hours ", command=self.refresh_month)
            self.reset.grid(row=3, column=2 , pady=10)

            #Display Status 
            self.status= tk.StringVar()
            self.status.set("Not Met")
            self.statusLabel= tk.Label(self.tab1, text =self.status.get() , font=("Arial", 12) )
            self.statusLabel.grid(row=3, column=3 , pady=10)

            #Add Button : popup to select add manual or upload file 
            self.addrbt= tk.Button(self.tab1, text="Add RBT", command = self.add_schedule)
            self.addrbt.grid(row=4, column=0 , pady=10)

            #Edit button 
            self.edit= tk.Button(self.tab1, text="Edit Schedule", command = self.edit_schedule )
            self.edit.grid(row=4, column=1 , pady=10)

            #Delete button 
            self.deleteT1= tk.Button(self.tab1, text="Delete RBT", command = self.delete_schedule )
            self.deleteT1.grid(row=4, column=2 , pady=10)

            #--------------------------------------------Table for tab 1------------------------------------------------------------------------------------
            #Table to show the schedule of the RBTs
            self.scheduleTable=ttk.Treeview(self.tab1)
            self.scheduleTable.grid(column = 0 , row= 5 , columnspan=4 , sticky = 'nsew')
            self.scheduleTable['columns'] = ("RBT", "Hours", "Status")
            self.scheduleTable.column("#0", width=0, stretch=tk.NO)   #phantom column
            self.scheduleTable.column("RBT", anchor=tk.W, width=120)
            self.scheduleTable.column("Hours", anchor=tk.CENTER, width=100)
            self.scheduleTable.column("Status", anchor=tk.CENTER, width=100)
            self.scheduleTable.heading("#0" , text = "Label" , anchor= tk.W)
            self.scheduleTable.heading("RBT", text= "RBT Name" , anchor= tk.W )
            self.scheduleTable.heading("Hours", text= "Hours" , anchor= tk.W )
            self.scheduleTable.heading("Status" , text="Status")

            #insert  data to the schedule table
            all_schedules= self.db.get_all_schedules()   #get all the data from the database
            for row in all_schedules:
                self.scheduleTable.insert(parent='', index='end', values=row)
            




            

            #------------------------------------------------------------------------------------------------------------------------------------------
            #-----------------------------------------------TAB # 2 - RECORDS------------------------------------------------------------------------------------
            #------------------------------------------------------------------------------------------------------------------------------------------
           #Stablish a grid layout for the second tab 
            self.tab2.rowconfigure(0, weight=1)
            self.tab2.rowconfigure(1, weight=1)
            self.tab2.rowconfigure(2, weight=1)
            self.tab2.rowconfigure(3, weight=1)
            self.tab2.rowconfigure(4, weight=1)
            self.tab2.columnconfigure(0, weight=1)
            self.tab2.columnconfigure(1, weight=1)
            self.tab2.columnconfigure(2, weight=5)
            #----BUTTONS AND LABELS FOR TAB 2------------------------------------------------------------------------------------
            #I have a label , and two buttons that when clicked call their own functions 
            self.titleT2 = tk.Label(self.tab2, text="Here are the records of all your supervised RBTs", font=("Arial", 13) )
            self.titleT2.grid(row=0, column=0 , columnspan=3 , pady=5 )
            #Search Button 
            self.btsearch= tk.Button(self.tab2, text = "Search" , command=self.t2search)
            self.btsearch.grid(column = 0, row = 1 )

            self.input=tk.Entry(self.tab2)
            self.input.grid(row= 1, column = 1)

            #ADD button 
            self.add=tk.Button(self.tab2, text="ADD" , command=self.add_record)
            self.add.grid(column=0,row=2 , pady=10 )


            #Update Button 
            self.updatet2= tk.Button(self.tab2 , text= "Update ", command= self.on_update_click )
            self.updatet2.grid(column=0, row = 3)
           
           #Delete Button
            self.deletet2= tk.Button(self.tab2 , text= "Delete" , command= self.on_delete_click)
            self.deletet2.grid(column=0, row = 4)

           #Order by name 
            self.order_name= tk.Button(self.tab2 , text= "Order by Name" , command= self.name_order )
            self.order_name.grid(column=1, row = 2)
          
           #Order by date
            self.order_date= tk.Button(self.tab2 , text= "Order by Date" , command= self.date_order )
            self.order_date.grid(column=1, row = 3)

           #Reload button to show all the records again after doing a search or an order
            self.reload= tk.Button(self.tab2 , text= "Reload" , command= self.refresh_table)
            self.reload.grid(column=1, row = 4)

           #-----TABLE FOR TAB 2------------------------------------------------------------------------------------
       
            self.table= ttk.Treeview(self.tab2)
            self.table.grid(column = 3 , row= 1 ,columnspan = 3 , sticky = 'nsew')

            #define the columns of the table
            self.table['columns'] = ("Name", "Client", "Start Date" , "End Date")
            #For each column i need to define the heading and the width
            self.table.column("#0", width=0, stretch=tk.NO)   #phantom column 
            self.table.column("Name", anchor=tk.W, width=120)
            self.table.column("Client", anchor=tk.W, width=120)
            self.table.column("Start Date", anchor=tk.CENTER, width=100)
            self.table.column("End Date", anchor=tk.CENTER, width=100)
            #Headers 
            self.table.heading("#0" , text = "Label" , anchor= tk.W)
            self.table.heading("Name", text= "RBT Name" , anchor= tk.W )
            self.table.heading("Client", text= "Client" , anchor= tk.W )
            self.table.heading("Start Date", text= "Start Date" , anchor= tk.W )
            self.table.heading("End Date" , text="End Date")
          
          #Insert the date on the treeview 
            all_data= self.db.get_all_records()   #get all the data from the database
            for row in all_data:
                self.table.insert(parent='', index='end', values=row)
            self.window.mainloop()

      
        #-----Functions for the buttons of tab1------------------------------------------------------------------------------------
        def see(self):
            print(self.clicked.get())
       
        #refresh
        def refresh_hours(self):
            info=self.db.get_all_schedules()
            for items in self.scheduleTable.get_children():    #empty my table 
                self.scheduleTable.delete(items)
            for row in info:
                self.scheduleTable.insert(parent='', index='end', values=row)

        #add schedule function : manual and upload 
        def add_schedule(self):
            popup=tk.Toplevel(self.window)
            popup.title("Add Schedule")
            manual=tk.Button(popup, text="Add Manually", command= self.add_manual)
            manual.pack(pady=10)
            upload=tk.Button(popup, text="Upload File", command= self.upload_file)
            upload.pack(pady=10)
        
        def add_manual(self):
            popup=tk.Toplevel(self.window)
            popup.title("Add Schedule Manually")
            #Function to submit the information of the entries to the database and close the popup window
            def submit():
                new_schedule= Schedule(NameEntry.get(), ClientEntry.get(), int(MonthEntry.get()), 0, "Not Met")
                self.db.add_schedules(new_schedule)
                self.refresh_hours()
                popup.destroy()

            popup.columnconfigure(0, weight=1)
            popup.columnconfigure(1, weight=1)
            popup.columnconfigure(2, weight=1)
            popup.columnconfigure(3, weight=1)
            popup.rowconfigure(0, weight=1)
            popup.rowconfigure(1, weight=1)
            popup.rowconfigure(2, weight=1)
            popup.rowconfigure(3, weight=1)
            #Create the labels and entries for the popup window
            Name= tk.Label(popup , text="RBT Name: " , font=("Arial", 12) )
            Name.grid(row=0, column=0 , padx=10 , pady=10)
            Client= tk.Label(popup , text="Client Name: " , font=("Arial", 12) )
            Client.grid(row=1, column=0 , padx=10 , pady=10)
            Month= tk.Label(popup , text="Approved hours a month : " , font=("Arial", 12) )
            Month.grid(row=2, column=0 , padx=10 , pady=10)
            #Create the entries for the popup window
            NameEntry= tk.Entry(popup , width=30)
            NameEntry.grid(row=0, column=1 , padx=10 , pady=10)
            ClientEntry= tk.Entry(popup , width=30)
            ClientEntry.grid(row=1, column=1 , padx=10 , pady=10)
            MonthEntry= tk.Entry(popup , width=30)
            MonthEntry.grid(row=2, column=1 , padx=10 , pady=10)
                #Create the submit button for the popup window
            submit=tk.Button(popup, text = "Submit" , command= submit)
            submit.grid(row=3, column=0 , columnspan=2 , pady=10)

        def upload_file(self):
            file_path = filedialog.askopenfilename(title="Select File to upload ", filetypes=[("Text File", ('*.txt')), ("All files", "*.*")])
            print("Selected File:", file_path)

       
        #add hours to the db 
        def add_hours(self):
            rbt_name= self.clicked.get()
            if rbt_name == "Select an RBT":
                return
            #get new hours 
            new_hours=self.entry_hours.get()
            #get the old hours 
            self.db.cursor.execute('''SELECT hours FROM hours WHERE rbt_name= ? ''', (rbt_name,)) 
            prev_hours=self.db.cursor.fetchone()
            #print 
            total_hours= int(prev_hours[0]) + int(new_hours)
            #update the hours in the database
            new_value= Schedule(rbt_name,"" , "" , total_hours, "")
            self.db.update_schedule(new_value)
            self.db.update_status(rbt_name)
            self.refresh_hours()

        #refresh the month 
        def refresh_month(self):
            #loop the db , and for each RBT reset hours to zero , then update the status and refresh table 
            self.db.refresh_month()
            self.refresh_hours()

        #delete the schedule 
        def delete_schedule(self):
            self.db.delete_schedule(self.clicked.get())
            self.refresh_hours()

        #edit the schedule 
        def edit_schedule(self):
            if self.clicked.get() == "Select an RBT":
                return

            popup=tk.Toplevel(self.window)
            popup.title("Edit Schedule")
            
            def edit():
               if not new_monthEntry.get().isdigit():
                   error=tk.Toplevel(popup)
                   error.title("Error")
                   error_label=tk.Label(error, text="Please enter a valid number for the hours of the month")
                   error_label.pack(pady=10)
                   return
               
               new_value= Schedule(self.clicked.get(),"", new_monthEntry.get(),"","")
               self.db.edit_schedule(new_value)
               self.db.update_status(self.clicked.get())
               self.refresh_hours()
               popup.destroy()

            popup.columnconfigure(0, weight=1)
            popup.columnconfigure(1, weight=1)
            popup.rowconfigure(0, weight=1)
            popup.rowconfigure(1, weight=1)
            #Create the labels and entries for the popup window
            new_month= tk.Label(popup , text="Approved hours a month : " , font=("Arial", 12) )
            new_month.grid(row=0, column=0 , padx=10 , pady=10)
            #Create the entries for the popup window
            new_monthEntry= tk.Entry(popup , width=30)
            new_monthEntry.grid(row=0, column=1 , padx=10 , pady=10)
            #Create the submit button for the popup window
            submit=tk.Button(popup, text = "Submit" , command= edit)
            submit.grid(row=1, column=1 , columnspan=2 , pady=10)
           


        #-----Functions for the buttons of tab2------------------------------------------------------------------------------------
         #create a refresh method to update the table with the new records
        def refresh_table(self):
            for items in self.table.get_children():    #empty my table 
                self.table.delete(items)
            all_data= self.db.get_all_records()   #get all the data from the database
            for row in all_data:
                self.table.insert(parent='', index='end', values=row)
                    
        def add_record(self):
            popup=tk.Toplevel(self.window)
            popup.title("Add Record")

            def submit():
                #save the entry information into the RBTrecord class and then add it to the database, close the popup window
                new_record=RBTRecord(rbt_name.get(), client_name.get(), start_date_label.get(), end_date_label.get())
                self.db.add_record(new_record)
                self.refresh_table()
                popup.destroy()


            popup.columnconfigure(0, weight=1)
            popup.columnconfigure(1, weight=1)
            popup.columnconfigure(2, weight=1)
            popup.rowconfigure(0, weight=1)
            popup.rowconfigure(1, weight=1)
            popup.rowconfigure(2, weight=1)
            popup.rowconfigure(3, weight=1)
            popup.rowconfigure(4, weight=1)

            #Create the labels and entries for the popup window
            #Labels
            rbt_name_label= tk.Label(popup , text="RBT Name: " , font=("Arial", 12) )
            rbt_name_label.grid(row=0, column=0 , padx=10 , pady=10)
            client_name_label= tk.Label(popup , text="Client Name: " , font=("Arial", 12) )
            client_name_label.grid(row=1, column=0 , padx=10 , pady=10)
            start_date_label= tk.Label(popup , text="Start Date: " , font=("Arial", 12) )
            start_date_label.grid(row=2, column=0 , padx=10 , pady=10)
            end_date_label= tk.Label(popup , text="End Date: " , font=("Arial", 12) )
            end_date_label.grid(row=3, column=0 , padx=10 , pady=10)

            #Entries
            rbt_name= tk.Entry(popup , width=30)
            rbt_name.grid(row=0, column=1 , padx=10 , pady=10)
            client_name= tk.Entry(popup , width=30)
            client_name.grid(row=1, column=1 , padx=10 , pady=10)
            start_date_label= tk.Entry(popup , width=30)
            start_date_label.grid(row=2, column=1 , padx=10 , pady=10)
            end_date_label= tk.Entry(popup , width=30)
            end_date_label.grid(row=3, column=1 , padx=10 , pady=10)


            #create the submit button for the popup window
            submit=tk.Button(popup, text = "Submit" , command= submit)
            submit.grid(row=4, column=0 , columnspan=2 , pady=10)
           
        def t2search(self):
            #clear the table before showing the search results
            for items in self.table.get_children():    #empty my table 
                self.table.delete(items)
            #show the new info on the table
            search_result= self.db.search_record(self.input.get())
            for row in search_result:
                self.table.insert(parent='', index='end', values=row)
               
        def on_update_click(self):
            #clear the table 
            

            def submit():
                #get the new information from the entries and update the record in the database, then refresh the table and close the popup window
                new_record=RBTRecord(rbt_name.get(), client_name.get(), start_date_label.get(), end_date_label.get())
                self.db.update_record(self.input.get(), new_record)
                self.refresh_table()
                popup.destroy()

            #pop uo window to ask for the new information of the record that we want to update
            popup=tk.Toplevel(self.window)
            popup.title("Update Record")
            popup.columnconfigure(0, weight=1)
            popup.columnconfigure(1, weight=1)
            popup.columnconfigure(2, weight=1)
            popup.rowconfigure(0, weight=1)
            popup.rowconfigure(1, weight=1)
            popup.rowconfigure(2, weight=1)
            popup.rowconfigure(3, weight=1)
            popup.rowconfigure(4, weight=1)

            #Create the labels and entries for the popup window
            #Labels
            rbt_name_label= tk.Label(popup , text="RBT to Update: " , font=("Arial", 12) )
            rbt_name_label.grid(row=0, column=0 , padx=10 , pady=10)
            client_name_label= tk.Label(popup , text="Client Name: " , font=("Arial", 12) )
            client_name_label.grid(row=1, column=0 , padx=10 , pady=10)
            start_date_label= tk.Label(popup , text="Start Date: " , font=("Arial", 12) )
            start_date_label.grid(row=2, column=0 , padx=10 , pady=10)
            end_date_label= tk.Label(popup , text="End Date: " , font=("Arial", 12) )
            end_date_label.grid(row=3, column=0 , padx=10 , pady=10)

            #Entries
            rbt_name= tk.Entry(popup , width=30)
            rbt_name.grid(row=0, column=1 , padx=10 , pady=10)
            client_name= tk.Entry(popup , width=30)
            client_name.grid(row=1, column=1 , padx=10 , pady=10)
            start_date_label= tk.Entry(popup , width=30)
            start_date_label.grid(row=2, column=1 , padx=10 , pady=10)
            end_date_label= tk.Entry(popup , width=30)
            end_date_label.grid(row=3, column=1 , padx=10 , pady=10)


            #create the submit button for the popup window
            submit=tk.Button(popup, text = "Submit" , command= submit)
            submit.grid(row=4, column=0 , columnspan=2 , pady=10)  

        def on_delete_click(self):
               
            popupMedu=tk.Toplevel(self.window)
            popupMedu.title("Delete Record")
                #create the label and entry for the popup window
            label=tk.Label(popupMedu , text="Enter the name of the RBT you want to delete: " , font=("Arial", 12) )
            label.grid(row=0, column=0 , padx=10 , pady=10)
            entry=tk.Entry(popupMedu , width=30)
            entry.grid(row=0, column=1 , padx=10 , pady=10)
                #create the submit button for the popup window
            def submit():
                self.db.delete_record(entry.get())
                self.refresh_table()
                popupMedu.destroy()
                #create the submit button 
            button=tk.Button(popupMedu , text="Delete" , command= submit)
            button.grid(row=1, column=0 , columnspan=2 , pady=10)

        def name_order(self):
            for items in self.table.get_children():    #empty my table
                self.table.delete(items)
            sorted_result=self.db.sort_by_name()
            for i in sorted_result: 
                self.table.insert(parent='', index='end', values=i)

        def date_order(self):
            for items in self.table.get_children():    #empty my table
                self.table.delete(items)
            data=self.db.sort_by_date()
            print(data)
            for items in data:
                self.table.insert(parent='', index='end', values=items)


@dataclass
class RBTRecord:
    rbt_name : str
    client_name: str
    start_date: str
    end_date: str

@dataclass
class Schedule: 
    rbt_name : str
    client_name: str
    month :int 
    hours: int
    status :str

#My database Manager For tab2 Class 
class DatabaseManager :
    #initialize 
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    #create the table if it does not exist
    def create_table(self): 
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records 
                            (rbt_name TEXT NOT NULL,
                            client_name TEXT NOT NULL,
                            start_date TEXT NOT NULL,
                            end_date TEXT NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hours 
                            (rbt_name TEXT NOT NULL,
                            client_name TEXT NOT NULL, 
                            month INTEGER NOT NULL ,
                            hours INTEGER NOT NULL,
                            status TEXT NOT NULL)''')
        self.connection.commit()

    #---------------------------------------FUNCTIONS FOR THE HOURS TABLE------------------------------------------------------------------------------------
    #add records to the hours table
    def add_schedules(self, schedule : Schedule):
        self.cursor.execute('''INSERT INTO hours (rbt_name, client_name , month , hours , status) 
                               VALUES (?,?,?,?,?)''', (schedule.rbt_name, schedule.client_name, schedule.month, schedule.hours, schedule.status))
        self.connection.commit()
    
    #get all the schedules
    def get_all_schedules(self):
        self.cursor.execute('''SELECT rbt_name, hours, status FROM hours''')
        return self.cursor.fetchall()

    #delete record 
    def delete_schedule(self, rbt_name):
        self.cursor.execute('''DELETE FROM hours WHERE rbt_name= ? ''' ,(rbt_name,))
        self.connection.commit()

    #update record 
    def update_schedule(self, new_value: Schedule):       
        self.cursor.execute('''UPDATE hours SET hours=? WHERE rbt_name = ?''' , 
                            ( new_value.hours, new_value.rbt_name))
        self.connection.commit()

    #get RBT names 
    def get_names(self):
        self.cursor.execute("SELECT rbt_name FROM hours")
        return self.cursor.fetchall()

    #get status of a schedule
    def update_status(self, rbt_name):
        hours = float(self.cursor.execute('''SELECT hours FROM hours WHERE rbt_name= ? ''' , (rbt_name,)).fetchone()[0])
        month = self.cursor.execute('''SELECT month FROM hours WHERE rbt_name= ? ''' , (rbt_name,)).fetchone()[0]
        if hours >= (month*5/100):
            status = "Met"
        else:
                status = "Not Met"

        self.cursor.execute('''UPDATE hours SET status=? WHERE rbt_name= ? ''' , (status , rbt_name))

    #refresh month : reset hours to zero for all the RBTs and update the status
    def refresh_month(self):
        self.cursor.execute('''UPDATE hours SET hours=0''')
        self.cursor.execute('''UPDATE hours SET status="Not Met"''')
        self.connection.commit()


    #edit schedule : fixing info on the schedule of an RBT
    def edit_schedule(self,new_value:Schedule):
        self.cursor.execute(''' UPDATE hours SET month=? WHERE rbt_name = ?''' , (new_value.month, new_value.rbt_name))
        self.connection.commit()


    #---------------------------------------FUNCTIONS FOR THE DATABASE MANAGER CLASS------------------------------------------------------------------------------------
    #add records to the database
    def add_record(self, record: RBTRecord):
        self.cursor.execute('''INSERT INTO records (rbt_name, client_name, start_date, end_date) 
                                VALUES (?, ?, ?, ?)''', (record.rbt_name, record.client_name, record.start_date, record.end_date))
        self.connection.commit()
        
    #get all records 
    def get_all_records(self):
        self.cursor.execute('''SELECT * FROM records''')
        return self.cursor.fetchall()     #fetchall to ensure i get the things I obtained from my database

    #search record by name
    def search_record(self, rbt_name):
        self.cursor.execute('''SELECT * FROM records WHERE rbt_name LIKE ?  ''', (rbt_name,))
        return self.cursor.fetchall()

    
    
    #delete record by name
    def delete_record(self,rbt_name):
        self.cursor.execute('''DELETE FROM records WHERE rbt_name= ? ''' ,(rbt_name,))
        self.connection.commit()

    #update record 
    def update_record(self,rbt_name, new_value: RBTRecord):
        self.cursor.execute('''UPDATE records SET start_date=? , end_date=? WHERE rbt_name = ?''' , 
                            (new_value.start_date,new_value.end_date, rbt_name))
        self.connection.commit()

    #sort by name 
    def sort_by_name(self):
        self.cursor.execute('''SELECT * FROM records ORDER BY rbt_name ASC ''')
        return self.cursor.fetchall()
        
   #sort by date
    def sort_by_date(self):
        self.cursor.execute('''SELECT * FROM records ORDER BY start_date ASC ''')
        return self.cursor.fetchall()
        
    
# --- AT THE VERY BOTTOM OF YOUR SCRIPT ---
if __name__ == "__main__":
    # This creates the object, which triggers __init__, 
    # which starts the database and the Tkinter loop.
    app = MyGUI()


#Create the window using Tk
#Label is for a text 
# tk.Text(cuadro de texto , window, font , etc )
#tk.Button( button )
# frames can be with pack , grid , place
#close the loop to close your window 



"""
1-RBT record , ver activo o viejo , leer pdf y que agarre de ahi la infomacion 
2-Manager : 
3- Cliente : avise 2 meses antes de assestment para preparar , 1 mes antes alerta pueda leer el assestment para ver 

"""
#window.mainloop()
