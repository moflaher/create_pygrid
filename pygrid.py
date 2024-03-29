#! /usr/bin/env python3
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
import options
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 10000
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as NT2tk
except ImportError:
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as NT2tk


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
            
        #init options and load .config file    
        self.config=options.defaultConfig()
        options.loadConfig(self.config)    

        top.geometry("1026x675+477+155")
        top.title("Pygrid")
        top.configure(highlightcolor="black")

        self.TSizegrip1 = ttk.Sizegrip(top)
        self.TSizegrip1.place(anchor=SE, relx=1.0, rely=1.0)

        self.Frame1 = Frame(top)
        self.Frame1.place(relx=0.0, rely=0.06, relheight=0.94, relwidth=0.78)
        self.Frame1.configure(relief=GROOVE,borderwidth="2",width=805)

        self.figure = Figure(dpi=50)
        self.Canvas1 = FigureCanvasTkAgg(self.figure, master=self.Frame1)
        self.Canvas1.get_tk_widget().pack(side=TOP, fill="both", expand=1)       

        self.ax = self.figure.add_axes([.05,.05,.80,.9]) 
        self.ax.axis([float(self.config['gen']['dlonmin']), float(self.config['gen']['dlonmax']),
                      float(self.config['gen']['dlatmin']), float(self.config['gen']['dlatmax'])])
        self.cax = self.figure.add_axes([.05+.8+0.025,.05,.025,.9])
        self.cax.set_visible(False)
        self.toolbar = NT2tk( self.Canvas1, self.Frame1 )
        self.menubar = Menu(top,bg=self._bgcolor,fg=self._fgcolor)
        top.configure(menu = self.menubar)
        
        def add_cascade(r,m,t):
            r.add_cascade(menu=m, activebackground="#d9d9d9",
            activeforeground="#000000", background="#d9d9d9",
            foreground="#000000", label=t)            
        
        def add_command(r,c,t):
            r.add_command(activebackground="#d8d8d8",
            activeforeground="#000000", background="#d9d9d9",
            command=c, foreground="#000000", label=t)
                        
        
        self.file = Menu(top,tearoff=0)
        add_cascade(self.menubar,self.file,"File")
        add_command(self.file,pygrid_support.TODO,"New")
        self.file.add_separator(background="#d9d9d9")
        add_command(self.file,pygrid_support.TODO,"Exit")

        self.save = Menu(top,tearoff=0)
        add_cascade(self.menubar,self.save,"Save")
        add_command(self.save,pygrid_support.save_segfile,"Save segfile")
        add_command(self.save,pygrid_support.save_neifile,"Save neifile")
        add_command(self.save,pygrid_support.save_nodfile,"Save nodfile")
        add_command(self.save,pygrid_support.save_nod2polyfile,"Save nod2poly file")
        add_command(self.save,pygrid_support.save_llzfile,"Save llzfile")
        add_command(self.save,pygrid_support.save_markerfile,"Save markerfile")

        self.load = Menu(top,tearoff=0)
        add_cascade(self.menubar,self.load,"Load")
        add_command(self.load,pygrid_support.load_coastline,"Load coastline")
        add_command(self.load,pygrid_support.load_segfile,"Load segfile")
        add_command(self.load,pygrid_support.load_neifile,"Load neifile")
        add_command(self.load,pygrid_support.load_nodfile,"Load nodfile")
        add_command(self.load,pygrid_support.load_llzfile,"Load llzfile")
        add_command(self.load,pygrid_support.load_fvcomfile,"Load fvcom")
        add_command(self.load,pygrid_support.load_fvcom_inputfile,"Load fvcom input")
        add_command(self.load,pygrid_support.load_markerfile,"Load markerfile")
        
        self.options = Menu(top,tearoff=0)
        add_cascade(self.menubar,self.options,"Options")
        add_command(self.options,self.getGeneralOptionBox,"General Options")
        add_command(self.options,self.getCoastOptionBox,"Coastline Options")
        add_command(self.options,self.getSegOptionBox,"Seg Options")
        add_command(self.options,self.getNeiOptionBox,"Nei Options")
        add_command(self.options,self.getNodOptionBox,"Nod Options")
        add_command(self.options,self.getllzOptionBox,"llz Options")
        add_command(self.options,self.getFvcomOptionBox,"Fvcom Options")
        add_command(self.options,self.getMarkerOptionBox,"Marker Options")
               
        self.help = Menu(top,tearoff=0)
        add_cascade(self.menubar,self.help,"Help")
        add_command(self.help,pygrid_support.TODO,"About")

             
        ################################################################
        #
        #   Checkboxes
        #
        ################################################################
        self.Frame3 = Frame(top)
        self.Frame3.place(relx=0.0, rely=0.0, relheight=0.07, relwidth=0.78)
        self.Frame3.configure(relief=GROOVE,borderwidth="2",width=805)

        self.types=['coast','seg','nei','nod','llz','neic','fvcom','marker']
        self.CBVar={}
        for typ in self.types:
            self.CBVar[typ]=IntVar()
            
        def cbutton(frm,x,y,h,w,t,c,v):
            cb = Checkbutton(frm)
            cb.place(relx=x, rely=y, relheight=h, relwidth=w)
            cb.configure(activebackground="#d9d9d9",justify=LEFT)
            cb.configure(text=t,command=c,variable=v)
            return cb

        cbutton(self.Frame3,0.01,0.04,0.91,0.15,'''Show coastline''',
                pygrid_support.toggle_coastline, self.CBVar['coast'])
        cbutton(self.Frame3,0.16,0.04,0.91,0.15,'''Show Segfile''',
                pygrid_support.toggle_segfile, self.CBVar['seg'])
        cbutton(self.Frame3,0.31,0.04,0.91,0.12,'''Show Neifile''',
                pygrid_support.toggle_neifile, self.CBVar['nei'])
        cbutton(self.Frame3,0.43,0.04,0.91,0.14,'''Show Nodfile''',
                pygrid_support.toggle_nodfile, self.CBVar['nod'])
        cbutton(self.Frame3,0.57,0.04,0.91,0.12,'''Show llzfile''',
                pygrid_support.toggle_llzfile, self.CBVar['llz'])
        cbutton(self.Frame3,0.70,0.04,0.91,0.15,'''Show nei color''',
                pygrid_support.toggle_neifilecolor, self.CBVar['neic'])

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
        self.Frame2.configure(relief=GROOVE,borderwidth="2",width=215)
        
        self.Frame5 = Frame(self.nb)
        self.Frame5.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame5.configure(relief=GROOVE,borderwidth="2",width=215)
        
        self.Frame6 = Frame(self.nb)
        self.Frame6.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame6.configure(relief=GROOVE,borderwidth="2",width=215)    
        
        self.Frame7 = Frame(self.nb)
        self.Frame7.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame7.configure(relief=GROOVE,borderwidth="2",width=215)  
        
        self.Frame8 = Frame(self.nb)
        self.Frame8.place(relx=0.78, rely=0.0, relheight=0.75, relwidth=0.22)
        self.Frame8.configure(relief=GROOVE,borderwidth="2",width=215)            
                
        self.nb.add(self.Frame2, text='Nodes')
        self.nb.add(self.Frame5, text='Depth')
        self.nb.add(self.Frame6, text='Seg')
        self.nb.add(self.Frame7, text='FVCOM')
        self.nb.add(self.Frame8, text='Marker')

        self.nb.place(relx=0.78, rely=0, relheight=0.75, relwidth=0.22)
        
        
        
        rh = 0.055
        rw = 0.85
        rw2 = 0.4  
        rw4 = 0.2      
        sh = 0.06
        
        ########################################################################
        # functions for labels entrys etc that capture common elements
        ########################################################################
        def label(frm,x,y,h,w,t):
            l = Label(frm)
            l.place(relx=x, rely=y, relheight=h, relwidth=w)
            l.configure(activebackground="#f9f9f9")
            l.configure(text=t)     
            return l
            
        def entry(frm,x,y,h,w,t):
            e = Entry(frm)
            e.place(relx=x, rely=y, relheight=h, relwidth=w)
            e.configure(background="white")
            e.configure(font="TkFixedFont")
            e.configure(selectbackground="#c4c4c4")
            e.insert(0,t)
            return e
            
        def button(frm,x,y,h,w,t,c):
            b = Button(frm)
            b.place(relx=x, rely=y, relheight=h, relwidth=w)
            b.configure(activebackground="#d9d9d9")
            b.configure(text=t)
            b.configure(command=c)
            return b   
        
        ########################################################################
        #
        #   Node Tab
        #
        ########################################################################

        ry = 0.01

        label(self.Frame2,0.075,ry,rh,rw2,'''Set resolution''')
        self.Entry1 = entry(self.Frame2,0.525,ry,rh,rw2,'')
        button(self.Frame2,0.075,ry+sh*1,rh,rw,'''Spray Area''',pygrid_support.spray_area)
        button(self.Frame2,0.075,ry+sh*2,rh,rw,'''Remove Area''',pygrid_support.remove_area)
        button(self.Frame2,0.075,ry+sh*3,rh,rw,'''Remove Area (llz)''',pygrid_support.remove_area_llz)
        button(self.Frame2,0.075,ry+sh*5,rh,rw,'''Remove nodes inside seg''',pygrid_support.remove_nodeseg_in)
        button(self.Frame2,0.075,ry+sh*6,rh,rw,'''Remove nodes outside seg''',pygrid_support.remove_nodeseg_out)
        button(self.Frame2,0.075,ry+sh*7,rh,rw,'''Extract nod from nei''',pygrid_support.extract_nod)
        button(self.Frame2,0.075,ry+sh*8,rh,rw,'''Extract seg from nei''',pygrid_support.extract_seg)
        button(self.Frame2,0.075,ry+sh*9,rh,rw,'''Extract llz from nei''',pygrid_support.extract_llz)
        button(self.Frame2,0.075,ry+sh*10,rh,rw,'''Sub llz depth into nei''',pygrid_support.subllz2nei)


        
        
        ########################################################################
        #
        #   Depth tab
        #
        ########################################################################
        
        ry = 0.01        
        label(self.Frame5,0.1,ry,rh,.2,'''Min''')        
        label(self.Frame5,0.375,ry,rh,.2,'''Max''')        
        label(self.Frame5,0.66,ry,rh,.2,'''Mean''')
        
        ry += sh
        self.Labelsmin = label(self.Frame5,0.1,ry,rh,.2,'''na''')        
        self.Labelsmax = label(self.Frame5,0.375,ry,rh,.2,'''na''')        
        self.Labelsmean = label(self.Frame5,0.66,ry,rh,.2,'''na''')
                
        button(self.Frame5,0.075,ry+0.05,rh,rw,'''Calc Stats''',pygrid_support.calc_stats)


        ry += 2*sh
        label(self.Frame5,0.5,ry,rh,rw2,'''Set depth''')
        button(self.Frame5,0.075,ry+0.05,rh,rw2,'''Set depth''',pygrid_support.set_depth)
        self.Entry3 = entry(self.Frame5,0.525,ry+0.05,rh,rw2,'')

        ry += 2*sh
        label(self.Frame5,0.5,ry,rh,rw2,'''Avg. depth''')
        button(self.Frame5,0.075,ry+0.05,rh,rw2,'''Avg. depth''',pygrid_support.avg_depth)
        self.Entry4 = entry(self.Frame5,0.525,ry+0.05,rh,rw2,'')
                
        ry += 2*sh
        label(self.Frame5,.275,ry,rh,.3,'''Limit Min''')
        label(self.Frame5,.625,ry,rh,.3,'''Limit Max''')

        ry += sh
        label(self.Frame5,.05,ry,rh,.2,'''Depth''')
        self.Entryhmin = entry(self.Frame5,0.275,ry,rh,rw2*.75,'')
        self.Entryhmax = entry(self.Frame5,0.625,ry,rh,rw2*.75,'')
    
        ry += sh
        label(self.Frame5,.05,ry,rh,.2,'''dhh''')
        self.Entrydhhmin = entry(self.Frame5,0.275,ry,rh,rw2*.75,'')
        self.Entrydhhmax = entry(self.Frame5,0.625,ry,rh,rw2*.75,'')
        
        ry += sh
        button(self.Frame5,0.075,ry,rh,rw,'''Smooth''',pygrid_support.smooth)
        
        
        ########################################################################
        #
        #   Seg Tab
        #
        ########################################################################
        ry = 0.01  
        button(self.Frame6,0.075,ry,rh,rw2,'''Select Seg''',pygrid_support.select_seg)      
        self.Entry2=entry(self.Frame6,0.525,ry,rh,rw2,'')        
        button(self.Frame6,0.075,ry+sh*1,rh,rw,'''Create Seg''',pygrid_support.create_seg)
        button(self.Frame6,0.075,ry+sh*2,rh,rw,'''Delete Seg''',pygrid_support.delete_seg)     
        
        ########################################################################
        #
        #   FVCOM Tab
        #
        ########################################################################
        ry = 0.01  
        cbutton(self.Frame7,0.075,ry,rh,rw,'''Show FVCOM''',
                pygrid_support.toggle_fvcom, self.CBVar['fvcom'])
                
        label(self.Frame7,.075,ry+sh,rh,rw4,'''Times:''')
        self.timemin=label(self.Frame7,.275,ry+sh,rh,rw4,'''na''')
        self.timemax=label(self.Frame7,.5,ry+sh,rh,rw4,'''na''')
        self.etime = entry(self.Frame7,0.75,ry+sh,rh,rw4,'0')
        label(self.Frame7,.075,ry+sh*2,rh,rw4,'''Levels:''')
        self.lvlmin=label(self.Frame7,.275,ry+sh*2,rh,rw4,'''na''')
        self.lvlmax=label(self.Frame7,.5,ry+sh*2,rh,rw4,'''na''')
        self.elvl = entry(self.Frame7,0.75,ry+sh*2,rh,rw4,'0')

        
        self.FVCOMMenuVar = StringVar(root)
        self.FVCOMChoices={'speed_da','speed','dhh','sidelength','vorticity_da','vorticity','density'}
        self.FVCOMMenuVar.set('speed_da')
        self.FVCOMMenu = OptionMenu(self.Frame7,self.FVCOMMenuVar,*self.FVCOMChoices)
        self.FVCOMMenu.place(relx=0.075,rely=ry+sh*3,relheight=rh,relwidth=rw)
        #self.FVCOMMenuVar.trace('w', pygrid_support.TODO)#change_fvcommenu)
           
        self.overmenu = entry(self.Frame7,0.075,ry+sh*4,rh,rw,'')
           
        self.fsb = Frame(self.Frame7)
        self.fsb.place(relx=rw+.01,rely=ry+sh*5,relheight=.625, relwidth=0.1)

        self.sb = Scrollbar(self.fsb,orient="vertical")
        self.sb.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.Frame7)
        self.listbox.place(relx=0.01,rely=ry+sh*5,relheight=.625,relwidth=rw)

        # attach listbox to scrollbar
        self.listbox.config(yscrollcommand=self.sb.set)
        self.sb.config(command=self.listbox.yview)
        
        button(self.Frame7,0.075,ry+sh*15.5,rh,rw,'''Plot FVCOM''',pygrid_support._plot_fvcomfile)     
        
        ########################################################################
        #
        #   Markers Tab
        #
        ########################################################################
        ry = 0.01  
        cbutton(self.Frame8,0.075,ry,rh,rw,'''Show Markers''',
                pygrid_support.toggle_markerfile, self.CBVar['marker'])
                
        label(self.Frame8,.075,ry+sh,rh,rw2,'''Lon:''')
        self.mlon = entry(self.Frame8,0.075,ry+sh*2,rh,rw2,'')
        
        label(self.Frame8,.525,ry+sh,rh,rw2,'''Lat:''')
        self.mlat = entry(self.Frame8,0.525,ry+sh*2,rh,rw2,'')
        
        
        label(self.Frame8,.075,ry+sh*3,rh,rw,'''Label:''')
        self.mlabel = entry(self.Frame8,0.075,ry+sh*4,rh,rw,'')
                
        
        button(self.Frame8,0.075,ry+sh*15.5,rh,rw,'''Add Marker''',pygrid_support._add_marker) 
        
        ########################################################################
        #
        #   Selection controls
        #
        ########################################################################        
        self.FrameSelection = Frame(top)
        self.FrameSelection.place(relx=0.78, rely=0.75, relheight=.1, relwidth=0.22)
        self.FrameSelection.configure(relief=GROOVE,borderwidth="2",width=215)
        
        button(self.FrameSelection,0.05,0.075,0.4,rw,'''Clear Selection''',pygrid_support.clear_selection)
        button(self.FrameSelection,0.05,0.525,0.4,rw,'''Select Area''',pygrid_support.select_area)
        
        
        ########################################################################
        #
        #   Colorbar controls
        #
        ########################################################################        
        self.Frame4 = Frame(top)
        self.Frame4.place(relx=0.78, rely=0.85, relheight=.15, relwidth=0.22)
        self.Frame4.configure(relief=GROOVE,borderwidth="2",width=215)
        
        label(self.Frame4,0.05,0.03,0.255,rw2,'''Max''')
        self.Entry41=entry(self.Frame4,0.525,0.03,0.255,rw2,'')
        label(self.Frame4,0.05,0.33,0.255,rw2,'''Min''')
        self.Entry42=entry(self.Frame4,0.525,0.33,0.255,rw2,'')
        button(self.Frame4,0.075,.66,0.255,rw2,'''Redraw llz''',pygrid_support.redraw_llz)
        button(self.Frame4,0.525,.66,0.255,rw2,'''Redraw nei''',pygrid_support.redraw_nei)


    def getGeneralOptionBox(self):
        GeneralBox=options.GeneralOptionBox(self.config)
        GeneralBox.root=root
    def getCoastOptionBox(self):
        CoastBox=options.CoastOptionBox(self.config)
        CoastBox.root=root
    def getSegOptionBox(self):
        SegBox=options.SegOptionBox(self.config)
        SegBox.root=root
    def getNeiOptionBox(self):
        NeiBox=options.NeiOptionBox(self.config)
        NeiBox.root=root
    def getNodOptionBox(self):
        NodBox=options.NodOptionBox(self.config)
        NodBox.root=root
    def getllzOptionBox(self):
        llzBox=options.llzOptionBox(self.config)
        llzBox.root=root
    def getFvcomOptionBox(self):
        fvcomBox=options.fvcomOptionBox(self.config)
        fvcomBox.root=root
    def getMarkerOptionBox(self):
        markerBox=options.markerOptionBox(self.config)
        markerBox.root=root


if __name__ == '__main__':
    vp_start_gui()
    







