import gspread
import tkinter as tk
from tkinter import messagebox
from tkinter import Canvas
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import END
import glob
import re
from Config import API, LOGO, NAME
data = ['DATE','SESSION', 'WORKOUTS', 'NOTES', 'NT SCORE']

#api= glob.glob('/**/GoogleAPI.json', recursive=True)[0] if glob.glob('/**/GoogleAPI.json', recursive=True) else None
gc = gspread.service_account(filename=API)
sh = gc.open(NAME)

class MainMenu:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("800x700")
        self.root.title("Eye-To-Eye Database")
        self.label = tk.Label(self.root, text="SportsVision Athlete Database", font=("Callabri", 40))
        self.label.pack()

        LogoPath = LOGO
        Logo = Image.open(LogoPath)
        resizedLogo = Logo.resize((800, 350), Image.Resampling.BICUBIC)
        OurCompany = ImageTk.PhotoImage(resizedLogo)
        image_label = tk.Label(self.root, image=OurCompany)
        image_label.pack()

        #The button to open the part of the program to enter a new athlete
        self.NewAthlete = tk.Button(self.root, text='Enter New Athlete',pady=20, padx=71, font=('Callabri', 15)
                                    , command= NewAthlete, fg='white', bg='blue')
        self.NewAthlete.place(x=240, y=510)

        #The button to search an athlete and add a new session
        self.SearchAthlete = tk.Button(self.root, text='Search Exisitng Athlete',pady=20, padx=50, font=('Callabri', 15)
                                       , command= SearchAthlete, fg='white', bg='blue')
        self.SearchAthlete.place(x=240, y=430)

        #BUTTON FUNCTION TO SAVE SPREADSHEET AND CLOSE APP
        def TheEnd():
            self.root.destroy
        #Save file, should always do before closing program
        self.savefile = tk.Button(self.root, text='Save File',pady=20, padx=110, font=('Callabri', 15)
                                  , command= TheEnd, fg='white', bg='blue')
        self.savefile.place(x=240, y=590)

        self.root.mainloop()


class SearchMenu:
    def __init__(self):

        self.SearchTop = tk.Toplevel()
        self.SearchTop.geometry('300x400')
        self.SearchTop.title('Search existing athlete')

        #combo box names to allign to
        def namelist():
            NameList = []
            for Ws in sh.worksheets():
                splitted = str(Ws)
                splitted= splitted.split(' ')
                name = splitted[1]
                Name = name.strip("'")
                NameList.append(Name)
            return NameList
            
        Namelist = namelist()
        print(Namelist)

        def updfunc(butt):
            button = butt.widget
            index=int(button.curselection()[0])
            global value
            value = button.get(index)
            self.svar.set(value)
            #This retreives the name for the worksheet we want to work in
            SearchMenu.namevar = value
            self.thelist.delete(0,END)
            
        #setting up search bar
        self.svar = tk.StringVar()
        self.searchmenu = tk.Entry(self.SearchTop, font=("Callabri",16), textvariable=self.svar)
        self.searchmenu.pack()
        self.thelist = tk.Listbox(self.SearchTop, font=("Callabri",16), relief='flat')
        self.thelist.pack()
        print(self.searchmenu.get())
        
        #Matches names to user input
        def dataretrieve(*args):
            ananlyze = self.searchmenu.get()
            self.thelist.delete(0,END)
            for names in Namelist:
                if(re.match(ananlyze,names,re.IGNORECASE)):
                    self.thelist.insert(tk.END,names)
                    
        self.thelist.bind('<<ListboxSelect>>', updfunc)
        self.svar.trace('w',dataretrieve)
        self.enterbutton = tk.Button(self.SearchTop, text='Enter', pady=5, padx=15, font=('Callabri', 10), fg='white', bg='blue',
                                     command=AthleteMenu)
        self.enterbutton.pack()

