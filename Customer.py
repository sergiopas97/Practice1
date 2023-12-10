class Customer:
    headings = ['ID','Name','Bill Address','Phone','Email','Pos']
    fields = {
        '-ID-': 'Customer ID:',
        '-Name-': 'Customer Name:',
        '-Bill-': 'Billing Address:',
        '-Phone-': 'Phone:',
        '-Email-': 'Email:',
        '-PosFile-': 'Position into File'
    }

    # El método __init__ es llamado al crear el objeto
    def __init__(self, ID, name, bill, phone, email,posFile):
        # Atributos de instancia
        self.ID = ID
        self.name = name
        self.bill = bill
        self.phone = phone
        self.email = email
        self.posFile = posFile
        self.erased = False

    def __eq__(self, oC):
        return oC.posFile==self.posFile

    def __str__(self):
        return str(self.ID)+str(self.name)+str(self.bill)+str(self.phone)+str(self.email)+str(self.posFile)
    def customerinPos(self,pos):
        return self.posFile==pos

    def setCustomer(self,name, bill, phone, email):
        self.name = name
        self.bill = bill
        self.phone = phone
        self.email = email

