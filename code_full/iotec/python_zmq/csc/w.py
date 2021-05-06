import Tkinter as tk
import tkMessageBox

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.button = tk.Button(self, text="Create new window", 
                                command=self.create_window)
        self.button.pack(side="top")


    
    def create_window(self):
    

        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)

        def show():
          tkMessageBox.showinfo("FitoSmart - sendData", e1.get())
        #  print("hola" + e1.get());
    
        #l = tk.Label(t, text="This is window #%s" % self.counter)
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
        #l = tk.Button(t, text="Ok")
        #l.pack(side="bottom", fill="both", expand=True, padx=100, pady=100)
        l = tk.Label(t, text="First Name").grid(row=0)
        l = tk.Label(t, text="Last Name").grid(row=1)

        e1 = tk.Entry(t)
        e2 = tk.Entry(t)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)

        l = tk.Button(t, text='Quit', command=t.quit).grid(row=3, column=0, sticky="w", pady=4)
        l = tk.Button(t, text='Show', command=show).grid(row=3, column=1, sticky="w", pady=4)

if __name__ == "__main__":
    root = tk.Tk()
    main = MainWindow(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