#The window to enter date for an exixsting athlete
class Athletemenu:
    def __init__(self):

        self.SearchTop = tk.Toplevel()
        self.SearchTop.geometry('500x300')
        self.SearchTop.title('Search Athlete')

        #SearchAhlete label
        self.label = tk.Label(self.SearchTop, text="SportsVision Athlete "+ value, font=("Callabri", 25))
        self.label.pack()
        
        #Button to Pre-load a session into the athletes database without having to write in notes
        self.session = tk.Button(self.SearchTop, text='Preload Workout', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue', 
                                 command=PRELOAD)
        self.session.pack()

        #Write notes for previous workouts that were already entered into the database
        self.notesbutton = tk.Button(self.SearchTop, text='Enter Notes', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue', 
                                     command=NOTES)
        self.notesbutton.pack()

        def TodaysWorkout():
            ws = sh.worksheet(value)
            thedate = ws.cell(row=2, col=1)
            thedate=thedate.value
            firstworkout = ws.cell(row=2, col=3)
            firstworkout = firstworkout.value
            secondworkout = ws.cell(row=3, col=3)
            secondworkout = secondworkout.value
            thirdworkout = ws.cell(row=4, col=3)
            thirdworkout = thirdworkout.value
            fourthworkout = ws.cell(row=5, col=3)
            fourthworkout = fourthworkout.value
            wkeTop = tk.Toplevel()
            wkeTop.geometry('1200x400')
            label = tk.Label(wkeTop, text="Todays date: " + thedate, font=("Callabri", 40))
            label.pack()
            label1 = tk.Label(wkeTop, text=firstworkout, font=("Callabri", 40))
            label1.pack()
            labe2 = tk.Label(wkeTop, text=secondworkout, font=("Callabri", 40))
            labe2.pack()
            label3 = tk.Label(wkeTop, text=thirdworkout, font=("Callabri", 40))
            label3.pack()
            label4 = tk.Label(wkeTop, text=fourthworkout, font=("Callabri", 40))
            label4.pack()

            Gotit = tk.Button(wkeTop, text='Exit', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue', 
                                     command=wkeTop.destroy)


        self.workouttodaybutton = tk.Button(self.SearchTop, text='Todays Workout', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue', 
                                     command=TodaysWorkout)
        self.workouttodaybutton.pack()

        #BUTTON FUNCTION TO ENTER DATA

        def dataentry():
            thename = SearchMenu.namevar
            ws = sh.worksheet(thename)
            print(ws)
            list = []
            date = self.DateEntry.get()
            list.append(date)   
            workouts = self.WorkoutsEntry.get()
            list.append(workouts)
            notes = self.NotesEntry.get()   
            list.append(notes)
            ws.add_rows(2)
            ws.update('A2', date)
            ws.update('B2',  workouts)
            ws.update('C2', notes)
            messagebox.showinfo('Info Entered', 'session info for ' + thename + ' saved to databse')
            self.SearchTop.destroy

        #Button to save and close the window
        self.endbutton = tk.Button(self.SearchTop, text='Back', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue'
                          , command=dataentry)
        self.endbutton.pack()

        self.SearchTop.mainloop()

#The window to add a new athlete
class NewAthleteMenu:
    def __init__(self):

        self.NewTop = tk.Toplevel()
        self.NewTop.geometry('500x200')
        self.NewTop.title('New Athlete')

        #Newathlete label
        self.label = tk.Label(self.NewTop, text="New SportsVision Athlete", font=("Callabri", 25))
        self.label.pack()

        #Enter new anthlete description label
        self.NewAthlelabl = tk.Label(self.NewTop, text="enter new athlete name:", font=("Callabri",10))
        self.NewAthlelabl.pack()
        self.NewAthlelabl.place(x=100, y=59)
        #ENter ne athlete entry bar
        self.Athletename = tk.Entry(self.NewTop)
        self.Athletename.pack()
        self.Athletename.place(x=250, y=62)
        #BUTTON FUNCTION TO CREATE NEW ATHLETE
        def AthleteCreation():
            Newguy = self.Athletename.get()
            newSS = sh.add_worksheet(title=Newguy, rows=1000, cols=5)
            newSS.append_row(data)
            messagebox.showinfo('Info Entered', 'session info for ' + self.Athletename.get() + ' saved to databse')
            self.NewTop.destroy

        #Button to save and close the window
        self.endbutton = tk.Button(self.NewTop, text='save and close', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue'
                          , command=AthleteCreation)
        self.endbutton.pack()
        self.endbutton.place(x=200, y=92)
        #self.endbutton.grid(row=50, column=10)

        self.NewTop.mainloop()

