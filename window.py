import tkinter as tk
from tkinter import ttk
import requests
import json



class Window:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Values exchanger")
        self.root.geometry("850x500")
        self.initialize_currencies()
        self.create_layout()
        self.root.mainloop()
        

    def create_layout(self):
        ### Define grid ###
        self.frame = tk.Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        ### Labels ###
        self.z = tk.Label(self.frame, text="z", font=("Arial", 18))
        # z.pack()
        self.na = tk.Label(self.frame, text="na", font=("Arial", 18))
        # na.pack()

        ### Enties ###
        self.float_validator = self.root.register(self.validate_float)
        self.entry = tk.Entry(self.frame, validate="key", validatecommand=(self.float_validator, '%P'))

        self.resultText = tk.StringVar()
        self.result = tk.Entry(self.frame, textvariable=self.resultText)
        self.result['state'] = 'readonly'

        
        ### Buttons ###
        self.end = tk.Button(self.frame, text="Zakończ", font=('Arial', 12), command=self.root.destroy)
        self.btn = tk.Button(self.frame, text="Przelicz", font=('Arial', 12), command=self.count)


        ### list ###
        self.fromV = ttk.Combobox(self.frame, name="from", width=37)
        self.fromV['state'] = 'readonly'
        self.fromV['values'] = self.currencies

        self.toV = ttk.Combobox(self.frame, name="to", width=37)
        self.toV['state'] = 'readonly'
        self.toV['values'] = self.currencies

        ### Add event listener to combobox ###
        def comboChange(event):
            if str(event.widget)[-1] == "o":
                widget = self.fromV
            else:
                widget = self.toV
            id = self.currencies.index(event.widget.get())
            widget['values'] = self.currencies[:id] + self.currencies[id+1:]

        self.fromV.bind('<<ComboboxSelected>>', comboChange)
        self.toV.bind('<<ComboboxSelected>>', comboChange)


        ### Label for Table date ###
        self.labelDate = tk.Label(self.frame, textvariable=self.refreshDate, font=("Arial", 18))
        
        ### Place content on grid ###
        self.z.grid(row=1, column=0, pady=50, padx=10)
        self.na.grid(row=1, column=3, padx=10)
        self.fromV.grid(row=1, column=1)
        self.toV.grid(row=1, column=4)
        self.entry.grid(row=2, column=1, pady=50)
        self.result.grid(row=2, column=4)
        self.btn.grid(row=3, column=1, pady=50)
        self.end.grid(row=3, column=4)
        self.labelDate.grid(row=0, column=3)
        
        

        ### Place grid frame ###
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        

    def validate_float(self, value):
        if not value:
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def initialize_currencies(self):
        fileName = "currenciesData.json"
        URL = "http://api.nbp.pl/api/exchangerates/tables/A/"

        self.refreshDate = tk.StringVar()
        self.currencies = []

        try:
            r = requests.get(url = URL)

            if r.status_code == 200:
                data = r.json()[0]
                s = f"Tabela z dnia {data['effectiveDate']}"
                self.refreshDate.set(s)
                self.rates = data['rates']
                with open(fileName, 'w') as file:
                    file.write(json.dumps(data))
        except:
            try:
                with open(fileName) as file:
                    data = json.load(file)
                    s = f"Tabela z dnia {data['effectiveDate']}"
                    self.refreshDate.set(s)
                    self.rates = data['rates']
            except:
                print("There is not backup data, or it is damaged! Please connect to the internet!")
                return
        
        self.currenciesCounter = {}
        for rate in self.rates:
            self.currenciesCounter[rate['code']] = rate['mid']
            self.currencies.append(f"{rate['currency']}({rate['code']})")

        ### Add PLN
        self.currencies.append("polski złoty(PLN)")
        self.currenciesCounter["PLN"] = 1

    def count(self):
        ## get the currencies to change
        try:
            fromV = float(self.currenciesCounter[self.fromV.get()[-4:-1]])
            toV = float(self.currenciesCounter[self.toV.get()[-4:-1]])
            ## get the value to change
            val = float(self.entry.get()) ## we can change to float without error check, cause of validation
            
            ### Count
            self.resultText.set(str(val*fromV/toV))
        except:
            pass

