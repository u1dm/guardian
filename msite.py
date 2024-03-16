import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet_core.control_event import ControlEvent
from session import Session
s = Session()

def main(page: ft.Page) -> None:
        page.title = 'Sigunp'         
        page.vertical_alignment=ft.MainAxisAlignment.CENTER                               
        page.theme_mode = ft.ThemeMode.DARK

        text_username : TextField = TextField(label='Username', text_align=ft.TextAlign.LEFT, width=200)
        text_password : TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT, width=200, password=True)
        button_register: ElevatedButton = ElevatedButton(text='Register', width=200)
        button_sudmit: ElevatedButton = ElevatedButton(text='Sing up', width=200, disabled=True)
        
        def validate(e: ControlEvent) -> None:
                if all([text_username.value, text_password.value]):
                        button_sudmit.disabled = False
                else:
                    button_sudmit.disable = True

                page.update()

        add_button: ElevatedButton = ElevatedButton(text='Add')
        delete_button: ElevatedButton = ElevatedButton(text='Delete')

        def sumbit(e: ControlEvent) -> None:
               print('Username:', text_username.value)
               print('Password:', text_password.value)
               login_state = s.login(username=text_username.value, master_password=text_password.value)
               
               if login_state == "SUCCESS_LOGIN":
                    page.clean()
                    for i in s.list_all_passwords():
                           page.vertical_alignment=ft.MainAxisAlignment.START
                           page.add(ft.Text(i))
                    page.add(add_button)
                    page.add(delete_button)

        label_field : TextField = TextField(label='Label', text_align=ft.TextAlign.LEFT)
        login_field : TextField = TextField(label='Login', text_align=ft.TextAlign.LEFT)
        password_field : TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT)
        confirm_add_button : ElevatedButton = ElevatedButton(text='Confirm')

        register_user : TextField = TextField(label='Login', text_align=ft.TextAlign.LEFT)
        register_master_password : TextField = TextField(label='Password', text_align=ft.TextAlign.LEFT)
        button_register_confirm :  ElevatedButton = ElevatedButton(text='Register')

        label_field_delete : TextField = TextField(label='Label', text_align=ft.TextAlign.LEFT)
        confirm_add_button_delete : ElevatedButton = ElevatedButton(text='Confirm')

        def add_password(e: ControlEvent) -> None:
            page.clean()
            page.add(   
                  label_field,
                  login_field,
                  password_field,
                  confirm_add_button
            )


        def add2_password(e: ControlEvent) -> None:
              print('Label:', label_field.value)
              print('Login:', login_field.value)
              print('Password:', password_field.value)
              s.add_password(label=label_field.value, login=login_field.value, password=password_field.value)
              page.clean()
              for i in s.list_all_passwords():
                           page.vertical_alignment=ft.MainAxisAlignment.START
                           page.add(ft.Text(i))
              page.add(add_button)
              page.add(delete_button)
               
        def delete_password(e: ControlEvent) -> None:
            page.clean()
            page.add(   
                   label_field_delete,
                   confirm_add_button_delete
            )
            
        def delete2_password(e: ControlEvent) -> None:
               print('Label for delete:', label_field_delete.value)
               s.delete_password(label=label_field_delete.value)
               page.clean()
               for i in s.list_all_passwords():
                           page.vertical_alignment=ft.MainAxisAlignment.START
                           page.add(ft.Text(i))
               page.add(add_button)
               page.add(delete_button)

        def register(e: ControlEvent) -> None:
              page.clean()
              page.add(   
                     Row( 
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[    
                                   Column(   
                                   [      
                                          
                                          register_user,
                                          register_master_password,
                                          button_register_confirm
                                   ]
                            )
                                   
                            ],
                     )
              )

       #  def database(e: ControlEvent) -> None:
       #        page.clean()
       #        page.add(     
       #                      ft.DataTable(       
       #                             columns=[   
       #                                    ft.DataColumn(ft.Text("Label")),
       #                                    ft.DataColumn(ft.Text("Login")),
       #                                    ft.DataColumn(ft.Text("Password")),
       #                             ],

                            
       #                             rows=[
                                          
       #                                    ft.DataRow( 
       #                                           cells=[      
                                                 
       #                                                  ft.DataCell(ft.Text(i[1])),
       #                                                  ft.DataCell(ft.Text(i[2])),
       #                                                  ft.DataCell(ft.Text(i[3])),                                         
                                                               
       #                                           ],
       #                                    ),
       #                             ],
       #                      ),
       #               )



        def register_2(e: ControlEvent) -> None:
              print('User:', register_user.value)
              print('Password:', register_master_password.value)
              s.register(username=register_user.value, master_password=register_master_password.value)
              page.clean()
              page.add(   
                     Row( 
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[    
                                   Column(   
                                   [text_username,
                                   text_password,
                                   button_sudmit, button_register
                                   ]
                            )
                                   
                            ],
                     )
              )

        button_register_confirm.on_click = register_2
        confirm_add_button_delete.on_click = delete2_password
        delete_button.on_click = delete_password

        add_button.on_click = add_password
        confirm_add_button.on_click = add2_password

        button_register.on_click = register
        text_username.on_change = validate
        text_password.on_change = validate
        button_sudmit.on_click = sumbit

        page.add(   
               Row( 
                      alignment=ft.MainAxisAlignment.CENTER,
                      controls=[    
                            Column(   
                             [
                              ft.Text('Guardian', text_align='CENTER', size='20'),
                              text_username,
                              text_password,
                              button_sudmit, button_register
                              ]
                      )
                             
                      ],
               )
        )

if __name__ == '__main__':
       ft.app(port=8551, target=main, view=ft.AppView.WEB_BROWSER)