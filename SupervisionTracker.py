from ast import main
from calendar import c
from itertools import count
from pickle import TRUE
from re import S
import tkinter as tk 
from tkinter import ttk
from dataclasses import dataclass
import sqlite3
from tkinter.tix import PopupMenu


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

           #------------------------------------------------TAB # 1- SCHEDULE------------------------------------------------------------------------------------
            #Lets start working on the first tab , which is the manage tab , here i will add a label and a button that when clicked will call a function
            self.titleT1=tk.Label(self.tab1, text="Welcome to the Supervision Tracker", font=("Arial", 16) )
            self.titleT1.pack(pady=10)

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
            self.table.grid(column = 3 , row= 1 ,sticky = 'nsew')

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
        self.connection.commit()
 
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

     #delete record 
    
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
#window.mainloop()
