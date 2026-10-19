<img width="250" height="350" alt="image" src="https://github.com/user-attachments/assets/da78fd4a-07e4-4b58-a4a6-612d8ec578d0" />



# 1. Enable multilib repository non-interactively
sudo sed -i '/\[multilib\]/,/Include/'\''s/^#//' /etc/pacman.conf

# 2. Execute a single, atomic system upgrade and package installation
sudo pacman -Syu --needed --noconfirm \
  linux-firmware archlinux-xdg-menu reflector man-db man-pages git base-devel btop wget curl unzip zip eza ripgrep fuse2 openssh \
  amd-ucode mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon libva-mesa-driver lib32-libva-mesa-driver libva-utils vulkan-tools \
  hyprland hyprpaper hypridle hyprlock hyprpicker hyprpolkitagent xdg-desktop-portal-hyprland xdg-desktop-portal-gtk xdg-user-dirs \
  waybar wofi kitty dunst nautilus qt5-wayland qt6-wayland xwayland pipewire wireplumber pipewire-pulse pipewire-alsa pipewire-jack pavucontrol libnotify \
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-jetbrains-mono papirus-icon-theme nwg-look \
  cups cups-browsed avahi nss-mdns hplip system-config-printer \
  mpv vlc ffmpeg gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav \
  obs-studio v4l2loopback-dkms linux-headers wf-recorder grim slurp swappy kdenlive blender audacity krita gimp tenacity wl-clipboard \
  steam lutris wine wine-gecko wine-mono gamemode lib32-gamemode mangohud lib32-mangohud goverlay protontricks

# 3. Enable and start system-level daemons (Networking, Bluetooth, Printing, Discovery)
sudo systemctl enable --now NetworkManager bluetooth cups avahi-daemon

# 4. Enable and start user-level audio subsystem (PipeWire)
systemctl --user enable --now pipewire pipewire-pulse wireplumber# 1. Enable multilib repository non-interactively
sudo sed -i '/\[multilib\]/,/Include/'\''s/^#//' /etc/pacman.conf

# 2. Execute a single, atomic system upgrade and package installation
sudo pacman -Syu --needed --noconfirm \
  linux-firmware archlinux-xdg-menu reflector man-db man-pages git base-devel btop wget curl unzip zip eza ripgrep fuse2 openssh \
  amd-ucode mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon libva-mesa-driver lib32-libva-mesa-driver libva-utils vulkan-tools \
  hyprland hyprpaper hypridle hyprlock hyprpicker hyprpolkitagent xdg-desktop-portal-hyprland xdg-desktop-portal-gtk xdg-user-dirs \
  waybar wofi kitty dunst nautilus qt5-wayland qt6-wayland xwayland pipewire wireplumber pipewire-pulse pipewire-alsa pipewire-jack pavucontrol libnotify \
  noto-fonts noto-fonts-cjk noto-fonts-emoji ttf-jetbrains-mono papirus-icon-theme nwg-look \
  cups cups-browsed avahi nss-mdns hplip system-config-printer \
  mpv vlc ffmpeg gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav \
  obs-studio v4l2loopback-dkms linux-headers wf-recorder grim slurp swappy kdenlive blender audacity krita gimp tenacity wl-clipboard \
  steam lutris wine wine-gecko wine-mono gamemode lib32-gamemode mangohud lib32-mangohud goverlay protontricks

# 3. Enable and start system-level daemons (Networking, Bluetooth, Printing, Discovery)
sudo systemctl enable --now NetworkManager bluetooth cups avahi-daemon

# 4. Enable and start user-level audio subsystem (PipeWire)
systemctl --user enable --now pipewire pipewire-pulse wireplumber
