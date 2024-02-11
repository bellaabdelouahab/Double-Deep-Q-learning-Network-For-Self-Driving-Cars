from pyglet import shapes,graphics,text
import pyglet
class button:
    buttono = pyglet.graphics.Batch()
    def go(self):
        self.start_button=shapes.BorderedRectangle(0, 460, 150, 40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.draw_button_track=shapes.BorderedRectangle(0, 420, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.draw_button_goal=shapes.BorderedRectangle(0, 380, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.draw_button_save=shapes.BorderedRectangle(0, 340, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.draw_button_delete=shapes.BorderedRectangle(0, 300, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.save_model=shapes.BorderedRectangle(0, 260, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.load_model=shapes.BorderedRectangle(0, 220, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.plot_learning=shapes.BorderedRectangle(0, 180, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.plot_scores=shapes.BorderedRectangle(0, 140, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.driving=shapes.BorderedRectangle(0, 100, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.loadtruck=shapes.BorderedRectangle(0, 60, 150,  40, color=(20, 200, 20),border_color=(200,20,20),batch=self.buttono)
        self.start_button.opacity=150
        self.draw_button_track.opacity=150
        self.draw_button_goal.opacity=150
        self.draw_button_save.opacity=150
        self.draw_button_delete.opacity=150
        self.save_model.opacity=150
        self.load_model.opacity=150
        self.plot_learning.opacity=150
        self.plot_scores.opacity=150
        self.driving.opacity=150
        self.loadtruck.opacity=150
        self.button_text=text.Label('start learning',font_name='Times New Roman',font_size=16,x=10, y=475,batch=self.buttono,color=(255,255,255,255))
        self.button_draw_track=text.Label('Draw Line',font_name='Times New Roman',font_size=16,x=10, y=435,batch=self.buttono,color=(255,255,255,255))
        self.button_draw_goal=text.Label('Draw Goal',font_name='Times New Roman',font_size=16,x=10, y=395,batch=self.buttono,color=(255,255,255,255))
        self.button_save_track=text.Label('save Track',font_name='Times New Roman',font_size=16,x=10, y=355,batch=self.buttono,color=(255,255,255,255))
        self.button_delete_track=text.Label('delete Track',font_name='Times New Roman',font_size=16,x=10, y=315,batch=self.buttono,color=(255,255,255,255))
        self.save_model_label=text.Label('Save Model',font_name='Times New Roman',font_size=16,x=10, y=275,batch=self.buttono,color=(255,255,255,255))
        self.load_model_label=text.Label('load Model',font_name='Times New Roman',font_size=16,x=10, y=235,batch=self.buttono,color=(255,255,255,255))
        self.plot_learn_label=text.Label('show learning',font_name='Times New Roman',font_size=16,x=10, y=195,batch=self.buttono,color=(255,255,255,255))
        self.plot_score_label=text.Label('show scores',font_name='Times New Roman',font_size=16,x=10, y=155,batch=self.buttono,color=(255,255,255,255))
        self.manual_label=text.Label('Manual : off',font_name='Times New Roman',font_size=16,x=10, y=115,batch=self.buttono,color=(255,255,255,255))
        self.loadtrucklabel=text.Label('load truck',font_name='Times New Roman',font_size=16,x=10, y=75,batch=self.buttono,color=(255,255,255,255))
        self.move_up=shapes.BorderedRectangle(782,464,30,30,color=(156,34,199),batch=self.buttono)
        self.move_down=shapes.BorderedRectangle(782,428,30,30,color=(156,134,199),batch=self.buttono)
        self.move_left=shapes.BorderedRectangle(746,428,30,30,color=(156,34,199),batch=self.buttono)
        self.move_right=shapes.BorderedRectangle(818,428,30,30,color=(156,34,199),batch=self.buttono)
        
        
        self.buttono.invalidate()