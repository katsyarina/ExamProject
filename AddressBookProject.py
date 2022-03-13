import wx
import sqlite3

adressbook =  sqlite3.connect('adressbook_db.db')
cursor = adressbook.cursor()
cursor.execute('''create table if not exists adressbook_table(id integer primary key autoincrement, identify varchar(30), firstname varchar(30), secondname varchar(30), s_secondname varchar(30), 
country varchar (50), city varchar(50), postind varchar(12), homephone varchar(20), mobile varchar(20), email varchar(30), notes text)''')

class AddressBook(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Address Book", size=(500,550))
        self.panel = wx.Panel(self,-1)
        self.SetBackgroundColour("#68ed7e")
        self.Centre()
        ico = wx.Icon("open-book.png")
        self.SetIcon(ico)
       
        self.title=wx.StaticText(self.panel,-1,"Справочная информация по адресам",pos=(110,15))
        self.firstname=wx.StaticText(self.panel,-1,"Фамилия",pos=(65,50))
        self.secondname=wx.StaticText(self.panel,-1,"Имя",pos=(92,80))
        self.s_secondname=wx.StaticText(self.panel,-1,"Отчество",pos=(66,110))
        self.country=wx.StaticText(self.panel,-1,"Страна",pos=(78,140))
        self.city=wx.StaticText(self.panel,-1,"Населенный пункт",pos=(12,170))
        self.postind=wx.StaticText(self.panel,-1,"Почтовый индекс",pos=(19,200))
        self.homephone=wx.StaticText(self.panel,-1,"Домашний телефон",pos=(5,230))
        self.mobile=wx.StaticText(self.panel,-1,"Моб. телефон",pos=(38,260))
        self.email=wx.StaticText(self.panel,-1,"Email",pos=(88,290))
        self.notes=wx.StaticText(self.panel,-1,"Заметка",pos=(73,320))

        self.firstname1=wx.TextCtrl(self.panel,-1,"",pos=(130,50),size=(170,20))
        self.secondname1=wx.TextCtrl(self.panel,-1,"",pos=(130,80),size=(170,20))
        self.s_secondname1=wx.TextCtrl(self.panel,-1,"",pos=(130,110),size=(170,20))
        self.country1=wx.TextCtrl(self.panel,-1,"",pos=(130,140),size=(250,20))
        self.city1=wx.TextCtrl(self.panel,-1,"",pos=(130,170),size=(250,20))
        self.postind1=wx.TextCtrl(self.panel,-1,"",pos=(130,200),size=(170,20))
        self.homephone1=wx.TextCtrl(self.panel,-1,"",pos=(130,230),size=(170,20))
        self.mobile1=wx.TextCtrl(self.panel,-1,"",pos=(130,260),size=(170,20))
        self.email1=wx.TextCtrl(self.panel,-1,"",pos=(130,290),size=(170,20))
        self.notes1=wx.TextCtrl(self.panel,-1,"",pos=(130,320),size=(250,100),style=wx.TE_MULTILINE)


        self.btn1 = wx.Button(self.panel,202,"очистить форму",pos=(80,450),size=(110,30))
        self.btn = wx.Button(self.panel,201,"сохранить",pos=(200,450),size=(70,30))
        self.btn2 = wx.Button(self.panel,203,"изменить форму",pos=(280,450),size=(105,30))
        
        self.Bind(wx.EVT_BUTTON,self.retrive,id=203)
        self.Bind(wx.EVT_BUTTON,self.clear,id=202)
        self.Bind(wx.EVT_BUTTON,self.save,id=201)

    @staticmethod
    def id_update():
        cursor.execute('''select id from adressbook_table''')
        arr = cursor.fetchall()
        m = 1
        for i in arr:
            id_star = int(i[0])
            cursor.execute('''update adressbook_table set id = ? where id = ?''', (m, id_star))
            adressbook.commit()
            m += 1

    def getvalue_fordate(self):
        self.firstname = self.firstname1.GetValue()
        self.secondname = self.secondname1.GetValue()
        self.s_secondname = self.s_secondname1.GetValue()
        self.country = self.country1.GetValue()
        self.city = self.city1.GetValue()
        self.postind = self.postind1.GetValue()
        self.homephone = self.homephone1.GetValue()
        self.mobile = self.mobile1.GetValue()
        self.email = self.email1.GetValue()
        self.notes = self.notes1.GetValue()

    def save(self, event):
        self.getvalue_fordate()


        if (len(self.firstname) and len(self.secondname) and len(self.s_secondname) and len(self.country) and len(self.city) and len(self.postind) and len(self.homephone) and len(self.mobile) and len(self.email) and len(self.notes))>0:
            box = wx.TextEntryDialog(None,"Введите идентификационный номер","Title","индентификационный номер")
            if box.ShowModal() == wx.ID_OK:
                self.addressbookname=box.GetValue()

                AddressBook.table_select()
                if self.addressbookname not in [i[1] for i in k]:
                    cursor.execute('''insert into adressbook_table(identify, firstname, secondname, s_secondname, 
                    country, city, postind, homephone, mobile, email, notes) values(?,?,?,?,?,?,?,?,?,?,?)''',
                                   (self.addressbookname,
                                    self.firstname,
                                    self.secondname,
                                    self.s_secondname,
                                    self.country,
                                    self.city,
                                    self.postind,
                                    self.homephone,
                                    self.mobile,
                                    self.email,
                                    self.notes))
                    AddressBook.id_update()
                    adressbook.commit()
                else:
                    self.dial = wx.MessageDialog(None, 'Запись с таким названием уже существует, введите другое название', 'Info', wx.OK)
                    self.dial.ShowModal()
            else:
                self.dial = wx.MessageDialog(None, 'Запись не сохранена', 'Info', wx.OK)
                self.dial.ShowModal()
        else:
            self.dial = wx.MessageDialog(None, 'Пожалуйста, заполните все поля', 'Info', wx.OK)
            self.dial.ShowModal()

    def clear(self, event):
        self.firstname1.Clear()
        self.secondname1.Clear()
        self.s_secondname1.Clear()
        self.country1.Clear()
        self.city1.Clear()
        self.postind1.Clear()
        self.homephone1.Clear()
        self.mobile1.Clear()
        self.email1.Clear()
        self.notes1.Clear()
        
    def retrive(self, event):

        cursor.execute('''select * from adressbook_table''')
        k = cursor.fetchall()
        arr = [i[1] for i in k]
        self.box=wx.SingleChoiceDialog(None,"Выберите идентификационный номер","identify", arr)
        if self.box.ShowModal()==wx.ID_OK:
            self.apples=self.box.GetStringSelection()
            cursor.execute('''select * from adressbook_table where identify = (?)''', (self.apples,))
            k = cursor.fetchall()
            self.firstname1.SetValue(k[0][2])
            self.secondname1.SetValue(k[0][3])
            self.s_secondname1.SetValue(k[0][4])
            self.country1.SetValue(k[0][5])
            self.city1.SetValue(k[0][6])
            self.postind1.SetValue(str(k[0][7]))
            self.homephone1.SetValue(str(k[0][8]))
            self.mobile1.SetValue(str(k[0][9]))
            self.email1.SetValue(k[0][10])
            self.notes1.SetValue(k[0][11])
            self.btn4=wx.Button(self.panel,205,"Обновить",pos=(395,450),size=(70,30))
            self.Bind(wx.EVT_BUTTON,self.update,id=205)
            self.note=wx.StaticText(self.panel,-1,"После внесения изменений, нажмите кнопку 'Обновить' ",pos=(100,485))


    def update(self,event):
        self.getvalue_fordate()
        cursor.execute('''update adressbook_table set firstname=(?), secondname=(?), s_secondname=(?), 
country=(?), city=(?), postind=(?), homephone=(?), mobile=(?), email=(?), notes=(?) where identify = (?)''', (self.firstname,
                              self.secondname,
                              self.s_secondname,
                              self.country,
                              self.city,
                              self.postind,
                              self.homephone,
                              self.mobile,
                              self.email,
                              self.notes,
                              self.apples))
        adressbook.commit()
        self.btn4.Destroy()
        self.dial = wx.MessageDialog(None, 'Обновлено', 'Info', wx.OK)
        self.dial.ShowModal()

    @staticmethod
    def table_select():
        cursor.execute('''select * from adressbook_table''')
        k = cursor.fetchall()
        return k



if __name__ == "__main__":
    cursor.execute('''select * from adressbook_table''')
    k = cursor.fetchall()
    for i in k:
        print(' '.join([str(j) for j in i]))
    app = wx.App()
    frame = AddressBook()
    frame.Centre()
    frame.Show()
    app.MainLoop()
