import gi
import socket
import webbrowser
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

report = "http://www.example.com"

def on_delete_event(widget, event):
    # Returning True to prevent the window from being closed
    return True


def send_message(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9999))
    client.send(message.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    client.close()
    return response

def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_title("LX's Help!")
    win.set_default_size(300, 300)
    win.set_resizable(False)
    win.set_size_request(300, 300)
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
    win.entry = Gtk.Entry()
    win.label = Gtk.Label(label="Go ahead! Ask a question! This is an early alpha release of the new, fast, lightweight and innovative LXM (Lightning X Machine) model. It does not have many words, nor can it remember things that were said previously, but it sure can try! To ensure maximum success of this simple AI, keep questions short and try not to use fancy or uncommon words. Version 0.1A.")
    win.label.set_wrap(True)
    vbox.append(win.entry)
    buttonone = Gtk.Button(label="Ask question")
    buttontwo = Gtk.Button(label="Report a bug")
    hbox.append(buttonone)
    hbox.append(buttontwo)
    vbox.append(hbox)
    vbox.append(win.label)
    buttonone.connect('clicked', lambda x: win.label.set_text(send_message(win.entry.get_text())))
    buttontwo.connect('clicked', lambda x: webbrowser.open(report, new=2))
    win.set_child(vbox)  # Set the vbox as the child of the window
    win.present()

app = Gtk.Application(application_id='org.gtk.lxhelp')
app.connect('activate', on_activate)
app.run(None)

