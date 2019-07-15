try:
    import Tkinter as tkinter
except ImportError:
    import tkinter

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import pygrid_support
import matplotlib as mpl

class Mbox(object):

    root = None

    def __init__(self, config):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)
        """
        
        self.config=config
        
        tki = tkinter
        self.top = tki.Toplevel(Mbox.root)
        self.top.geometry("400x500+650+250")
        self.top.title("Plot Options")
        self.top.configure(highlightcolor="black")

        self.frm = tki.Frame(self.top, borderwidth=4, relief='ridge')
        self.frm.pack(fill='both', expand=True)


        rh = 0.055
        rw = 0.85
        rw2 = 0.4 
        rw3 = 0.33       
        sh = 0.06
        ry = 0.01
        
        self.Label2 = tki.Label(self.frm)
        self.Label2.place(relx=0.650, rely=ry, relheight=rh, relwidth=rw3)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Override''')

        ry += sh

        self.Label1 = tki.Label(self.frm)
        self.Label1.place(relx=0.0, rely=ry, relheight=rh, relwidth=rw3)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Colormap''') 

        self.CMMenuVar = tki.StringVar(self.root)
        self.CMChoices={'viridis','jet','seismic'}
        self.CMMenuVar.set(self.config['plot']['colormap'])
        self.CMMenu = tki.OptionMenu(self.frm,self.CMMenuVar,*self.CMChoices)
        self.CMMenu.place(relx=0.2850, rely=ry, relheight=rh, relwidth=rw3)
        #self.CMMenuVar.trace('w', pygrid_support.change_neimenu)
        
        self.Entry1 = tki.Entry(self.frm)
        self.Entry1.place(relx=0.6500, rely=ry, relheight=rh, relwidth=rw3)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")



        label = tki.Label(self.frm, text='')
        label.pack(padx=4, pady=4)

        # caller_wants_an_entry = dict_key is not None

        # if caller_wants_an_entry:
            # self.entry = tki.Entry(self.frm)
            # self.entry.pack(pady=4)

            # # b_submit = tki.Button(self.frm, text='Submit')
            # # b_submit['command'] = lambda: self.entry_to_dict(dict_key)
            # b_submit.pack()


        self.b_save = tki.Button(self.frm)
        self.b_save.place(relx=.01+sh*0.1, rely=.925, relheight=rh, relwidth=rw3*.95)
        self.b_save.configure(activebackground="#d9d9d9")
        self.b_save.configure(text='''Save''')
        self.b_save.configure(command=self.saveConfig)
        
        self.b_cancel = tki.Button(self.frm)
        self.b_cancel.place(relx=.01+rw3*.95+sh*.25, rely=.925, relheight=rh, relwidth=rw3*.95)
        self.b_cancel.configure(activebackground="#d9d9d9")
        self.b_cancel.configure(text='''Close''')
        self.b_cancel.configure(command=self.top.destroy)
        
        self.b_submit = tki.Button(self.frm)
        self.b_submit.place(relx=.01+rw3*2*.95+sh*.4, rely=.925, relheight=rh, relwidth=rw3*.95)
        self.b_submit.configure(activebackground="#d9d9d9")
        self.b_submit.configure(text='''Apply''')
        self.b_submit.configure(command=self.setConfig)


    def setConfig(self):
        reNEIC=False
        
        e1=self.Entry1.get() 
        if e1 != '' and self.config['plot']['colormap']!=e1:
            try:
                mpl.cm.get_cmap(e1)            
                self.config['plot']['colormap']=e1
                reNEIC=True
            except ValueError:
                print('Invalid Colormap')
        elif self.config['plot']['colormap']!=self.CMMenuVar.get():
            self.config['plot']['colormap']=self.CMMenuVar.get()
            reNEIC=True
            
            
        
        if reNEIC:
            pygrid_support._plot_neifilecolor
            

            
    
    def saveConfig(self):
        '''Save the config file to .config'''    
        # Open the file and write to it
        with open('.config', "w") as f:
            
            for key1 in self.config.keys():
                f.write('[{}]\n'.format(key1))
                for key2 in self.config[key1].keys():
                    f.write('{} {}\n'.format(key2,self.config[key1][key2]))
                f.write('\n')


            
            


def defaultConfig():
    '''Default options'''
    config = {}
    
    config['plot']={'linewidth': 1,
                    'colormap': 'viridis'}

    
    return config
    
                
def loadConfig(config):
    '''This is a ... less then stellar parser and should be replaced.'''
    
        
    
    # Open the file and read it
    with open('.config', "r") as f:
        dkey=''
        for line in f:
            line=line.replace('\n','')
            if line.startswith('['):
                dkey=line[1:-1]
                continue
            if len(line)>0:
                sline=line.split(' ')
                #print(dkey)
                #print(sline)
                config[dkey][sline[0]]=sline[1]