class Preload:
    def __init__(self):

        self.Pretop = tk.Toplevel()
        self.Pretop.geometry('500x500')
        self.Pretop.title('Session info')

        #Label to enter the date of the session
        self.datLabel = tk.Label(self.Pretop, text="enter date of session:",font=("Callabri",10))
        self.datLabel.pack()
        self.datLabel.place(x=80, y=110)
        #Entry to enter the date of the session
        self.athletename = tk.Entry(self.Pretop)
        self.athletename.pack()
        self.athletename.place(x=220, y=110)

        #Label to enter the session #
        self.numbLabel = tk.Label(self.Pretop, text="enter session number:",font=("Callabri",10))
        self.numbLabel.pack()
        self.numbLabel.place(x=80, y=140)
        #Entry to enter session #
        self.numbename = tk.Entry(self.Pretop)
        self.numbename.pack()
        self.numbename.place(x=220, y=140)


        self.workoutsLabel1 = tk.Label(self.Pretop, text="enter first workout of new session:",font=("Callabri",10))
        self.workoutsLabel1.pack()
        self.workoutsLabel1.place(x=50, y=200)
        #Entry for first workout
        self.work1ename = tk.Entry(self.Pretop)
        self.work1ename.pack()
        self.work1ename.place(x=280, y=200)

        self.workoutsLabel2 = tk.Label(self.Pretop, text="enter second workout of new session:",font=("Callabri",10))
        self.workoutsLabel2.pack()
        self.workoutsLabel2.place(x=50, y=230)
        #Entry for second workout
        self.work2ename = tk.Entry(self.Pretop)
        self.work2ename.pack()
        self.work2ename.place(x=280, y=230)

        self.workoutsLabel3 = tk.Label(self.Pretop, text="enter third workout of new session:",font=("Callabri",10))
        self.workoutsLabel3.pack()
        self.workoutsLabel3.place(x=50, y=260)
        #Entry for third workout
        self.work3ename = tk.Entry(self.Pretop)
        self.work3ename.pack()
        self.work3ename.place(x=280, y=260)

        self.workoutsLabel4 = tk.Label(self.Pretop, text="enter fourth workout of new session:",font=("Callabri",10))
        self.workoutsLabel4.pack()
        self.workoutsLabel4.place(x=50, y=290)
        #Entry for first workout
        self.work4ename = tk.Entry(self.Pretop)
        self.work4ename.pack()
        self.work4ename.place(x=280, y=290)

        def dataentry():
            thename = value
            ws = sh.worksheet(thename)
            wokoutlist = []
            otherlist = []
            date = self.athletename.get()
            otherlist.append(date)
            session = self.numbename.get()
            otherlist.append(session)
            workout1 = self.work1ename.get()
            wokoutlist.append(workout1)
            workout2 = self.work2ename.get()
            wokoutlist.append(workout2)
            workout3 = self.work3ename.get()
            wokoutlist.append(workout3)
            workout4 = self.work4ename.get()
            wokoutlist.append(workout4)
            for i, val in enumerate(wokoutlist):
                rownum = i + 2
                ws.insert_row([otherlist[0], otherlist[1], val], index=rownum)
            for stuff in wokoutlist:
                wokoutlist.remove(stuff)
            for stuff in otherlist:
                otherlist.remove(stuff)
            messagebox.showinfo('Info Entered', 'session info for ' + thename + ' saved to databse')
            self.Pretop.destroy

        self.endbutton = tk.Button(self.Pretop, text='save and close', pady=9, padx=20, font=('Callabri', 12), fg='white', bg='blue'
                          , command=dataentry)
        self.endbutton.pack()
        self.endbutton.place(x=200, y=350)        

        self.Pretop.mainloop()

