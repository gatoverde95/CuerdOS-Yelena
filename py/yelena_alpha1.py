import os
import gi
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class WelcomeWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title("CuerdOS Yelena Hi!!")  # Modificación del título de la ventana

        self.set_default_size(600, 480)
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
        banner_path = os.path.join("/usr/share/welcome_cuerd/banner.png")
        if os.path.exists(banner_path):
            banner_image.set_from_file(banner_path)
            banner_image.set_size_request(645, 258)
            main_box.pack_start(banner_image, False, False, 0)

        welcome_label = Gtk.Label()
        welcome_label.set_text("Hola!! Bienvenido a CuerdOS GNU/Linux")
        main_box.pack_start(welcome_label, True, True, 0)

        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        icon_folder = "/usr/share/welcome_cuerd/icons/"
        self.images_folder = "/usr/share/welcome_cuerd/images/"

        button_data = [
            ("Web oficial", "web.png", self.on_web_button_clicked),
            ("Extras", "extras.png", self.on_extras_button_clicked),
            ("Sobre la Distribución", "documentation.png", self.on_documentation_button_clicked),
            ("Lista de Aplicaciones", "apps.png", self.on_apps_button_clicked),
            ("Más Juegos...", "games.png", self.on_more_games_button_clicked)
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
        exit_image = Gtk.Image.new_from_file(os.path.join(icon_folder, "exit.png"))
        exit_button.set_image(exit_image)
        exit_button.set_label("Salir")
        exit_button.set_always_show_image(True)
        exit_button.connect("clicked", self.on_exit_button_clicked)
        exit_button.set_size_request(80, 40)
        
        telegram_button = Gtk.Button(label="CuerdOS Feedback")
        telegram_button.set_image(Gtk.Image.new_from_file(os.path.join(icon_folder, "telegram.png")))
        telegram_button.connect("clicked", self.on_telegram_button_clicked)
        telegram_button.set_size_request(80, 40)

        github_button = Gtk.Button(label="GitHub")
        github_button.set_image(Gtk.Image.new_from_file(os.path.join(icon_folder, "github.png")))
        github_button.connect("clicked", self.on_github_button_clicked)
        github_button.set_size_request(80, 40)

        buttons_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        buttons_box2.pack_end(exit_button, False, False, 0)
        buttons_box2.pack_end(telegram_button, False, False, 0)
        buttons_box2.pack_end(github_button, False, False, 0)
        
        main_box.pack_end(buttons_box2, False, False, 0)

        startup_check = Gtk.CheckButton(label="No iniciar al encender")
        main_box.pack_end(startup_check, False, False, 0)

        # Image Viewer
        self.image_viewer = Gtk.Image()
        self.stack.add_named(self.image_viewer, "image_viewer")
        self.image_paths = [
            os.path.join(self.images_folder, "doc1.png"),
            os.path.join(self.images_folder, "doc2.png"),
            os.path.join(self.images_folder, "doc3.png")
        ]
        self.current_image_index = 0
        self.image_viewer.set_from_file(self.image_paths[self.current_image_index])

        self.setup_header_bar()
        self.hide_navigation_buttons()

        # Conectar eventos para la navegación con la rueda del mouse
        self.add_events(Gdk.EventMask.SCROLL_MASK)
        self.connect("scroll-event", self.on_scroll_event)

        # Conectar eventos para la navegación con botones de dirección
        self.connect("key-press-event", self.on_key_press_event)

    def setup_header_bar(self):
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Bienvenido a CuerdOS"

        self.back_button = Gtk.Button()
        self.back_button.add(Gtk.Image.new_from_icon_name("go-previous", Gtk.IconSize.BUTTON))
        self.back_button.connect("clicked", self.on_back_button_clicked)
        self.header.pack_start(self.back_button)

        self.next_button = Gtk.Button()
        self.next_button.add(Gtk.Image.new_from_icon_name("go-next", Gtk.IconSize.BUTTON))
        self.next_button.connect("clicked", self.on_next_button_clicked)
        self.header.pack_start(self.next_button)

        self.set_titlebar(self.header)

    def on_web_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://cuerdos.github.io/index_es.html"])

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
            os.path.join(self.images_folder, "imag4.png"),
            os.path.join(self.images_folder, "imag5.png")
        ]
        self.current_image_index = 0
        self.image_viewer.set_from_file(self.image_paths[self.current_image_index])

    def on_more_games_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://github.com/gatoverde95/CuerdOS-Extras-Games"])

    def on_exit_button_clicked(self, button):
        Gtk.main_quit()

    def on_telegram_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://t.me/+GibSWjFc89Q2ODU8"])

    def on_github_button_clicked(self, button):
        subprocess.Popen(["firefox", "https://github.com/CuerdOS"])

    def on_documentation_button_clicked(self, button):
        self.stack.set_visible_child_name("image_viewer")
        self.show_navigation_buttons()
        self.image_paths = [
            os.path.join(self.images_folder, "doc4.png"),
            os.path.join(self.images_folder, "doc5.png"),
            os.path.join(self.images_folder, "doc6.png"),
            os.path.join(self.images_folder, "doc7.png")
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
        self.back_button.hide()
        self.next_button.hide()

    def show_navigation_buttons(self):
        self.back_button.show()
        self.next_button.show()

    # Manejar el evento de desplazamiento de la rueda del mouse
    def on_scroll_event(self, widget, event):
        if event.direction == Gdk.ScrollDirection.DOWN:
            self.on_back_button_clicked(None)
        elif event.direction == Gdk.ScrollDirection.UP:
            self.on_next_button_clicked(None)

    # Manejar el evento de pulsación de tecla
    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_Left:
            self.on_back_button_clicked(None)
        elif event.keyval == Gdk.KEY_Right:
            self.on_next_button_clicked(None)

win = WelcomeWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
