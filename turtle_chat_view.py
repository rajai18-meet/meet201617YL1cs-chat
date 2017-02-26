#2016-2017 PERSONAL PROJECTS: TurtleChat!
#WRITE YOUR NAME HERE!
"Rajai"

import turtle
#import the Client class from the turtle_chat_client module
from turtle_chat_client import Client
#Finally, from the turtle_chat_widgets module, import two classes: Button and TextInput
from turtle_chat_widgets import Button, TextInput

class TextBox(TextInput):
    def draw_box(self):
        
        self.draw = turtle.clone()
        self.draw.hideturtle()
        self.draw.penup()
        self.draw.goto(self.width/2,0)
        self.draw.pendown()
        self.draw.goto(-self.width/2,0)
        self.draw.goto(-self.width/2,-self.height)
        self.draw.goto(self.width/2, -self.height)
        self.draw.goto(self.width/2,0)
      

    def write_msg(self):
        self.writer.clear()
        self.writer.write(self.new_msg, font=('Cambria', 17,))

    
class SendButton(Button):
    def __init__(self, view):
        super(SendButton,self).__init__(my_turtle=None, shape=None, pos=(0,-150))
        self.view=view
        
    def fun(self, x=None, y=None):
        self.view.send_msg()

class View:
    _MSG_LOG_LENGTH=5 #Number of messages to retain in view
    _SCREEN_WIDTH=300
    _SCREEN_HEIGHT=600
    _LINE_SPACING=round(_SCREEN_HEIGHT/2/(_MSG_LOG_LENGTH+1))

    def __init__(self,username='Me',partner_name='Partner'):

        self.username=username
        self.partner_name=partner_name
        self.my_client= Client()
        turtle.setup(width = self._SCREEN_WIDTH, height= self._SCREEN_HEIGHT)

        self.msg_queue=[]
        self.display=turtle.clone()
        self.display.hideturtle()
        self.display.penup()
        self.display.goto(-100,100)
        self.textbox = TextBox()
        self.sendbutton = SendButton(self)

        self.setup_listeners()
    
    def send_msg(self):
        '''
        You should implement this method.  It should call the
        send() method of the Client object stored in this View
        instance.  It should also call update the list of messages,
        self.msg_queue, to include this message.  It should
        clear the textbox text display (hint: use the clear_msg method).
        It should call self.display_msg() to cause the message
        display to be updated.
        '''
        self.my_client.send(self.textbox.new_msg)
        self.msg_queue.insert(0,self.textbox.new_msg)
        self.textbox.clear_msg()
        self.display_msg()

    def get_msg(self):
        return self.textbox.get_msg()

    def setup_listeners(self):
        '''
        Set up send button - additional listener, in addition to click,
        so that return button will send a message.
        To do this, you will use the turtle.onkeypress function.
        The function that it will take is
        self.send_btn.fun
        where send_btn is the name of your button instance

        Then, it can call turtle.listen()
        '''
        turtle.onkeypress(self.sendbutton.fun, 'Return')
        turtle.listen()

    def msg_received(self,msg):
        '''
        This method is called when a new message is received.
        It should update the log (queue) of messages, and cause
        the view of the messages to be updated in the display.

        :param msg: a string containing the message received
                    - this should be displayed on the screen
        '''
        print(msg) #Debug - print message
        show_this_msg=self.partner_name+' says:\r'+ msg
        self.msg_queue.insert(0,show_this_msg)
        self.display_msg()
        #Add the message to the queue either using insert (to put at the beginning)
        #or append (to put at the end).
        #
        #Then, call the display_msg method to update the display

    def display_msg(self):
        '''
        This method should update the messages displayed in the screen.
        You can get the messages you want from self.msg_queue
        '''
        self.display.clear()
        self.display.write(self.msg_queue[0])
##############################################################
##############################################################


#########################################################
#Leave the code below for now - you can play around with#
#it once you have a working view, trying to run you chat#
#view in different ways.                                #
#########################################################
if __name__ == '__main__':
    my_view=View()
    _WAIT_TIME=200 #Time between check for new message, ms
    def check() :
        msg_in=my_view.my_client.receive()
        if not(msg_in is None):
            if msg_in==my_view.my_client._END_MSG:
                print('End message received')
                sys.exit()
            else:
                my_view.msg_received(msg_in)
        turtle.ontimer(check,_WAIT_TIME) #Check recursively
    check()
    turtle.mainloop()
