import sqlite3 as dbapi
from gi.repository import Gtk,Gdk

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
        self.rojo = Gdk.RGBA()
        self.rojo.parse("Red")
        self.verde = Gdk.RGBA()
        self.verde.parse("Green")

        #Conexión con la base de datos
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()
        #Abrimos y conectamos a la interfaz de taller
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Taller.glade")
        self.inicializar()
        self.ventana = self.builder.get_object("Taller")

        #Declaramos los nombres de los métodos para que al pulsar el boton tenga función
        sinais = {"on_insertar_clicked": self.on_insertar_clicked,
                      "on_consultar_clicked": self.on_consultar_clicked,
                      "on_borrar_clicked": self.on_borrar_clicked,
                      "on_Modificar_clicked": self.on_Modificar_clicked,
                      "on_ayuda_clicked":self.on_ayuda_clicked,
                      "delete-event": Gtk.main_quit}
        self.builder.connect_signals(sinais)
        self.ventana.set_title("Taller.")
        self.ventana.show_all()


    def inicializar(self):
        #treeview o tabla, en el que se muestran los datos de la base de datos
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

    #Metodo de ayuda al usuario explicando como usar los botones y el programa
    def on_ayuda_clicked(self, widget):
        self.popup = ("Necesitas ayuda? \nAñadir: Rellene todos los campos para hacer una insercion en la base de datos\nEditar: introduce la matricula que quieres modificar, y cambia los campos que necesites.\nEliminar:Selecciona en la tabla la fila que quieres borrar y listo.")


    # Método Consultar, imprime los datos de la base
    def on_consultar_clicked(self, control):
        self.actualizar()

    #Metodo borrar que borra seleccionando la fila en la tabla
    def on_borrar_clicked(self, widget):
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.matricula = model[selec][0]
            self.cursor.execute("delete from taller where matricula ='" + self.matricula + "'")
            self.actualizar()
            self.bd.commit
            self.popup("Borrado")

     #Método Modificar. Modifica a través de la primary Key
    def on_Modificar_clicked(self, modificar):
        matricula = self.builder.get_object("matricula").get_text()
        vehiculo = self.builder.get_object("vehiculo").get_text()
        kilometros = self.builder.get_object("kilometros").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()

        self.cursor.execute("update taller set vehiculo ='" + vehiculo + "'"
                                             ",kilometros='" + kilometros + "'"
                                             ",fecha='" + fecha + "'"
                                             ",cliente='" + cliente + "'"
                                             ",cif='" + cifnif +"'"
                                             ",telefono='" + telefono +"'"
                                             ",direccion='" + direccion +"' where matricula='" + matricula + "'")
        self.popup("Modificado")
        self.bd.commit()
        self.actualizar()

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
        self.actualizar()
        # Siempre se debe hacer un commit al final de cada evento
        self.bd.commit()
    #Este metodo simplemente actualiza la tabla
    def actualizar(self):
        self.lista.clear()
        self.cursor.execute("select * from taller")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)

    def cerrar(self, widget):
        widget.destroy()

    #Este metodo abre una ventana emergente que muestra
    # el texto correspondiente a cada metodo
    def popup(self, texto):
        window = Gtk.Window(title="Aviso")
        label = Gtk.Label(texto)
        label.set_padding(15, 15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

""" # Método Borrar viejo
    def on_borrar_clicked(self, borrar):
        matricula = self.builder.get_object("matricula").get_text()
        #print("El evento está siendo borrado por código")
        self.cursor.execute("delete from taller where matricula ='" + matricula + "'")
        self.popup("Borrado")
        self.bd.commit()
        self.actualizar()
        """