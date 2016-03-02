import sqlite3 as dbapi
from gi.repository import Gtk

class Taller:

   # cursor.execute("CREATE TABLE taller (matricula VARCHAR(7) PRIMARY KEY NOT NULL,"
    #                        "vehiculo VARCHAR(20),"
     #                       "kilometros INT,"
      #                      "fecha VARCHAR(50) ,"
       #                     "cliente VARCHAR(10),"
        #                    "cif VARCHAR(10),"
         #                   "telefono INT,"
          #                  "direccion VARCHAR(10))")

    def __init__(self):
        #Conexión con la base de datos, y conectar a la interface
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()

        self.builder = Gtk.Builder()
        self.builder.add_from_file("Taller.glade")
        self.inicializar()
        self.ventana = self.builder.get_object("Taller")

        # Señales, aquí se declaran los métodos anteriormente comentados, para que al pulsar accedan
        sinais = {"on_insertar_clicked": self.on_insertar_clicked,
                      "on_consultar_clicked": self.on_consultar_clicked,
                      "on_borrar_clicked": self.on_borrar_clicked,
                      "on_Modificar_clicked": self.on_Modificar_clicked,
                      "delete-event": Gtk.main_quit}

        self.builder.connect_signals(sinais)
        self.ventana.set_title("Taller.")
        self.ventana.show_all()


    def inicializar(self):
         #treeview

        self.box = self.builder.get_object("box2")
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vista = Gtk.TreeView()
        self.box.add(self.scroll)
        self.scroll.add(self.vista)
        self.scroll.set_size_request(500, 500)
        self.scroll.show()

        self.lista = Gtk.ListStore(str, str, str, str, str, str, str, str)

        self.lista.clear()
        self.cursor.execute("select * from taller")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)

        for i, title in enumerate(["matricula","vehiculo","kilometro","fecha","cliente","cif", "telefono", "direccion"]):
            render = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(title, render, text=i)
            self.vista.append_column(columna)



    # Método Consultar, imprime los datos de la base por consola
    def on_consultar_clicked(self, control):
        self.actualizar()

    def actualizar(self):
        self.lista.clear()
        self.cursor.execute("select * from taller")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)



    # Método Borrar
    def on_borrar_clicked(self, borrar):
        matricula = self.builder.get_object("matricula").get_text()
        #print("El evento está siendo borrado por código")
        self.cursor.execute("delete from taller where matricula ='" + matricula + "'")
        self.popup("Borrado")
        self.bd.commit()
        self.actualizar()

    # Método Modificar. Modifica a través de la primary Key
    def on_Modificar_clicked(self, modificar):
        matricula = self.builder.get_object("matricula").get_text()
        vehiculo = self.builder.get_object("vehiculo").get_text()
        kilometros = self.builder.get_object("kilometros").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()

        print("Esperando datos")
        self.cursor.execute("update taller set vehiculo ='" + vehiculo + "'"
                                             ",kilometros='" + kilometros + "'"
                                             ",fecha='" + fecha + "'"
                                             ",cliente='" + cliente + "'"
                                             ",cif='" + cifnif +"'"
                                             ",telefono='" + telefono +"'"
                                             ",direccion='" + direccion +"' where matricula='" + matricula + "'")
        self.popup("Modificado")
        self.bd.commit()

    # Método insertar
    def on_insertar_clicked(self, control):
        matricula = self.builder.get_object("matricula").get_text()
        vehiculo = self.builder.get_object("vehiculo").get_text()
        kilometros = self.builder.get_object("kilometros").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()


        print("inserte")
        self.cursor.execute(
            "insert into taller values('" + matricula + "'"
                                     ",'" + vehiculo + "'"
                                     ",'" + kilometros + "'"
                                     ",'" + fecha+"'"
                                     ",'" + cliente + "'"
                                     ",'" + cifnif +"'"
                                     ",'" + telefono +"'"
                                     ",'" + direccion +"')")
        self.popup("Insertado")
        # Siempre se debe hacer un commit al final de cada evento
        self.bd.commit()

    def cerrar(self, widget):
        widget.destroy()

    def popup(self, texto):
        window = Gtk.Window(title="Aviso")
        label = Gtk.Label(texto)
        label.set_padding(15, 15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

