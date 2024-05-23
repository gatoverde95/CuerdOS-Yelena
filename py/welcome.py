import os
import gi
import subprocess
import configparser

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class WelcomeWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("CuerdOS Yelena 1.1a Sonia")

        icon_path = "/usr/share/welcome_cuerd/data/welcome.png"

        if os.path.exists(icon_path):
            self.set_icon_from_file(icon_path)
        else:
            print("El archivo de icono no existe en la ruta especificada:", icon_path)

        self.set_default_size(645, 499)
        self.set_resizable(False)

        self.stack = Gtk.Stack()
        self.add(self.stack)

        # Stack switcher
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(1000)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.stack.add_named(main_box, "main_box")

        banner_image = Gtk.Image()
        banner_path = os.path.join("/usr/share/welcome_cuerd/data/banner.png")
        if os.path.exists(banner_path):
            banner_image.set_from_file(banner_path)
            banner_image.set_size_request(645, 258)
            main_box.pack_start(banner_image, False, False, 0)

        welcome_label = Gtk.Label()
        welcome_label.set_text("Hola!! Bienvenido a CuerdOS GNU/Linux | Cessna 1.1")
        main_box.pack_start(welcome_label, True, True, 0)

        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        icon_folder = "/usr/share/welcome_cuerd/icons/"
        self.images_folder = "/usr/share/welcome_cuerd/data/img/"

        button_data = [
            ("Pagina Oficial", "web.png", self.on_web_button_clicked),
            ("Extras", "extras.png", self.on_extras_button_clicked),
            ("Informacion", "documentation.png", self.on_documentation_button_clicked),
            ("Aplicaciones", "apps.png", self.on_apps_button_clicked),
            ("Más Juegos...", "games.png", self.on_more_games_button_clicked),
            ("Novedades", "changelog.png", self.on_changelog_button_clicked)  # Nuevo botón para abrir el registro de cambios
        ]

        for label, icon_file, callback in button_data:
            button = Gtk.Button(label=label)
            icon_path = os.path.join(icon_folder, icon_file)
            if os.path.exists(icon_path):
                button.set_image(Gtk.Image.new_from_file(icon_path))
            button.connect("clicked", callback)
            buttons_box.pack_start(button, True, True, 0)

        main_box.pack_start(buttons_box, True, True, 0)

        exit_button = Gtk.Button()
        exit_button.set_label("Salir")
        exit_button.set_always_show_image(True)
        exit_button.connect("clicked", self.on_exit_button_clicked)
        exit_button.set_size_request(80, 40)

        telegram_button = Gtk.Button(label="CuerdOS Feedback")
        telegram_button.connect("clicked", self.on_telegram_button_clicked)
        telegram_button.set_size_request(80, 40)

        github_button = Gtk.Button(label="GitHub")
        github_button.connect("clicked", self.on_github_button_clicked)
        github_button.set_size_request(80, 40)

        reddit_button = Gtk.Button(label="Reddit")
        reddit_button.connect("clicked", self.on_reddit_button_clicked)
        reddit_button.set_size_request(80, 40)

        sourceforge_button = Gtk.Button(label="SourceForge")
        sourceforge_button.connect("clicked", self.on_sourceforge_button_clicked)
        sourceforge_button.set_size_request(80, 40)

        buttons_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        buttons_box2.pack_start(telegram_button, False, False, 0)
        buttons_box2.pack_start(github_button, False, False, 0)
        buttons_box2.pack_end(exit_button, False, False, 0)
        buttons_box2.pack_end(reddit_button, False, False, 0)
        buttons_box2.pack_end(sourceforge_button, False, False, 0)

        main_box.pack_end(buttons_box2, False, False, 0)

        self.setup_image_viewer()

        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("scroll-event", self.on_scroll_event)

        self.connect("key-press-event", self.on_key_press_event)

        self.check_startup_config()

    def setup_image_viewer(self):
        image_viewer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        toolbar_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image_viewer_box.pack_end(toolbar_box, False, False, 0)

        back_button = Gtk.Button(label="Atrás")
        back_button.connect("clicked", self.on_back_button_clicked)
        toolbar_box.pack_start(back_button, False, False, 0)

        next_button = Gtk.Button(label="Siguiente")
        next_button.connect("clicked", self.on_next_button_clicked)
        toolbar_box.pack_end(next_button, False, False, 0)

        self.image_viewer = Gtk.Image()
        image_viewer_box.pack_start(self.image_viewer, True, True, 0)

        self.stack.add_named(image_viewer_box, "image_viewer")

    def on_startup_toggled(self, button):
        if button.get_active():
            self.set_startup_config(True)
        else:
            self.set_startup_config(False)

    def check_startup_config(self):
        config = configparser.ConfigParser()
        config_file = 'config.inf'
        if os.path.exists(config_file):
            config.read(config_file)
            if config.has_section('Startup'):
                startup_enabled = config.getboolean('Startup', 'Enabled')
                self.startup_checkbutton.set_active(startup_enabled)

    def set_startup_config(self, enabled):
        config = configparser.ConfigParser()
        config['Startup'] = {'Enabled': str(enabled)}
        with open('config.inf', 'w') as configfile:
            config.write(configfile)

        if enabled:
            self.create_autostart_file()
        else:
            self.remove_autostart_file()

    def create_autostart_file(self):
        desktop_file_path = os.path.expanduser('~/.config/autostart/welcome.desktop')
        desktop_file_content = (
            "[Desktop Entry]\n"
            "Type=Application\n"
            "Exec=python3 /usr/share/welcome_cuerd/welcome.py\n"
            "Hidden=false\n"
            "NoDisplay=false\n"
            "X-GNOME-Autostart-enabled=true\n"
            "Name[en_US]=Welcome\n"
            "Name=Welcome\n"
        )
        try:
            with open(desktop_file_path, 'w') as desktop_file:
                desktop_file.write(desktop_file_content)
        except Exception as e:
            print(f"Error al crear el archivo de autostart: {e}")

    def remove_autostart_file(self):
        desktop_file_path = os.path.expanduser('~/.config/autostart/welcome.desktop')
        if os.path.exists(desktop_file_path):
            os.remove(desktop_file_path)

    def on_web_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://cuerdos.github.io/"])

    def on_extras_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://github.com/gatoverde95/CuerdOS-Extras"])

    def on_tools_button_clicked(self, button):
        print("Acceder a herramientas")

    def on_apps_button_clicked(self, button):
        self.stack.set_visible_child_name("image_viewer")
        self.show_navigation_buttons()
        self.image_paths = [
            os.path.join(self.images_folder, "imag1.png"),
            os.path.join(self.images_folder, "imag2.png"),
            os.path.join(self.images_folder, "imag3.png"),
            os.path.join(self.images_folder, "imag4.png")
        ]
        self.current_image_index = 0
        self.image_viewer.set_from_file(self.image_paths[self.current_image_index])

    def on_more_games_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://github.com/gatoverde95/CuerdOS-Extras-Games"])

    def on_changelog_button_clicked(self, button):
        changelog_path = "/usr/share/welcome_cuerd/data/changelog.txt"  # Reemplaza "/path/to/changelog.txt" con la ruta real de tu archivo de registro de cambios
        if os.path.exists(changelog_path):
            subprocess.Popen(["gedit", changelog_path])  # Cambia "gedit" por tu editor de texto preferido si no estás usando GNOME gedit
        else:
            print("El archivo de registro de cambios no existe en la ruta especificada:", changelog_path)

    def on_exit_button_clicked(self, button):
        Gtk.main_quit()

    def on_telegram_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://t.me/+GibSWjFc89Q2ODU8"])

    def on_github_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://github.com/CuerdOS"])

    def on_reddit_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://www.reddit.com/r/CuerdOS/"])

    def on_sourceforge_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://sourceforge.net/projects/cuerdos/"])

    def on_documentation_button_clicked(self, button):
        self.stack.set_visible_child_name("image_viewer")
        self.show_navigation_buttons()
        self.image_paths = [
            os.path.join(self.images_folder, "doc1.png"),
            os.path.join(self.images_folder, "doc2.png"),
            os.path.join(self.images_folder, "doc3.png"),
            os.path.join(self.images_folder, "doc4.png")
        ]
        self.current_image_index = 0
        self.image_viewer.set_from_file(self.image_paths[self.current_image_index])

    def on_back_button_clicked(self, button):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_viewer.set_from_file(self.image_paths[self.current_image_index])
        else:
            self.stack.set_visible_child_name("main_box")
            self.hide_navigation_buttons()

    def on_next_button_clicked(self, button):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.image_viewer.set_from_file(self.image_paths[self.current_image_index])

    def hide_navigation_buttons(self):
        pass

    def show_navigation_buttons(self):
        pass

    def on_scroll_event(self, widget, event):
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.on_back_button_clicked(None)
        elif event.direction == Gdk.ScrollDirection.UP:
            self.on_next_button_clicked(None)

    def on_key_press_event(self, widget, event):
        keyval = event.keyval
        if keyval == Gdk.KEY_Left:
            self.on_back_button_clicked(None)
        elif keyval == Gdk.KEY_Right:
            self.on_next_button_clicked(None)

def run():
    win = WelcomeWindow()
    win.connect("destroy", Gtk.main_quit)
    win.set_position(Gtk.WindowPosition.CENTER)  # Centra la ventana en la pantalla
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    run()
