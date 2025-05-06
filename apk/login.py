#login.py
import flet as ft
import uuid

class AuthManager:
    def __init__(self):
        self.users = {
            "admin": {
                "password": "1234",
                "email": "admin@example.com",
                "photo": "/default_avatar.png",
                "language": "es",
                "theme": "light",
                "units": "metric",
                "notifications": "daily",
                "location": "",
                "map_prefs": {
                    "map_type": "roadmap",
                    "search_radius": 5000,
                    "visible_residues": ["all"]
                },
                "recycling_stats": {
                    "Plástico": 0,
                    "Papel": 0,
                    "Vidrio": 0,
                    "Orgánico": 0,
                    "Metal": 0,
                    "Pilas": 0,
                    "Electrónicos": 0
                },
                "fcm_token": ""  # Token para notificaciones push (vacío por defecto)
            }
        }
        self.reset_requests = {}

    def register_user(self, username, password, email):
        if username in self.users:
            return False, "El usuario ya existe"
        self.users[username] = {
            "password": password,
            "email": email,
            "photo": "/default_avatar.png",
            "language": "es",
            "theme": "light",
            "units": "metric",
            "notifications": "daily",
            "location": "",
            "map_prefs": {
                "map_type": "roadmap",
                "search_radius": 5000,
                "visible_residues": ["all"]
            },
            "recycling_stats": {
                "Plástico": 0,
                "Papel": 0,
                "Vidrio": 0,
                "Orgánico": 0,
                "Metal": 0,
                "Pilas": 0,
                "Electrónicos": 0
            },
            "fcm_token": ""
        }
        return True, "Registro exitoso"

    def login_user(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return True, "Login exitoso"
        return False, "Usuario o contraseña incorrectos"

    def request_password_reset(self, email):
        for username, data in self.users.items():
            if data["email"] == email:
                reset_code = str(uuid.uuid4())[:8]
                self.reset_requests[email] = reset_code
                return True, f"Código de recuperación enviado: {reset_code}"
        return False, "Email no encontrado"

    def reset_password(self, email, code, new_password):
        if email in self.reset_requests and self.reset_requests[email] == code:
            for username, data in self.users.items():
                if data["email"] == email:
                    data["password"] = new_password
                    del self.reset_requests[email]
                    return True, "Contraseña actualizada"
        return False, "Código o email inválidos"

class LoginScreen:
    def __init__(self, page: ft.Page, navigator=None):
        self.page = page
        self.navigator = navigator
        self.auth_manager = AuthManager()
        self.page.title = "Clasificador de Basura - Login"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.current_view = "login"
        self.password_visible = False  # Estado para controlar visibilidad de contraseña
        self.setup_ui()

    def setup_ui(self):
        self.username_field = ft.TextField(label="Usuario", width=300)
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            width=300,
            suffix_icon=ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_password_visibility
            )
        )
        self.email_field = ft.TextField(label="Email", width=300, visible=False)
        self.reset_code_field = ft.TextField(label="Código de recuperación", width=300, visible=False)
        self.message = ft.Text(value="", color=ft.Colors.RED, visible=False)

        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            on_click=self.validate_login,
            width=300,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE
        )
        self.register_button = ft.ElevatedButton(
            text="Crear Cuenta",
            on_click=self.register_user,
            width=300,
            visible=False,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )
        self.request_reset_button = ft.ElevatedButton(
            text="Enviar Código",
            on_click=self.request_reset,
            width=300,
            visible=False,
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE
        )
        self.reset_password_button = ft.ElevatedButton(
            text="Cambiar Contraseña",
            on_click=self.reset_password,
            width=300,
            visible=False,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )

        self.to_register_button = ft.TextButton(
            text="Crear cuenta",
            on_click=lambda e: self.switch_view("register")
        )
        self.to_reset_button = ft.TextButton(
            text="¿Olvidaste tu contraseña?",
            on_click=lambda e: self.switch_view("reset")
        )
        self.to_login_button = ft.TextButton(
            text="Volver al login",
            on_click=lambda e: self.switch_view("login"),
            visible=False
        )

        social_buttons = [
            ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Image(
                            src=svg_url,
                            width=24,
                            height=24,
                            fit=ft.ImageFit.CONTAIN
                        ),
                        ft.Text(provider, color=ft.Colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                on_click=lambda e, p=provider: self.social_login(p),
                width=300,
                bgcolor=color
            ) for provider, svg_url, color in [
                ("Google", "F:/respaldopc/EcoSorter/apk/imagenes/2504914.png", ft.Colors.BLUE_400),
                ("Facebook", "https://upload.wikimedia.org/wikipedia/commons/0/05/Facebook_Logo_%282019%29.png", ft.Colors.BLUE_600),
                ("Instagram", "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", ft.Colors.PINK_400),
                ("Microsoft", "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg", ft.Colors.BLUE_GREY_400)
            ]
        ]

        self.form_container = ft.Column(
            [
                ft.Text("Bienvenido A EcoSorter", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Image(
                    src="F:/respaldopc/EcoSorter/apk/imagenes/EcoSorter Image 28 abr 2025, 10_49_20.png",
                    width=200,
                    height=200,
                    fit=ft.ImageFit.CONTAIN
                ),
                self.email_field,
                self.username_field,
                self.password_field,
                self.reset_code_field,
                self.login_button,
                self.register_button,
                self.request_reset_button,
                self.reset_password_button,
                self.message,
                ft.Row(
                    [self.to_register_button, self.to_reset_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                self.to_login_button,
                ft.Divider(),
                ft.Text("O registrarse con:", color=ft.Colors.WHITE54),
                *social_buttons
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )

        self.page.clean()
        self.page.add(self.form_container)
        self.update_view()

    def toggle_password_visibility(self, e):
        self.password_visible = not self.password_visible
        self.password_field.password = not self.password_visible
        self.password_field.suffix_icon.icon = ft.Icons.VISIBILITY if self.password_visible else ft.Icons.VISIBILITY_OFF
        self.page.update()

    def switch_view(self, view):
        self.current_view = view
        self.message.visible = False
        self.password_visible = False
        self.password_field.password = True
        self.password_field.suffix_icon.icon = ft.Icons.VISIBILITY_OFF
        self.update_view()

    def update_view(self):
        is_login = self.current_view == "login"
        is_register = self.current_view == "register"
        is_reset = self.current_view == "reset"

        self.username_field.visible = is_login or is_register
        self.password_field.visible = is_login or is_register or is_reset
        self.password_field.label = "Nueva Contraseña" if is_reset else "Contraseña"
        self.email_field.visible = is_register or is_reset
        self.reset_code_field.visible = is_reset
        self.login_button.visible = is_login
        self.register_button.visible = is_register
        self.request_reset_button.visible = is_reset and not self.reset_code_field.value
        self.reset_password_button.visible = is_reset and self.reset_code_field.value
        self.to_register_button.visible = is_login
        self.to_reset_button.visible = is_login
        self.to_login_button.visible = not is_login

        self.page.update()

    def validate_login(self, e):
        success, msg = self.auth_manager.login_user(self.username_field.value, self.password_field.value)
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        self.page.update()
        if success and self.navigator:
            self.navigator.navigate("home")

    def register_user(self, e):
        success, msg = self.auth_manager.register_user(
            self.username_field.value, self.password_field.value, self.email_field.value
        )
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        if success:
            self.switch_view("login")
        self.page.update()

    def request_reset(self, e):
        success, msg = self.auth_manager.request_password_reset(self.email_field.value)
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        if success:
            self.reset_code_field.visible = True
            self.request_reset_button.visible = False
            self.reset_password_button.visible = True
        self.page.update()

    def reset_password(self, e):
        success, msg = self.auth_manager.reset_password(
            self.email_field.value, self.reset_code_field.value, self.password_field.value
        )
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        if success:
            self.switch_view("login")
        self.page.update()

    def social_login(self, provider):
        self.message.value = f"Autenticación con {provider} (simulada)"
        self.message.color = ft.Colors.BLUE
        self.message.visible = True
        self.page.update()
        if self.navigator:
            self.navigator.navigate("home")

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    app_navigator = AppNavigator(page)

if __name__ == "__main__":
    ft.app(target=main)