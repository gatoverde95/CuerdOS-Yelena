if (!require("RGtk2")) {
  install.packages("RGtk2")
}
library(RGtk2)

onDestroy <- function(widget, event) {
  gtkMainQuit()
}

posicionar_botones <- function() {
  radio <- 150
  centro_x <- 200
  centro_y <- 200
  num_botones <- 8

  for (i in 1:num_botones) {
    angulo <- 2 * pi * i / num_botones
    x <- centro_x + radio * cos(angulo)
    y <- centro_y + radio * sin(angulo)
    botones[[i]]$setAllocation(as.integer(x), as.integer(y), -1, -1)
  }
}

window <- gtkWindow(show = FALSE)
window$setSizeRequest(400, 400)

gSignalConnect(window, "destroy", onDestroy)

box <- gtkFixed()
botones <- list()

for (i in 1:8) {
  button <- gtkButton(label = paste("Botón", i))
  botones[[i]] <- button
  box$put(button, 0, 0)
}

window$add(box)
posicionar_botones()
window$showAll()
gtkMain()
