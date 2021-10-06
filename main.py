from tkinter import *
import tkinter.messagebox as tmsg
root = Tk()
root.geometry("450x450")
root.wm_title("gui voting system")
def lol():
    if scorea > scoreb:
        tmsg.showinfo("voting system","BJP has been win")
    if scoreb > scorea:
        tmsg.showinfo("voting system","Congress has been win")
    if scoreb == scorea or scorea == scoreb:
        tmsg.showinfo("voting system","BJP and Congress has been Tie")

list_of_voters_name = []
voted=[]
voted2 = False
voted3 = False




def login():
    global voted2,voted3
    entry_value = g.get()


    if entry_value in voted:
        tmsg.showinfo("voting system","you have already voted")
        score_lblu["text"] = f"{entry_value} has been alredy logined"
        o["stat"] = "disable"
        p["stat"] = "disable"
        voted2 = True
    else:
        voted2 = False



    if list_of_voters_name == []:
        voted.append(entry_value)
        if voted2 == False and voted3 == False:
            o["stat"] = "normal"
            p["stat"] = "normal"
            tmsg.showinfo("voting system",f"{entry_value} successfully login")





scorea = 0
def votea():
    global scorea
    scorea += 1
    score_lbl["text"] = f"BJP vote is {scorea}"
    o['stat'] = "disable"
    p['stat'] = "disable"
scoreb = 0
def voteb():
    global scoreb
    scoreb += 1
    scorea_lbl["text"] = f"Congress vote is {scoreb}"
    o['stat'] = "disable"
    p['stat'] = "disable"
Label(text="WELCOME TO OUR \nGUI VOTING SYSTEM",font="Consals 18 bold",bg="Gray").pack()
g = StringVar()
Entry(textvariable=g,width=40).pack()
Button(text="login",height=2,width=10,bg="blue",fg="white",command=login).pack(pady=10)
o=Button(text="vote BJP",width=30,bg="red",fg="white",stat="disable",command=votea)
o.pack(pady=20)
root.configure(bg="Gray")
p=Button(text="vote Congress",width=30,bg="red",fg="white",stat="disable",command=voteb)
p.pack(pady=10)
score_lblu = Label(text="",fg="red",bg="Gray")
score_lblu.pack()

score_lblj = Label(text="",fg="lime",bg="Gray")
score_lblj.pack()
score_lbl = Label(text="",bg="Gray")
score_lbl.pack()
scorea_lbl = Label(text="",bg="Gray")
scorea_lbl.pack()
Button(text="apply",command=lol,bg="black",fg="white").pack(pady=20)
root.mainloop()