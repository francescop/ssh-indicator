from gi.repository import Gtk as gtk
from ssh_indicator import SshIndicator

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    indicator = SshIndicator()
    main()
