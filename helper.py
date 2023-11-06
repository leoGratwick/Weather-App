helper = """
Screen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    id: body
                    orientation: "vertical"
                    
                    MDTopAppBar:
                        id: headerBar
                        title: 'Bristol'
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                        elevation: 3
                        
                    
                        
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'
                
                    
                
                MDLabel:
                    text: 'Choose a Location'
                    font_style: 'H5'
                    size_hint_y: None
                    height: self.texture_size[1]
                    
                MDLabel:
                    text: 'Check out the weather in different locations!'
                    font_style: 'Caption'
                    size_hint_y: None
                    height: self.texture_size[1]
                    
                ScrollView:
                    MDList:
                        id: locationNav
                    
    
                
                
                MDRectangleFlatButton:
                    text: 'Quit'
                    font_style: 'H6'
                    on_release: app.stop()
                    size_hint: (1,0.1)
                    markup: True
                    
                    
                    
                    
                
                
"""

