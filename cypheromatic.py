# Keaton Clause 30 Nov 2020

import tkinter as tk

UncodedM = ''
CodedM = ''
a = 1
b = 1
modby = 26

def Encode():
	a = int(e3.get().strip('"'))
	b = int(e4.get().strip('"'))
	UncodedM = e1.get()
	CodedM = ''
	
	print('C = ' + str(a) + "P + " + str(b) + " mod( " + str(modby) + " )" )
	# send to window dialog
	
	
	c_i = []
	u_i = []
	
	for c in UncodedM:
		u_i.append( ord(c)-97 )
		
	print(UncodedM)
	print(u_i)
	
	for i in u_i:
		i *= a
		i += b
		i = i % modby
		c_i.append(i)
		
	for ec in c_i:
		CodedM += str(chr(ec+97))
		
	print(c_i)
	print(CodedM)
	e2.delete(0, 100)
	e2.insert(1,CodedM)
	
def Decode():
	a = int(e3.get().strip('"'))
	b = int(e4.get().strip('"'))
	CodedM = e2.get()
	UncodedM = ''
	
	print('C = ' + str(a) + "P + " + str(b) + " mod(26)" )
	
	c_i = []
	u_i = []
	coderef = []
	
	j = 0
	for i in range(0,modby):
		temp = (j*a + b) % modby
		coderef.append(temp)
		j += 1
	
	for c in CodedM:
		c_i.append( ord(c)-97 )
		
	print(CodedM)
	print(c_i)
	
	for c in c_i:
		indx = coderef.index(c)
		u_i.append(indx)
		
	for dc in u_i:
		UncodedM += str(chr(dc+97))
		
	print(u_i)
	print(UncodedM)
	e1.delete(0,100)
	e1.insert(1,UncodedM)

#GUI
window = tk.Tk()
window.title('CypherOMatic')

#Labels/Entry
#formulaLabel = tk.Label(window, text = "a : ").grid(row = 12)

tk.Label(window, text = "a : ").grid(row = 0)
e3 = tk.Entry(window)
e3.insert(0, str(a))
e3.grid(row = 0, column = 1)

tk.Label(window, text = "b : ").grid(row = 1)
e4 = tk.Entry(window)
e4.insert(0, str(b))
e4.grid(row = 1, column = 1)

tk.Label(window, text = "mod : ").grid(row = 2)
e5 = tk.Entry(window)
e5.insert(0, str(modby))
e5.grid(row = 2, column = 1)

tk.Label(window, text = "Uncoded Message: ").grid(row = 3)
e1 = tk.Entry(window)
e1.insert(0, UncodedM)
e1.grid(row = 3, column = 1)

tk.Label(window, text = "Coded Message: ").grid(row = 4)
e2 = tk.Entry(window)
e2.insert(0, CodedM)
e2.grid(row = 4, column = 1)

#buttons
btn1 = tk.Button(window, text='ENCODE', command= lambda: Encode())
btn1.grid(row = 7)

btn2 = tk.Button(window, text="DECODE", command= lambda: Decode())
btn2.grid(row = 7, column = 1)
#btn3 = tk.Button(window, text='Find AllTestFiles', command= lambda: findDir(filesPath, e1))
#btn3.grid(row = 6)
#btn4 = tk.Button(window, text='Find Playlist File', command= lambda: findFile(playPath, e2))
#btn4.grid(row = 6, column = 1)

window.mainloop()
