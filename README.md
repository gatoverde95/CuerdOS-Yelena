<!-- Logo -->
<p align="center">
  <img src="/img/yen.png" alt="Logo" width="300" height="300">
</p>

Es un tema diseñado y adaptado para CuerdOS GNU/Linux, para LightDM. Estara disponible en la version Legacy.

| Captura de pantalla |
| ------------------ |
| ![Standard Edition](/cuerd-png/lightdm.png) |

## ANTES DE INSTALAR, DEBES DESCARGAR LAS SIGUIENTES DEPENDENCIAS:

- lightdm
- lightdm-gtk-greeter
- lightdm-gtk-greeter-settings
- orchis-gtk-theme
- slick-greeter

Comando (Abre sakura): `sudo apt install lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings orchis-gtk-theme slick-greeter`

## INSTALACIÓN:

1. Abre sakura, luego ingresa `sudo su` y proporciona la contraseña.

2. Ejecuta el explorador de archivos como usuario Root:

   | Entorno de Escritorio | Comando       |
   |------------------------|---------------|
   | Cinnamon               | `sudo nemo`   |
   | MATE                   | `sudo caja`   |
   | Xfce                   | `sudo thunar` |
   | LXQt                   | `sudo pcmanfm-qt` |
   | LXDE                   | `sudo pcmanfm`    |
   | i3/Sway                | `sudo nemo`       |

3. Luego, busca el disco local y navega a la siguiente dirección:
   `/etc/lightdm/`
   
4. Copia todo lo de la carpeta del tema de LightDM
   `CuerdOS LightDM Theme/files/etc/lightdm` a `/etc/lightdm/`.

5. Copia los archivos del tema a la siguiente carpeta:
   `/CuerdOS LightDM Theme/files/usr/share/backgrounds/lightdm` a `/usr/share/backgrounds/`.

6. Después de haber instalado la configuración y parte del tema, sigue estos pasos:
   - Abre sakura.
   - Ejecuta `sudo su`.
   - Luego, ejecuta `sudo dpkg-reconfigure lightdm`.

7. ¡Reinicia tu máquina y listo!

## Descarga
Esta en el apartado de Lanzamientos se encuentra un .tar.gz
