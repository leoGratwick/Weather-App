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
                        title: app.location
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open"), "Menu", "Menu"]]
                        right_action_items: [["swap-horizontal-bold", lambda x: app.refresh(), "Swap to Opposite View"],["refresh", lambda x: app.refresh(), "Refresh"]]
                        elevation: 3
                        font_style: 'H3'
                        
                        
                        
                        
                        
                    
                        
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
                    text: 'Set A Default location'
                    font_style: 'H6'
                    on_release: app.set_default_location()
                    size_hint: (1,0.1)
                    
                
                MDRaisedButton:
                    text: 'Quit'
                    font_style: 'H6'
                    on_release: app.stop()
                    size_hint: (1,0.1)
                    markup: True
                    
       
                    
<PopupBox>:
    size_hint: .2, .2
    auto_dismiss: True  
    title: 'Weather Update'


<ItemConfirm>
    on_release: root.set_icon(check)
    id:itemConf

    CheckboxLeftWidget:
        id: check
        group: "check"
        on_active: app.on_checkbox_active(*args,itemConf.text)
                     
                    

                
                
"""

