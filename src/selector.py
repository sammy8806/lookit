import cairo
import gtk
import gtk.gdk

import screencapper

class Selector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0

        self.is_composited = False
        self.supports_alpha = False
        self.mouse_down = False

        self.pixbuf = None

        self.overlay = gtk.Window(gtk.WINDOW_POPUP)

        self.overlay.set_app_paintable(True)
        self.overlay.set_decorated(False)

        self.overlay.add_events(gtk.gdk.POINTER_MOTION_MASK |
                                gtk.gdk.BUTTON_PRESS_MASK |
                                gtk.gdk.BUTTON_RELEASE_MASK |
                                gtk.gdk.KEY_PRESS_MASK)

        self.overlay.connect('expose-event',            self.expose)
        self.overlay.connect('screen-changed',          self.screen_changed)
        self.overlay.connect('realize',                 self.realize)
        self.overlay.connect('show',                    self.on_show)
        self.overlay.connect('button-press-event',      self.button_pressed)
        self.overlay.connect('button-release-event',    self.button_released)
        self.overlay.connect('motion-notify-event',     self.motion_notify)
        self.overlay.connect('key-press-event',         self.key_pressed)

    def expose(self, widget, event=None):
        cr = widget.window.cairo_create()
        if self.is_composited and self.supports_alpha and not self.ffb:
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.set_source_rgba(0, 0, 0, 0)
            cr.paint()
            if self.mouse_down:
                cr.rectangle(self.x, self.y, self.dx, self.dy)
            
        else:
            cr.set_operator(cairo.OPERATOR_SOURCE)
            if self.pixbuf is None:
                self.pixbuf = screencapper.capture_screen()
                cr.set_source_pixbuf(self.pixbuf, 0, 0)
                cr.paint()

            if self.mouse_down:
                cr.rectangle(self.x, self.y, self.dx, self.dy)
                cr.stroke()
        
        return False

    def undraw_rect(self, widget):
        cr = widget.window.cairo_create()
        cr.set_source_pixbuf(self.pixbuf, 0, 0)
        cr.rectangle(self.x, self.y, self.dx, self.dy)
        cr.stroke()

    def screen_changed(self, widget, old_screen=None):
        screen = widget.get_screen()
        self.is_composited = screen.is_composited()
        widget.move(0, 0)
        widget.resize(screen.get_width(), screen.get_height())

        colormap = screen.get_rgba_colormap()
        if colormap == None:
            colormap = screen.get_rgb_colormap()
            self.supports_alpha = False
        else:
            self.supports_alpha = True

        widget.set_colormap(colormap)

        return True

    def realize(self, widget):
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSS))

    def on_show(self, widget):
        gtk.gdk.keyboard_grab(widget.window)

    def button_pressed(self, widget, event):
        self.mouse_down = True
        self.x = event.x
        self.y = event.y

    def button_released(self, widget, event):
        self.mouse_down = False
        gtk.main_quit()
        self.overlay.destroy()

    def motion_notify(self, widget, event):
        if self.mouse_down:
            if not self.is_composited or self.ffb:
                self.undraw_rect(widget)
            self.dx = event.x - self.x
            self.dy = event.y - self.y

            self.expose(self.overlay)

    def key_pressed(self, widget, event):
        if event.keyval == gtk.gdk.keyval_from_name('Escape'):
            self.button_released(widget, event)
        else:
            return False

    def selection_rectangle(self):
        if self.dx == 0 or self.dy == 0:
            return None
        if self.dx < 0:
            self.x += self.dx
            self.dx = -self.dx
        if self.dy < 0:
            self.y += self.dy
            self.dy = -self.dy
        return int(self.x), int(self.y), int(self.dx), int(self.dy)


    def get_selection(self, ffb=False):
        self.ffb = ffb
        self.screen_changed(self.overlay)
        self.overlay.show_all()
        gtk.main()
        return self.selection_rectangle()

if __name__ == '__main__':
    # For testing purposes only
    print (Selector().get_selection())
