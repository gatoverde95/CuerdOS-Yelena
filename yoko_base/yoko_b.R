if (!require("RGtk2")) {
  install.packages("RGtk2")
}
library(RGtk2)

onDestroy <- function(widget, event) {
  gtkMainQuit()
}

window <- gtkWindow(show = FALSE)
window$setSizeRequest(640, 480)

gSignalConnect(window, "destroy", onDestroy)

vbox <- gtkVBox(FALSE, 5)

for (i in 1:10) {
  button <- gtkButton(label = paste("Button", i))
  vbox$packStart(button, FALSE, FALSE, 0)
}

window$add(vbox)

window$showAll()

gtkMain()

