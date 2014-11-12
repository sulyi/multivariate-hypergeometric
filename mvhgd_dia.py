#/usr/bin/env python
#-*- coding: UTF-8 -*-

#.dia/python/mvhgd_dia.py

"""
Created on 2013.11.03.

@author: Ákos Sülyi
"""

# FIXME: broken, due to use of obsolete twmatrix
# TODO: create support for twmatrix compatibility

import dia


class CInputDialog:
    def __init__(self, d, data):
        import pygtk
        pygtk.require("2.0")
        import gtk
        win = gtk.Window()
        win.connect("delete_event", self.on_delete)
        win.set_title("Input")

        self.diagram = d
        self.data = data
        self.win = win
        self.error = gtk.MessageDialog(parent=self.win, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
        self.e_response = gtk.RESPONSE_OK
        
        box1 = gtk.VBox()
        win.add(box1)
        box1.show()
        
        box2 = gtk.VBox(spacing=10)
        box2.set_border_width(10)
        box1.pack_start(box2)
        box2.show()
        
        label1 = gtk.Label(
            "Please specify the number of elements by each category\n"
            "separated with comma and/or semicolon, space, line-breaks")
        label1.set_alignment(0, 0)
        box2.pack_start(label1, False, False)
        label1.show()
        
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        tv = gtk.TextView()
        tv.set_wrap_mode(gtk.WRAP_CHAR)
        self.text = tv.get_buffer()
        tv.set_editable(True)
        sw.add(tv)
        sw.show()
        tv.show()
        
        box2.pack_start(sw)
        
        separator = gtk.HSeparator()
        box1.pack_start(separator, expand=0)
        separator.show()

        box2 = gtk.VBox(spacing=10)
        box2.set_border_width(10)
        box1.pack_start(box2, expand=0)
        box2.show()
        
        box3 = gtk.HButtonBox()
        box3.set_layout(gtk.BUTTONBOX_END)
        box2.pack_start(box3)
        box3.show()
        
        button = gtk.Button("Ok")
        button.connect("clicked", self.on_draw)
        box3.pack_start(button)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()
        button.show()
        
        win.show()

    def on_draw(self, *args):
        instr = self.text.get_text(*self.text.get_bounds())
        # processing input text
        instr = instr.replace(" ", ",")
        instr = instr.replace(";", ",")
        instr = instr.replace("\n", ",")
        
        array = list()
        errors = list()
                
        for i in instr.split(","):
            try:
                if len(i):
                    array.append(int(i))
            except ValueError as e:
                errors.append(e.message)

        if not errors and array:
            draw_lattice(self.data, array)
            self.win.destroy()
        else:
            self.error.set_markup('\n\n'.join(("Invalid value for a number", '\n'.join(errors))))
            if self.error.run() == self.e_response:
                self.error.hide()

    def on_delete(self, *args):
        self.win.destroy()


def mvhgd_cb(data, flags):
    dlg = CInputDialog(dia.active_display().diagram, data)


def draw_lattice(data, array):
    import mvhgd
    if data:
        diagram = dia.active_display().diagram 
    else:
        diagram = dia.new("Hello_world.dia")
        data = diagram.data
    layer = data.active_layer
    
    lattice = mvhgd.Grid(array)
    droot = next(lattice)[0]
    
    drawn = list()
    
    root, h1, h2 = dia.get_object_type("Flowchart - Ellipse").create(0, 0)
    root.properties["text"] = ','.join(map(str, droot))
    
    height = len(droot) * root.properties["elem_height"].value
    width = root.properties["elem_width"].value + 1
    layer.add_object(root)
    
    prev = [root]
    
    y = 0
    x = 0
        
    for n, level in enumerate(lattice):
        y += height
        x = width * (len(level) - 1) / -2.0
        
        following = list()
        drawptr = [ level.parent._read_len_tab( n, i ) for i in range( 1, level.parent.m ) ]
        drawptr.append( 0 )
    
        for drawing in level:
            o, oh1, oh2 = dia.get_object_type("Flowchart - Ellipse").create(x, y)
            o.properties["text"] = ','.join(map(str, drawing))
            following.append(o)
            layer.add_object(o)
            x += width
            for k in range(level.parent.m):
                if drawing[k] < droot[k]:
                    line, lh1, lh2 = dia.get_object_type("Standard - Line").create(0, 0)
                    layer.add_object(line)
                    lh1.connect(prev[drawptr[k]].connections[16])
                    lh2.connect(o.connections[16])
                    diagram.update_connections(prev[drawptr[k]])
                    print '\t', drawptr[k]
                    drawptr[k] += 1
            
        prev = following

    dia.active_display().add_update_all()
    diagram.flush()
    return data

dia.register_action("mvhgd", "Haase diagram of a multivariate hypergeometric distribution",
                    "/DisplayMenu/Dialogs/DialogsExtensionStart",
                    mvhgd_cb)
