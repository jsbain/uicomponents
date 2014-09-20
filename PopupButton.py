import ui, threading, time
from initializer import initializer


class PopupButton (ui.View):
    # a button like class, which allows for long touch popup
#    @initializer
    def __init__(self, 
                 frame=(0, 0, 100, 100), 
                 title='',
                 flex='', 
                 background_color=(.8,.8,.8), 
                 longtouch_delay=0.5,
                 touch_enabled=True,
                 border_color=(0,0,0),
                 border_width=1,
                 corner_radius=10):
        self.frame=frame
        self.title=title
        self.flex=''
        self.background_color=background_color
        self.longtouch_delay=longtouch_delay
        self.touch_enabled=touch_enabled
        self.border_color=border_color
        self.border_width=border_width
        self.corner_radius=corner_radius
        self.multitouch_enabled=False 

        self.doing_longtouch=False #is long touch activated
        self.touched=False         #currently touching button
        self.t =  None


        self.title=''
        def action(sender):
            pass
        self.action = action
    def add_subview(self,subview):
        #override View to set hidden
        subview.hidden=True
        ui.View.add_subview(self,subview)
    def get_top_view(self):
        temp=self
        while temp.superview:
            temp=temp.superview
        return temp

    def did_load(self):
        # This will be called when a view has been fully loaded from a UI file.
        pass

    def will_close(self):
        # This will be called when a presented view is about to be dismissed.
        # You might want to save data here.
        t.stop()
        pass


        
    def draw(self):
        # This will be called whenever the view's content needs to be drawn.
        # You can use any of the ui module's drawing functions here to render
        # content into the view's visible rectangle.
        # Do not call this method directly, instead, if you need your view
        # to redraw its content, call set_needs_display().
        # Example:
        def darken(color):
            return tuple([0.5*x for x in color])
        ui.set_color(self.border_color)
        path = ui.Path.rounded_rect(0, 0, self.width, self.height,self.corner_radius)
        path.line_width=self.border_width
        path.stroke()

        if self.touched:
            if self.doing_longtouch:
                ui.set_color('blue')
            else:
                ui.set_color(darken(self.bg_color))
        else :
            ui.set_color(self.bg_color)
        
        path.fill()
        # fill corner darker
        corner = ui.Path()
        corner.move_to(self.width-self.corner_radius,0)
        corner.line_to(self.width,0)
        corner.line_to(self.width,self.corner_radius)
        corner.line_to(self.width-self.corner_radius,0)
        ui.set_color(darken(darken(self.bg_color)))
        corner.stroke()
        corner.fill()
        ui.draw_string(self.title, rect=self.bounds, font=('<system>', 12), color=self.tint_color, alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)

    def layout(self):
        # This will be called when a view is resized. You should typically set the
        # frames of the view's subviews here, if your layout requirements cannot
        # be fulfilled with the standard auto-resizing (flex) attribute.
        pass
   # @ui.in_background     
    def long_touch(self):
        if self.touched:
            self.doing_longtouch=True
            s=self.subviews[0]
            s.x=self.x
            s.y=self.y
            def pop():
                s.y=self.y-s.height-20
                s.x=self.x + 20
            ui.animate(pop,0.05)
            s.bg_color=self.bg_color
            s.border_color=self.border_color
            s.tint_color=self.tint_color
            s.hidden=False
            self.get_top_view().add_subview(s)
            self.set_needs_display()
        # todo, create root view popup.
        

    def touch_began(self, touch):
        # Called when a touch begins.
        # set timer for longtap, which gets cancelled in touch ended
        self.touched=True
        #self.t = threading.Timer(self.longtouch_delay, self.long_touch)
        #self.t.start()
        ui.delay(self.longtouch_delay, self.long_touch)

        self.doing_longtouch=False
        self.set_needs_display()
        self.lastTouchTime=time.time()
        pass
        
    def childHits(self,location):
        for s in self.subviews:
            if PopupButton.hit(s,ui.convert_point(location,self,s)):
                s.bg_color=(0,0,1)
                yield s
            else :
                s.bg_color=(.8,.8,.8) 

    @staticmethod
    def hit(self,location):
        if location[0]<0 or location[1]<0 or location[0]>self.width or location[1]>self.height:
            return False
        else :
            return True 
            
    def touch_moved(self, touch):
        # Called when a touch moves.
        #if not self.doing_longtouch:


        t= time.time()
        if t<self.lastTouchTime +0.1:
            return
        if self.doing_longtouch:
            for s in self.childHits(touch.location):
                pass


                
        elif not PopupButton.hit(self,touch.location):
          if self.touched :
            self.touched=False
            self.longtouch_cleanup()
            self.set_needs_display()
        elif not self.touched:
            self.touched=True
            self.doing_longtouch=False
            self.longtouch_cleanup()
            self.touch_began(touch)
        self.lastTouchTime=t

        
        #pass
    def longtouch_cleanup(self):
        for s in self.subviews:
            self.get_top_view().remove_subview(s)
    
    def touch_ended(self, touch):
        # Called when a touch ends.  if touch ended before timer, cancel it
        #self.t.cancel()
        ui.cancel_delays()
        if self.doing_longtouch:
            for  s in self.childHits(touch.location):
                s.action(s)
        elif self.touched:
            #normal button action
            self.touched=False
            self.set_needs_display()
            self.action(self)
        else:
            return
        self.doing_longtouch=False 
        self.touched=False
        self.set_needs_display()
        self.longtouch_cleanup()

    def keyboard_frame_will_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

    def keyboard_frame_did_change(self, frame):
        # Called when the on-screen keyboard appears/disappears
        # Note: The frame is in screen coordinates.
        pass

b = PopupButton()


b2=ui.Button()
b2.title='test'
b.width=40
b.height=40
b.corner_radius=5
b.title='Push'


b2.bg_color=(1,0,0)
b2.name='tempbutton'
b2.size_to_fit()
b.add_subview(b2)
def butt(sender):
     print 'butt'
b.action=butt
def butt2(sender):
    print 'shit it works'
    
b2.action=butt2

v=ui.View(name='top')
v2=ui.View(name='next')
v.add_subview(v2)
v2.add_subview(b)
print b.get_top_view().name
b.y=50
v.present('sheet')
