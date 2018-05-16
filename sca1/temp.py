import Tkinter as tk 
win = tk.Tk()
win.title('Python Gui')

def clickme():
	action.configure(text='***put a name while_~***'+name.get(),state='disabled')
	
	#aLabel.configure(foreground='red')

#win.resizable(0,0)

aLabel = tk.Label(win,text='choose a number:')
aLabel.grid(column=1,row=0)

chVarDis = tk.IntVar()
check1 = tk.Checkbutton(win, text='Disabled',variable=chVarDis,state='disabled')
check1.select()
check1.grid(column=0,row=4,sticky=tk.W)

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(win,text='UnSelected',variable=chVarUn)
check2.deselect()
check2.grid(column=1,row=4,sticky=tk.W)

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(win,text='Enable',variable=chVarEn)
check3.select()
check3.grid(column=2,row=4,sticky=tk.W)


color = ['Blue','Gold','Red']
def radCall():
	radSel = radVar.get()
	if   radSel == 1: win.configure(background=color[0])
	elif radSel == 2: win.configure(background=color[1])
	elif radSel == 3: win.configure(background=color[2])

radVar = tk.IntVar()
radVar.set(99)
for i in range(3):


scrol_W = 30
scrol_H = 3

win.mainloop() 
aly_contrl-@)!*-GDXGM_2018