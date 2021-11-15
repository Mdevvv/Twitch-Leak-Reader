#coding:utf-8

from tkinter.font import Font
from tkinter import *
from pandas import read_csv
import requests
import json

class Window:
    """inface graphique de l'utilisateur"""

    def __init__(self):
        root = Tk()

        # info écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        windowWidth = int(screen_width/2)
        windowHeight = int(screen_height/2)

        #parametre de base
        geometry = str(windowWidth) + "x" + str(windowHeight) + "+" + str(int((screen_width-windowWidth)/2)) + "+" + str(int((screen_height-windowHeight)/2))
        root.geometry(geometry)
        root.resizable(False, False)
        root.title("Twitch Leak Reader")
        root.iconbitmap("favicon.ico")
        rootBackground = '#18181B'
        purpleColor = '#a970ff'
        root.configure(background=rootBackground)


        #widget titre
        titre_Font = Font(family="Arial", size=int(round(windowWidth/20)))
        titre = Label(root, 
            text="Twitch Leaked Reader", 
            bg=rootBackground,
            font=titre_Font, 
            fg=purpleColor,  
            pady=int(round(windowWidth/10))
        )


        #widget entry du username
        userEntryFont =  Font(family="Arial", size=int(round(windowWidth/45)))
        userEntryVar = StringVar()
        userEntry = Entry(root,
            bg="black", 
            relief = "solid",
            width=int(round(windowWidth/25)),
            textvariable=userEntryVar,
            fg = "white", 
            font=userEntryFont,
            selectbackground = purpleColor,
            insertbackground = "white",

        )
        userEntry.insert(0,"user name")


        #button cliqué
        def sumbit():
            id = ApiTwitch(userEntryVar.get()).get()
            loadingVar.set("")
            
            if id == None :
                loadingVar.set("Invalid User Name")
                return None
            

            ResultWindow(ReaderTotal(id).get(), userEntryVar.get(), rootBackground, purpleColor)

        
        #widget bouton go
        submitButtonFont =  Font(family="Arial", size=int(round(windowWidth/45)))
        submitButton = Button(root,
            text = "submit",
            bg = purpleColor,
            fg = "white",
            font = submitButtonFont,
            activeforeground = "white",
            activebackground = "black",
            relief = "flat",
            command = sumbit,
        )

        
        #widget chargement
        loadingFont = Font(family="Arial", size=int(round(windowWidth/45)))
        loadingVar = StringVar()
        
        loading = Label(
            root,
            textvariable = loadingVar,
            fg = purpleColor,
            bg = rootBackground,
            font = loadingFont,
            pady=int(round(windowWidth/80))
        )

        
        #packing
        titre.pack()
        userEntry.pack()
        loading.pack()
        submitButton.pack(pady=int(round(windowWidth/15)))

        #mainloop
        root.mainloop()
    



class ReaderTotal:
    """lis le montant total depuis l'id"""

    def __init__(self, id):
        self._sum = 0.00
        self._loading = "0 %"
        self._id = id
        self._allFiles = 27

        #vérifie s'il n'a pas déjà été chercher
        data = read_csv("already_done.csv")
        data = data.set_index('user_id')
        if self._id in data.index : # vérifié si le user id exist dans ce csv
            print("find with already_done.csv file")
            self._sum = data.loc[self._id].sum()
        
        else :
            print("\n Please wait:")
            for i in range(self._allFiles):
                data = read_csv("decompressed_files/revenues" + str(i) + ".csv") # recupere le read_csv
                data = data.drop([ 'payout_entity_id', 'report_date'], axis=1) # enleve des colones inutile
                data = data.set_index('user_id') # transforme les indexs par les user_id 

                if self._id in data.index : # vérifié si le user id exist dans ce csv
                    self._sum += round(data.loc[self._id].sum(),2) # faire une somme et arrondir a 10^(-2) près

                self._loading = round(i/self._allFiles*100)
                print("",str(self._loading),"%")

            with open('already_done.csv', 'a', newline='') as f_object:  
                # Pass the CSV  file object to the writer() function
                writer_object = writer(f_object)
                # Result - a writer object
                # Pass the data in the list as an argument into the writerow() function
                writer_object.writerow([self._id, round(self._sum,2)])
                # Close the file object
    def get(self):
        return round(self._sum,2)
    
    def loading(self):
        return self._loading

class ResultWindow:
    """affiche le resultat dans une nouvelle fenetre tkinter"""

    def __init__(self, sum, username, Background_Color, Second_Color):
        self._root = Tk()

        #default settings
        self._root.resizable(False, False)
        self._root.configure(background=Background_Color)
        self._root.title("Result")
        self._root.iconbitmap("favicon.ico")
        self._rootBackground = '#18181B'

        #label pseudo du gars
        label_username = Label(self._root,
            text=str(username) + " :",
            bg=Background_Color,
            fg=Second_Color,
            font = ("Arial", 28),
            pady=20,
            padx=20,
        )
        
        #label de resultat
        label_result = Label(self._root, 
            text=(str(sum) + " $"),
            bg=Background_Color,
            fg="white",
            font = ("Arial", 40),
            pady=10,
            padx=10
        )
        label_username.pack()
        label_result.pack()

        print("\n"+ " -> " +str(username) + " :",(str(sum) + " $"),"\n")
        self._root.mainloop()

class ApiTwitch:
    """permet de récupérer l'id avec user name twitch"""

    def __init__(self, username) :

        self._id = None

        url=('https://api.twitch.tv/kraken/users?login='+ username)

        head = {"Accept": "application/vnd.twitchtv.v5+json", "Client-ID" : "abe7gtyxbr7wfcdftwyi9i5kej3jnq"} # en-tete de la requete
        r = requests.get(url, headers=head) #récupérer le profile de l'utilisateur 

        anser = json.loads(r.text) #transformation du json en dico

        if ("_total" in anser):
            if anser["_total"] != 0:
                self._id = int(anser['users'][0]['_id']) #recupération de l'id

        else :
            self._id = None

    def get(self):
        return self._id

Window()
