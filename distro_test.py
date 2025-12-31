from conchfetch import print_info
import conchfetch

print("test distro logos")

distro = input("> ")
conchfetch.get_distro_name = lambda: distro

print_info()