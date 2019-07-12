#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.8.6
# In conjunction with Tcl version 8.6
#    Jan 17, 2017 02:44:03 AM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import pygrid_support
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = New_Toplevel_1 (root)
    pygrid_support.init(root, top)
    
    #hate to put this here but....
    #handle args only first arg is used will load
    if(len(sys.argv)>1):
        filename=str(sys.argv[1])
        if filename[-3:]=='nei':
            root.after(100, pygrid_support.neifile(filename,True))
        if filename[-3:]=='seg':
            root.after(100, pygrid_support.segfile(filename,True))
        if filename[-3:]=='llz' or filename[-3:]=='xyz':
            root.after(100, pygrid_support.llzfile(filename,True))
        if filename[-3:]=='yxz':
            root.after(100, pygrid_support.llzfile(filename,True,True))
        if filename[-2:]=='ll':
            root.after(100, pygrid_support.nodfile(filename,True))
        if filename[-3:]=='dat':
            root.after(100, pygrid_support.llzfile(filename,True))
        root.after(100, pygrid_support.set_initdir(filename[:filename.rfind('/')]))
    else:
        root.after(100, pygrid_support.set_initdir('.'))
    root.mainloop()

w = None
def create_New_Toplevel_1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = New_Toplevel_1 (w)
    pygrid_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class New_Toplevel_1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        self._fgcolor = '#000000'  # X11 color: 'black'
        self._compcolor = '#d9d9d9' # X11 color: 'gray85'
        self._ana1color = '#d9d9d9' # X11 color: 'gray85' 
        self._ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=self._bgcolor)
        self.style.configure('.',foreground=self._fgcolor)
        self.style.map('.',background=
            [('selected', self._compcolor), ('active',self._ana2color)])

        top.geometry("1026x675+477+155")
        top.title("Pygrid")
        top.configure(highlightcolor="black")

        self.TSizegrip1 = ttk.Sizegrip(top)
        self.TSizegrip1.place(anchor=SE, relx=1.0, rely=1.0)

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.0, rely=0.06, relheight=0.94, relwidth=0.78)
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief=GROOVE)
        self.Frame1.configure(width=805)

        self.figure = Figure(dpi=50)
        self.Canvas1 = FigureCanvasTkAgg(self.figure, master=self.Frame1)
        self.Canvas1.get_tk_widget().pack(side=TOP, fill="both", expand=1)
        #self.Canvas1.place(relx=0.01, rely=0.06, relheight=0.85, relwidth=0.97)
        #self.Canvas1.configure(background="white")
        #self.Canvas1.configure(borderwidth="2")
        #self.Canvas1.configure(relief=RIDGE)
        #self.Canvas1.configure(selectbackground="#c4c4c4")
        #self.Canvas1.configure(width=784)
        

        self.ax = self.figure.add_axes([.05,.05,.80,.9]) 
        self.ax.axis([-180, 180, -90, 90])
        self.cax = self.figure.add_axes([.05+.8+0.025,.05,.025,.9])
        self.cax.set_visible(False)
        #self.Canvas1.show()
        self.toolbar = NavigationToolbar2TkAgg( self.Canvas1, self.Frame1 )
        #self.toolbar.pack(side=Tk.BOTTOM)

        self.menubar = Menu(top,bg=self._bgcolor,fg=self._fgcolor)
        top.configure(menu = self.menubar)
        
        self.file = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.file,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="File")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.TODO,
                foreground="#000000",
                label="New")
        self.file.add_separator(
                background="#d9d9d9")
        self.file.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.TODO,
                foreground="#000000",
                label="Exit")
        self.save = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.save,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Save")
        self.save.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.save_segfile,
                foreground="#000000",
                label="Save segfile")
        self.save.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.save_neifile,
                foreground="#000000",
                label="Save neifile")
        self.save.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.save_nodfile,
                foreground="#000000",
                label="Save nodfile")
        self.save.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.save_nod2polyfile,
                foreground="#000000",
                label="Save nod2poly file")
        self.save.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.save_llzfile,
                foreground="#000000",
                label="Save llzfile")
        self.load = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.load,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Load")
        self.load.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.load_coastline,
                foreground="#000000",
                label="Load coastline")
        self.load.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.load_segfile,
                foreground="#000000",
                label="Load segfile")
        self.load.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.load_neifile,
                foreground="#000000",
                label="Load neifile")
        self.load.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.load_nodfile,
                foreground="#000000",
                label="Load nodfile")
        self.load.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.load_llzfile,
                foreground="#000000",
                label="Load llzfile")
        self.help = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.help,
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#d9d9d9",
                foreground="#000000",
                label="Help")
        self.help.add_command(
                activebackground="#d8d8d8",
                activeforeground="#000000",
                background="#d9d9d9",
                command=pygrid_support.TODO,
                foreground="#000000",
                label="About")
                

             
        ########################################################################
        #
        #   Checkboxes
        #
        ########################################################################    
                
                
        self.Frame3 = Frame(top)
        self.Frame3.place(relx=0.0, rely=0.0, relheight=0.07, relwidth=0.78)
        self.Frame3.configure(relief=GROOVE)
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief=GROOVE)
        self.Frame3.configure(width=805)

        self.types=['coast','seg','nei','nod','llz','neic']
        self.CBVar={}
        for typ in self.types:
            self.CBVar[typ]=IntVar()

        self.Checkbutton1 = Checkbutton(self.Frame3)
        self.Checkbutton1.place(relx=0.01, rely=0.04, relheight=0.91, relwidth=0.15)
        self.Checkbutton1.configure(activebackground="#d9d9d9")
        self.Checkbutton1.configure(text='''Show coastline''')
        self.Checkbutton1.configure(width=72)        
        self.Checkbutton1.configure(command=pygrid_support.toggle_coastline)
        self.Checkbutton1.configure(variable=self.CBVar['coast'])

        self.Checkbutton2 = Checkbutton(self.Frame3)
        self.Checkbutton2.place(relx=0.16, rely=0.04, relheight=0.91, relwidth=0.15)
        self.Checkbutton2.configure(activebackground="#d9d9d9")
        self.Checkbutton2.configure(justify=LEFT)
        self.Checkbutton2.configure(text='''Show Segfile''')
        self.Checkbutton2.configure(width=82)
        self.Checkbutton2.configure(command=pygrid_support.toggle_segfile)
        self.Checkbutton2.configure(variable=self.CBVar['seg'])

        self.Checkbutton3 = Checkbutton(self.Frame3)
        self.Checkbutton3.place(relx=0.31, rely=0.04, relheight=0.91, relwidth=0.12)
        self.Checkbutton3.configure(activebackground="#d9d9d9")
        self.Checkbutton3.configure(justify=LEFT)
        self.Checkbutton3.configure(text='''Show Neifile''')
        self.Checkbutton3.configure(command=pygrid_support.toggle_neifile)
        self.Checkbutton3.configure(variable=self.CBVar['nei'])

        self.Checkbutton4 = Checkbutton(self.Frame3)
        self.Checkbutton4.place(relx=0.43, rely=0.04, relheight=0.91, relwidth=0.14)
        self.Checkbutton4.configure(activebackground="#d9d9d9")
        self.Checkbutton4.configure(justify=LEFT)
        self.Checkbutton4.configure(text='''Show Nodfile''')
        self.Checkbutton4.configure(command=pygrid_support.toggle_nodfile)
        self.Checkbutton4.configure(variable=self.CBVar['nod'])

        self.Checkbutton5 = Checkbutton(self.Frame3)
        self.Checkbutton5.place(relx=0.57, rely=0.04, relheight=0.91, relwidth=0.12)
        self.Checkbutton5.configure(activebackground="#d9d9d9")
        self.Checkbutton5.configure(justify=LEFT)
        self.Checkbutton5.configure(text='''Show llzfile''')
        self.Checkbutton5.configure(command=pygrid_support.toggle_llzfile)
        self.Checkbutton5.configure(variable=self.CBVar['llz'])
        
        self.Checkbutton6 = Checkbutton(self.Frame3)
        self.Checkbutton6.place(relx=0.70, rely=0.04, relheight=0.91, relwidth=0.15)
        self.Checkbutton6.configure(activebackground="#d9d9d9")
        self.Checkbutton6.configure(justify=LEFT)
        self.Checkbutton6.configure(text='''Show nei color''')
        self.Checkbutton6.configure(command=pygrid_support.toggle_neifilecolor)
        self.Checkbutton6.configure(variable=self.CBVar['neic'])
        
        self.NeiMenuVar = StringVar(root)
        self.NeiChoices={'Depth','dhh','Sidelength'}
        self.NeiMenuVar.set('Depth')
        self.NeiMenu = OptionMenu(self.Frame3,self.NeiMenuVar,*self.NeiChoices)
        self.NeiMenu.place(relx=0.850, rely=0.04, relheight=0.91, relwidth=0.15)
        self.NeiMenuVar.trace('w', pygrid_support.change_neimenu)

        ########################################################################
        #
        #   Make notebook
        #
        ######################################################################

        self.nb = ttk.Notebook(top)        
        
        self.Frame2 = Frame(self.nb)
        self.Frame2.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(width=215)
        
        self.Frame5 = Frame(self.nb)
        self.Frame5.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame5.configure(relief=GROOVE)
        self.Frame5.configure(borderwidth="2")
        self.Frame5.configure(relief=GROOVE)
        self.Frame5.configure(width=215)
        
        self.Frame6 = Frame(self.nb)
        self.Frame6.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame6.configure(relief=GROOVE)
        self.Frame6.configure(borderwidth="2")
        self.Frame6.configure(relief=GROOVE)
        self.Frame6.configure(width=215)
        
        
        
        self.nb.add(self.Frame2, text='Nodes')
        self.nb.add(self.Frame5, text='Depth')
        self.nb.add(self.Frame6, text='Seg')

        self.nb.place(relx=0.78, rely=0, relheight=0.75, relwidth=0.22)
        
        
        
        rh = 0.055
        rw = 0.85
        rw2 = 0.4        
        sh = 0.06
        
        ########################################################################
        #
        #   Node Tab
        #
        ########################################################################

        ry = 0.01

        self.Label1 = Label(self.Frame2)
        self.Label1.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw2)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Set resolution''')

        self.Entry1 = Entry(self.Frame2)
        self.Entry1.place(relx=0.525, rely=ry, relheight=rh, relwidth=rw2)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        ry += sh
        self.Button3 = Button(self.Frame2)
        self.Button3.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(text='''Spray Area''')
        self.Button3.configure(command=pygrid_support.spray_area)
        
        ry += sh
        self.Button4 = Button(self.Frame2)
        self.Button4.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(text='''Remove Area''')
        self.Button4.configure(command=pygrid_support.remove_area)
        
        ry += sh
        self.Button4 = Button(self.Frame2)
        self.Button4.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(text='''Remove Area (llz)''')
        self.Button4.configure(command=pygrid_support.remove_area_llz)

        ry += sh
        # self.Button5 = Button(self.Frame2)
        # self.Button5.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw2)
        # self.Button5.configure(activebackground="#d9d9d9")
        # self.Button5.configure(text='''Select Seg''')
        # self.Button5.configure(command=pygrid_support.select_seg)
        
        # self.Entry2 = Entry(self.Frame2)
        # self.Entry2.place(relx=0.525, rely=ry, relheight=rh, relwidth=rw2)
        # self.Entry2.configure(background="white")
        # self.Entry2.configure(font="TkFixedFont")
        # self.Entry2.configure(selectbackground="#c4c4c4")
        
        ry += sh
        self.Button6 = Button(self.Frame2)
        self.Button6.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(text='''Remove nodes inside seg''')
        self.Button6.configure(command=pygrid_support.remove_nodeseg_in)
        
        ry += sh
        self.Button7 = Button(self.Frame2)
        self.Button7.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button7.configure(activebackground="#d9d9d9")
        self.Button7.configure(text='''Remove nodes outside seg''')
        self.Button7.configure(command=pygrid_support.remove_nodeseg_out)

        ry += sh
        self.Button8 = Button(self.Frame2)
        self.Button8.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button8.configure(activebackground="#d9d9d9")
        self.Button8.configure(text='''Extract nod from nei''')
        self.Button8.configure(command=pygrid_support.extract_nod)
        
        ry += sh
        self.Button9 = Button(self.Frame2)
        self.Button9.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button9.configure(activebackground="#d9d9d9")
        self.Button9.configure(text='''Extract seg from nei''')
        self.Button9.configure(command=pygrid_support.extract_seg)
        
        ry += sh
        self.Button10 = Button(self.Frame2)
        self.Button10.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button10.configure(activebackground="#d9d9d9")
        self.Button10.configure(text='''Extract llz from nei''')
        self.Button10.configure(command=pygrid_support.extract_llz)
        
        #ry += sh
        #self.Button9 = Button(self.Frame2)
        #self.Button9.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        #self.Button9.configure(activebackground="#d9d9d9")
        #self.Button9.configure(text='''Remove area and seg''')
        #self.Button9.configure(command=pygrid_support.removeandseg)
        
        
        ########################################################################
        #
        #   Depth tab
        #
        ########################################################################
        
        ry = 0.01
        
        self.Labelmin = Label(self.Frame5)
        self.Labelmin.place(relx=0.1, rely=ry, relheight=rh, relwidth=.2)
        self.Labelmin.configure(activebackground="#f9f9f9")
        self.Labelmin.configure(text='''Min''')
        
        self.Labelmax = Label(self.Frame5)
        self.Labelmax.place(relx=0.375, rely=ry, relheight=rh, relwidth=.2)
        self.Labelmax.configure(activebackground="#f9f9f9")
        self.Labelmax.configure(text='''Max''')
        
        self.Labelmean = Label(self.Frame5)
        self.Labelmean.place(relx=0.66, rely=ry, relheight=rh, relwidth=.2)
        self.Labelmean.configure(activebackground="#f9f9f9")
        self.Labelmean.configure(text='''Mean''')  
        
        ry += sh
        
        self.Labelsmin = Label(self.Frame5)
        self.Labelsmin.place(relx=0.1, rely=ry, relheight=rh, relwidth=.2)
        self.Labelsmin.configure(activebackground="#f9f9f9")
        self.Labelsmin.configure(text='''na''')
        
        self.Labelsmax = Label(self.Frame5)
        self.Labelsmax.place(relx=0.375, rely=ry, relheight=rh, relwidth=.2)
        self.Labelsmax.configure(activebackground="#f9f9f9")
        self.Labelsmax.configure(text='''na''')
        
        self.Labelsmean = Label(self.Frame5)
        self.Labelsmean.place(relx=0.66, rely=ry, relheight=rh, relwidth=.2)
        self.Labelsmean.configure(activebackground="#f9f9f9")
        self.Labelsmean.configure(text='''na''')   
        
        self.Button10 = Button(self.Frame5)
        self.Button10.place(relx=0.075, rely=ry+0.05, relheight=rh, relwidth=rw)
        self.Button10.configure(activebackground="#d9d9d9")
        self.Button10.configure(text='''Calc Stats''')
        self.Button10.configure(command=pygrid_support.calc_stats)     

        ry += 2*sh
        
        self.Label3 = Label(self.Frame5)
        self.Label3.place(relx=0.5, rely=ry, relheight=rh, relwidth=rw2)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(text='''Set depth''')
        
        self.Button10 = Button(self.Frame5)
        self.Button10.place(relx=0.075, rely=ry+0.05, relheight=rh, relwidth=rw2)
        self.Button10.configure(activebackground="#d9d9d9")
        self.Button10.configure(text='''Set depth''')
        self.Button10.configure(command=pygrid_support.set_depth)
        
        self.Entry3 = Entry(self.Frame5)
        self.Entry3.place(relx=0.525, rely=ry+0.05, relheight=rh, relwidth=rw2)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(selectbackground="#c4c4c4")
        
        ry += 2*sh
        self.Label4 = Label(self.Frame5)
        self.Label4.place(relx=0.5, rely=ry, relheight=rh, relwidth=rw2)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''Avg. depth''')
        
        self.Button11 = Button(self.Frame5)
        self.Button11.place(relx=0.075, rely=ry+0.05, relheight=rh, relwidth=rw2)
        self.Button11.configure(activebackground="#d9d9d9")
        self.Button11.configure(text='''Avg. depth''')
        self.Button11.configure(command=pygrid_support.avg_depth)
        
        self.Entry4 = Entry(self.Frame5)
        self.Entry4.place(relx=0.525, rely=ry+0.05, relheight=rh, relwidth=rw2)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(selectbackground="#c4c4c4")
        
        ry += 2*sh
        self.Labelmin2 = Label(self.Frame5)
        self.Labelmin2.place(relx=0.275, rely=ry, relheight=rh, relwidth=.3)
        self.Labelmin2.configure(activebackground="#f9f9f9")
        self.Labelmin2.configure(text='''Limit Min''')
        
        self.Labelmax2 = Label(self.Frame5)
        self.Labelmax2.place(relx=0.625, rely=ry, relheight=rh, relwidth=.3)
        self.Labelmax2.configure(activebackground="#f9f9f9")
        self.Labelmax2.configure(text='''Limit Max''')
        
        ry += sh
        self.Labeldepth = Label(self.Frame5)
        self.Labeldepth.place(relx=0.05, rely=ry, relheight=rh, relwidth=.2)
        self.Labeldepth.configure(activebackground="#f9f9f9")
        self.Labeldepth.configure(text='''Depth''')
    
        self.Entryhmin = Entry(self.Frame5)
        self.Entryhmin.place(relx=0.275, rely=ry, relheight=rh, relwidth=rw2*.75)
        self.Entryhmin.configure(background="white")
        self.Entryhmin.configure(font="TkFixedFont")
        self.Entryhmin.configure(selectbackground="#c4c4c4")
        
        self.Entryhmax = Entry(self.Frame5)
        self.Entryhmax.place(relx=0.625, rely=ry, relheight=rh, relwidth=rw2*.75)
        self.Entryhmax.configure(background="white")
        self.Entryhmax.configure(font="TkFixedFont")
        self.Entryhmax.configure(selectbackground="#c4c4c4")
    
        ry += sh
        self.Labeldhh = Label(self.Frame5)
        self.Labeldhh.place(relx=0.05, rely=ry, relheight=rh, relwidth=.2)
        self.Labeldhh.configure(activebackground="#f9f9f9")
        self.Labeldhh.configure(text='''dhh''')
        
        self.Entrydhhmin = Entry(self.Frame5)
        self.Entrydhhmin.place(relx=0.275, rely=ry, relheight=rh, relwidth=rw2*.75)
        self.Entrydhhmin.configure(background="white")
        self.Entrydhhmin.configure(font="TkFixedFont")
        self.Entrydhhmin.configure(selectbackground="#c4c4c4")
        
        self.Entrydhhmax = Entry(self.Frame5)
        self.Entrydhhmax.place(relx=0.625, rely=ry, relheight=rh, relwidth=rw2*.75)
        self.Entrydhhmax.configure(background="white")
        self.Entrydhhmax.configure(font="TkFixedFont")
        self.Entrydhhmax.configure(selectbackground="#c4c4c4")
        
        
        ry += sh
        self.Button12 = Button(self.Frame5)
        self.Button12.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button12.configure(activebackground="#d9d9d9")
        self.Button12.configure(text='''Smooth''')
        self.Button12.configure(command=pygrid_support.smooth)
        
        
        
        ########################################################################
        #
        #   Seg Tab
        #
        ########################################################################

        ry = 0.01        
        self.Button5 = Button(self.Frame6)
        self.Button5.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw2)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(text='''Select Seg''')
        self.Button5.configure(command=pygrid_support.select_seg)
        
        self.Entry2 = Entry(self.Frame6)
        self.Entry2.place(relx=0.525, rely=ry, relheight=rh, relwidth=rw2)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")

        ry += sh
        self.Button13 = Button(self.Frame6)
        self.Button13.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button13.configure(activebackground="#d9d9d9")
        self.Button13.configure(text='''Create Seg''')
        self.Button13.configure(command=pygrid_support.create_seg)
        
        ry += sh
        self.Button14 = Button(self.Frame6)
        self.Button14.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        self.Button14.configure(activebackground="#d9d9d9")
        self.Button14.configure(text='''Delete Seg''')
        self.Button14.configure(command=pygrid_support.TODO)#select_seg)
        
        # ry += sh
        # self.Button4 = Button(self.Frame2)
        # self.Button4.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button4.configure(activebackground="#d9d9d9")
        # self.Button4.configure(text='''Remove Area''')
        # self.Button4.configure(command=pygrid_support.remove_area)
        
        # ry += sh
        # self.Button4 = Button(self.Frame2)
        # self.Button4.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button4.configure(activebackground="#d9d9d9")
        # self.Button4.configure(text='''Remove Area (llz)''')
        # self.Button4.configure(command=pygrid_support.remove_area_llz)

        # ry += sh
        # self.Button5 = Button(self.Frame2)
        # self.Button5.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw2)
        # self.Button5.configure(activebackground="#d9d9d9")
        # self.Button5.configure(text='''Select Seg''')
        # self.Button5.configure(command=pygrid_support.select_seg)
        
        # self.Entry2 = Entry(self.Frame2)
        # self.Entry2.place(relx=0.525, rely=ry, relheight=rh, relwidth=rw2)
        # self.Entry2.configure(background="white")
        # self.Entry2.configure(font="TkFixedFont")
        # self.Entry2.configure(selectbackground="#c4c4c4")
        
        # ry += sh
        # self.Button6 = Button(self.Frame2)
        # self.Button6.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button6.configure(activebackground="#d9d9d9")
        # self.Button6.configure(text='''Remove nodes inside seg''')
        # self.Button6.configure(command=pygrid_support.remove_nodeseg_in)
        
        # ry += sh
        # self.Button7 = Button(self.Frame2)
        # self.Button7.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button7.configure(activebackground="#d9d9d9")
        # self.Button7.configure(text='''Remove nodes outside seg''')
        # self.Button7.configure(command=pygrid_support.remove_nodeseg_out)

        # ry += sh
        # self.Button8 = Button(self.Frame2)
        # self.Button8.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button8.configure(activebackground="#d9d9d9")
        # self.Button8.configure(text='''Extract nod from nei''')
        # self.Button8.configure(command=pygrid_support.extract_nod)
        
        # ry += sh
        # self.Button9 = Button(self.Frame2)
        # self.Button9.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button9.configure(activebackground="#d9d9d9")
        # self.Button9.configure(text='''Extract seg from nei''')
        # self.Button9.configure(command=pygrid_support.extract_seg)
        
        # ry += sh
        # self.Button10 = Button(self.Frame2)
        # self.Button10.place(relx=0.075, rely=ry, relheight=rh, relwidth=rw)
        # self.Button10.configure(activebackground="#d9d9d9")
        # self.Button10.configure(text='''Extract llz from nei''')
        # self.Button10.configure(command=pygrid_support.extract_llz)
        
        

        
        ########################################################################
        #
        #   Selection controls
        #
        ########################################################################
        
        self.FrameSelection = Frame(top)
        self.FrameSelection.place(relx=0.78, rely=0.75, relheight=.1, relwidth=0.22)
        self.FrameSelection.configure(relief=GROOVE)
        self.FrameSelection.configure(borderwidth="2")
        self.FrameSelection.configure(relief=GROOVE)
        self.FrameSelection.configure(width=215)
        
        self.Button1 = Button(self.FrameSelection)
        self.Button1.place(relx=0.05, rely=0.075, relheight=0.4, relwidth=rw)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(text='''Clear Selection''')
        self.Button1.configure(command=pygrid_support.clear_selection)
        
        self.Button2 = Button(self.FrameSelection)
        self.Button2.place(relx=0.05, rely=0.525, relheight=0.4, relwidth=rw)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(text='''Select Area''')
        self.Button2.configure(command=pygrid_support.select_area)
        
        ########################################################################
        #
        #   Colorbar controls
        #
        ########################################################################
        
        self.Frame4 = Frame(top)
        self.Frame4.place(relx=0.78, rely=0.85, relheight=.15, relwidth=0.22)
        self.Frame4.configure(relief=GROOVE)
        self.Frame4.configure(borderwidth="2")
        self.Frame4.configure(relief=GROOVE)
        self.Frame4.configure(width=215)
        
        self.Label41 = Label(self.Frame4)
        self.Label41.place(relx=0.05, rely=0.03, relheight=0.255, relwidth=rw2)
        self.Label41.configure(activebackground="#f9f9f9")
        self.Label41.configure(text='''Max''')
        
        self.Entry41 = Entry(self.Frame4)
        self.Entry41.place(relx=0.525, rely=0.03, relheight=0.255, relwidth=rw2)
        self.Entry41.configure(background="white")
        self.Entry41.configure(font="TkFixedFont")
        self.Entry41.configure(selectbackground="#c4c4c4")
        
        self.Label42 = Label(self.Frame4)
        self.Label42.place(relx=0.05, rely=0.33, relheight=0.255, relwidth=rw2)
        self.Label42.configure(activebackground="#f9f9f9")
        self.Label42.configure(text='''Min''')
        
        self.Entry42 = Entry(self.Frame4)
        self.Entry42.place(relx=0.525, rely=0.33, relheight=0.255, relwidth=rw2)
        self.Entry42.configure(background="white")
        self.Entry42.configure(font="TkFixedFont")
        self.Entry42.configure(selectbackground="#c4c4c4")
        
        self.Button40 = Button(self.Frame4)
        self.Button40.place(relx=0.075, rely=0.66, relheight=0.255, relwidth=rw2)
        self.Button40.configure(activebackground="#d9d9d9")
        self.Button40.configure(text='''Redraw llz''')
        self.Button40.configure(command=pygrid_support.redraw_llz)
        
        self.Button40 = Button(self.Frame4)
        self.Button40.place(relx=0.525, rely=0.66, relheight=0.255, relwidth=rw2)
        self.Button40.configure(activebackground="#d9d9d9")
        self.Button40.configure(text='''Redraw nei''')
        self.Button40.configure(command=pygrid_support.redraw_nei)


if __name__ == '__main__':
    vp_start_gui()
    