class PostWorkout:
    def __init__(self):
    
        self.Notetop = tk.Toplevel()
        self.Notetop.geometry('500x500')
        self.Notetop.title('Session notes')

        self.SessionDate = tk.Label(self.Notetop, text="enter Date of session:",font=("Callabri",10))
        self.SessionDate.pack()
        self.SessionDate.place(x=100, y=70)
        #Entry date of session
        self.SessionDatentry = tk.Entry(self.Notetop)
        self.SessionDatentry.pack()
        self.SessionDatentry.place(x=250, y=70)

        def findates():
            fulllist = []
            uniqueDates = []
            try:
                ws = sh.worksheet(value)
            except:
                print('error')
            column_a = ws.col_values(1)
            for cell in column_a:
                cell = str(cell)
                fulllist.append(cell)
            for dates in fulllist:
                if dates not in uniqueDates:
                    uniqueDates.append(dates)
            findate = self.SessionDatentry.get()
            if findate in uniqueDates:
                self.scorename.config(state='normal')
                self.work1ent.config(state='normal')
                self.work2ent.config(state='normal')
                self.work3ent.config(state='normal')
                self.work4ent.config(state='normal')
                self.dbutton.config(state='normal')
                for stuff in uniqueDates:
                    uniqueDates.remove(stuff)
                for stuff in fulllist:
                    fulllist.remove(stuff)
                return findate
            else:
                print(uniqueDates)
                print('error')

        self.datebutton = tk.Button(self.Notetop, text='Enter', pady=3, padx=50, font=('Callabri', 12), fg='white', bg='blue',
                                    command=findates)        
        self.datebutton.pack()
        self.datebutton.place(x=160, y=110)

        #Enter NTscore(s) of session
        self.scoreLabel = tk.Label(self.Notetop, text="enter Neuro Tracker Score:",font=("Callabri",10))
        self.scoreLabel.pack()
        self.scoreLabel.place(x=80, y=170)
        #Entry for scores
        self.scorename = tk.Entry(self.Notetop, state='disabled')
        self.scorename.pack()
        self.scorename.place(x=250, y=170)        

        #Enter notes for workout 1
        self.wornote1 = tk.Label(self.Notetop, text="Enter notes of workout 1:", font=("Callabri",10))
        self.wornote1.pack()
        self.wornote1.place(x=80, y=230)
        #Entry for notes of workout
        self.work1ent = tk.Entry(self.Notetop, state='disabled')
        self.work1ent.pack()
        self.work1ent.place(x=250, y=230)

        #Enter notes for workout 2
        self.wornote2 = tk.Label(self.Notetop, text="Enter notes of workout 2:", font=("Callabri",10))
        self.wornote2.pack()
        self.wornote2.place(x=80, y=260)
        #Entry for notes of workout
        self.work2ent = tk.Entry(self.Notetop, state='disabled')
        self.work2ent.pack()
        self.work2ent.place(x=250, y=260)

        #Enter notes for workout 3
        self.wornote3 = tk.Label(self.Notetop, text="Enter notes of workout 3:", font=("Callabri",10))
        self.wornote3.pack()
        self.wornote3.place(x=80, y=290)
        #Entry for notes of workout
        self.work3ent = tk.Entry(self.Notetop, state='disabled')
        self.work3ent.pack()
        self.work3ent.place(x=250, y=290)

        #Enter notes for workout 4
        self.wornote4 = tk.Label(self.Notetop, text="Enter notes of workout 4:", font=("Callabri",10))
        self.wornote4.pack()
        self.wornote4.place(x=80, y=320)
        #Entry for notes of workout
        self.work4ent = tk.Entry(self.Notetop, state='disabled')
        self.work4ent.pack()
        self.work4ent.place(x=250, y=320)

        def Noted():
            notelist = []
            note1 = self.work1ent.get()
            note2 = self.work2ent.get()
            note3 = self.work3ent.get()
            note4 = self.work4ent.get()
            score = self.scorename.get()
            ws = sh.worksheet(value)
            ws.update('D2', note1)
            ws.update('D3', note2)
            ws.update('D4', note3)
            ws.update('D5', note4)
            ws.update('E2', score)
            messagebox.showinfo('Info Entered', 'session notes for ' + value + ' saved to databse')
            self.Notetop.destroy

        self.dbutton = tk.Button(self.Notetop, text='Enter Notes', pady=3, padx=50, font=('Callabri', 12), fg='white', bg='blue',
                                     state='disabled', command=Noted)        
        self.dbutton.pack()
        self.dbutton.place(x=160, y=350)


        self.Notetop.mainloop()

def AthleteMenu():
    Athletemenu()

#open new window to enter new athlete
def NewAthlete():
    NewAthleteMenu()

#open new window to search athlete and append new session info
def SearchAthlete():
    SearchMenu()

def PRELOAD():
    Preload()

def NOTES():
    PostWorkout()

MainMenu()