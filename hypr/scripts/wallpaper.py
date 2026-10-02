import os
import random
papers = ["win11_2.jpg","storm.png","LinuxGirl2.jpg","win2000.png","whitenblue.jpg","pixelcity.png","cigarrete.jpg","win11.jpg","thecoolest4.jpg","blue.png","eletric.jpg","teto.png","animecute.jpg","rei.png","lainwwin1.png","blacklinux.jpg","forest.jpg","thecoolest.jpg","retrowin.png","bluepixel.png","mikushop.jpg","cuteanime.png","linuxkillwin.jpg"]
wallpaper=random.choice(papers)
file = open("/home/wiredgod/.config/hypr/hyprpaper.conf","w")
file.writelines(
        ["wallpaper{\n"," monitor=eDP-1\n", f"path= ~/Wallpapers/{wallpaper}\n", "fit_mode=center\n","}\n","splash=false"]
        )
file.close()
os.system('killall hyprpaper && hyprpaper')
