from gi.repository import Gtk
from Taller import Taller

class Login:
    def __init__(self):

            builder2 = Gtk.Builder()
            builder2.add_from_file("inicio.glade")

            self.nombre = builder2.get_object("nombre")
            self.contraseña = builder2.get_object("contraseña")
            self.ventanaEntrada = builder2.get_object("inicio")

            sinais = {"on_Entrada_clicked": self.on_Entrada_clicked,
                      "delete-event": self.cerrar}

            builder2.connect_signals(sinais)
            self.ventanaEntrada.set_title("Log in.")
            self.ventanaEntrada.show_all()

    # Método de entrada para poder acceder por usuario y contraseña a la segunda ventana
    def on_Entrada_clicked(self, widget):
        nombre = self.nombre.get_text();
        contraseña = self.contraseña.get_text();
        if nombre == "taller" and contraseña == "root":
            nuevoObjeto = Taller()
            self.ventanaEntrada.destroy()

        else:
            self.popup("Prueba otra vez")
    #este metodo destruye las ventanas
    def cerrar(self, widget):
        widget.destroy()
    #Metodo para que salga una ventana emergente segun el metodo en el que lo llame
    def popup(self, texto):
        window = Gtk.Window(title="Warning")
        label = Gtk.Label(texto)
        label.set_padding(15,15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()


Login()
Gtk.main()
