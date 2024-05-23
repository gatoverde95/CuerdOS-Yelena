package main

import (
    "log"
    "os"
    "os/exec"
    "github.com/gotk3/gotk3/gtk"
)

func main() {
    gtk.Init(nil)

    win, err := gtk.WindowNew(gtk.WINDOW_TOPLEVEL)
    if err != nil {
        log.Fatal("Unable to create window:", err)
    }
    win.SetTitle("CuerdOS Yelena 1.1a Sonia")
    win.SetDefaultSize(600, 480)
    win.SetPosition(gtk.WIN_POS_CENTER)
    win.SetResizable(false)

    if _, err := os.Stat("/usr/share/welcome_cuerd/cuerd.png"); err == nil {
        pixbuf, _ := gdk.PixbufNewFromFile("/usr/share/welcome_cuerd/cuerd.png")
        win.SetIcon(pixbuf)
    } else {
        log.Println("El archivo de icono no existe en la ruta especificada")
    }

    stack, _ := gtk.StackNew()
    stackSwitcher, _ := gtk.StackSwitcherNew()
    stackSwitcher.SetStack(stack)
    stack.SetTransitionType(gtk.STACK_TRANSITION_TYPE_SLIDE_LEFT_RIGHT)
    stack.SetTransitionDuration(1000)

    mainBox, _ := gtk.BoxNew(gtk.ORIENTATION_VERTICAL, 6)
    stack.Add(mainBox, "main_box")

    bannerImage, _ := gtk.ImageNew()
    if _, err := os.Stat("/usr/share/welcome_cuerd/banner.png"); err == nil {
        bannerImage.SetFromFile("/usr/share/welcome_cuerd/banner.png")
        bannerImage.SetSizeRequest(645, 258)
        mainBox.PackStart(bannerImage, false, false, 0)
    }

    welcomeLabel, _ := gtk.LabelNew("Hola!! Bienvenido a CuerdOS GNU/Linux | Cessna 1.1")
    welcomeLabel.SetMarkup("<big><b>" + welcomeLabel.GetText() + "</b></big>")
    mainBox.PackStart(welcomeLabel, true, true, 0)

    startupCheckButton, _ := gtk.CheckButtonNewWithLabel("Iniciar al encender el equipo")
    mainBox.PackStart(startupCheckButton, false, false, 0)

    buttonsBox, _ := gtk.BoxNew(gtk.ORIENTATION_HORIZONTAL, 12)
    buttonsBox.SetMarginTop(12)
    buttonsBox.SetMarginBottom(12)
    buttonsBox.SetCenterWidget(gtk.NewLabel("")) // Espaciado central

    iconFolder := "/usr/share/welcome_cuerd/icons/"
    imagesFolder := "/usr/share/welcome_cuerd/images/"

    buttonData := [][]string{
        {"Pagina Oficial", "web.png", "https://cuerdos.github.io/index_es.html"},
        {"Extras", "extras.png", "https://github.com/gatoverde95/CuerdOS-Extras"},
        {"Informacion", "documentation.png", "documentation"},
        {"Aplicaciones", "apps.png", "apps"},
        {"Más Juegos...", "games.png", "https://github.com/gatoverde95/CuerdOS-Extras-Games"},
        {"Novedades", "changelog.png", "changelog"},
    }

    for _, data := range buttonData {
        button, _ := gtk.ButtonNewWithLabel(data[0])
        iconPath := iconFolder + data[1]
        if _, err := os.Stat(iconPath); err == nil {
            image, _ := gtk.ImageNewFromFile(iconPath)
            button.SetImage(image)
        }
        button.Connect("clicked", func() {
            switch data[2] {
            case "documentation":
                // Lógica para abrir la documentación
            case "apps":
                // Lógica para abrir las aplicaciones
            case "changelog":
                // Lógica para abrir el registro de cambios
            default:
                cmd := exec.Command("firefox", data[2])
                cmd.Start()
            }
        })
        buttonsBox.PackStart(button, true, true, 0)
    }

    mainBox.PackStart(buttonsBox, true, true, 0)

    exitButton, _ := gtk.ButtonNewWithLabel("Salir")
    exitButton.SetSizeRequest(120, 40)
    exitButton.GetStyleContext().AddClass("exit-button")
    exitButton.Connect("clicked", func() {
        gtk.MainQuit()
    })

    footerBox, _ := gtk.BoxNew(gtk.ORIENTATION_HORIZONTAL, 12)
    footerBox.SetMarginTop(12)
    footerBox.SetMarginBottom(12)
    footerBox.SetCenterWidget(gtk.NewLabel("")) // Espaciado central
    footerBox.PackStart(exitButton, false, false, 0)

    mainBox.PackEnd(footerBox, false, false, 0)

    if err := win.Connect("destroy", func() {
        gtk.MainQuit()
    }); err != nil {
        log.Fatal("Unable to connect destroy signal:", err)
    }

    win.Add(stack)
    win.ShowAll()
    gtk.Main()
}
