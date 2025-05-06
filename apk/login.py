#login.py
import flet as ft
import uuid
import re
import random
import string

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
                "fcm_token": ""
            }
        }
        self.reset_requests = {}
        self.verification_codes = {}  # Store 2FA and email verification codes

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

    def generate_verification_code(self, username):
        code = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit code
        self.verification_codes[username] = code
        return code

    def verify_code(self, username, code):
        if username in self.verification_codes and self.verification_codes[username] == code:
            del self.verification_codes[username]  # Clear code after verification
            return True
        return False

class LoginScreen:
    def __init__(self, page: ft.Page, navigator=None):
        self.page = page
        self.navigator = navigator
        self.auth_manager = AuthManager()
        self.page.title = "Clasificador de Basura - Login"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.current_view = "login"
        self.password_visible = False
        self.setup_ui()

    def check_password_strength(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not re.search(r"[A-Z]", password):
            return False, "La contraseña debe tener al menos una letra mayúscula"
        if not re.search(r"[a-z]", password):
            return False, "La contraseña debe tener al menos una letra minúscula"
        if not re.search(r"[0-9]", password):
            return False, "La contraseña debe tener al menos un número"
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "La contraseña debe tener al menos un carácter especial"
        return True, "Contraseña válida"

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

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
        self.confirm_password_field = ft.TextField(
            label="Confirmar Contraseña",
            password=True,
            width=300,
            visible=False,
            suffix_icon=ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                on_click=self.toggle_confirm_password_visibility
            )
        )
        self.email_field = ft.TextField(label="Email", width=300, visible=False)
        self.reset_code_field = ft.TextField(label="Código de recuperación", width=300, visible=False)
        self.verification_code_field = ft.TextField(label="Código de verificación", width=300, visible=False)

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
        self.verify_email_button = ft.ElevatedButton(
            text="Verificar Email",
            on_click=self.verify_email,
            width=300,
            visible=False,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )
        self.verify_2fa_button = ft.ElevatedButton(
            text="Verificar 2FA",
            on_click=self.verify_2fa,
            width=300,
            visible=False,
            bgcolor=ft.Colors.BLUE_600,
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
                self.confirm_password_field,
                self.reset_code_field,
                self.verification_code_field,
                self.message,
                self.login_button,
                self.register_button,
                self.request_reset_button,
                self.reset_password_button,
                self.verify_email_button,
                self.verify_2fa_button,
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

    def toggle_confirm_password_visibility(self, e):
        self.confirm_password_visible = not getattr(self, 'confirm_password_visible', False)
        self.confirm_password_field.password = not self.confirm_password_visible
        self.confirm_password_field.suffix_icon.icon = ft.Icons.VISIBILITY if self.confirm_password_visible else ft.Icons.VISIBILITY_OFF
        self.page.update()

    def switch_view(self, view):
        self.current_view = view
        self.message.visible = False
        self.password_visible = False
        self.password_field.password = True
        self.password_field.suffix_icon.icon = ft.Icons.VISIBILITY_OFF
        self.confirm_password_visible = False
        self.confirm_password_field.password = True
        self.confirm_password_field.suffix_icon.icon = ft.Icons.VISIBILITY_OFF
        self.update_view()

    def update_view(self):
        is_login = self.current_view == "login"
        is_register = self.current_view == "register"
        is_reset = self.current_view == "reset"
        is_verify_email = self.current_view == "verify_email"
        is_verify_2fa = self.current_view == "verify_2fa"

        self.username_field.visible = is_login or is_register
        self.password_field.visible = is_login or is_register or is_reset
        self.password_field.label = "Nueva Contraseña" if is_reset else "Contraseña"
        self.confirm_password_field.visible = is_register
        self.email_field.visible = is_register or is_reset
        self.reset_code_field.visible = is_reset
        self.verification_code_field.visible = is_verify_email or is_verify_2fa
        self.verification_code_field.label = "Código de 2FA" if is_verify_2fa else "Código de verificación"
        self.login_button.visible = is_login
        self.register_button.visible = is_register
        self.request_reset_button.visible = is_reset and not self.reset_code_field.value
        self.reset_password_button.visible = is_reset and self.reset_code_field.value
        self.verify_email_button.visible = is_verify_email
        self.verify_2fa_button.visible = is_verify_2fa
        self.to_register_button.visible = is_login
        self.to_reset_button.visible = is_login
        self.to_login_button.visible = not is_login

        self.page.update()

    def validate_login(self, e):
        # Password strength check
        is_strong, message = self.check_password_strength(self.password_field.value)
        if not is_strong:
            self.message.value = message
            self.message.color = ft.Colors.RED
            self.message.visible = True
            self.page.update()
            return

        # Login attempt
        success, msg = self.auth_manager.login_user(self.username_field.value, self.password_field.value)
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        self.page.update()
        if success and self.navigator:
            # Start 2FA process
            code = self.auth_manager.generate_verification_code(self.username_field.value)
            self.message.value = f"Código 2FA enviado: {code} (simulado)"
            self.message.color = ft.Colors.BLUE
            self.switch_view("verify_2fa")

    def verify_2fa(self, e):
        username = self.username_field.value
        code = self.verification_code_field.value
        if self.auth_manager.verify_code(username, code):
            self.message.value = "2FA verificado con éxito"
            self.message.color = ft.Colors.GREEN
            self.message.visible = True
            self.navigator.navigate("home")
        else:
            self.message.value = "Código 2FA incorrecto"
            self.message.color = ft.Colors.RED
            self.message.visible = True
        self.page.update()

    def register_user(self, e):
        # Email validation
        if not self.validate_email(self.email_field.value):
            self.message.value = "Formato de email inválido"
            self.message.color = ft.Colors.RED
            self.message.visible = True
            self.page.update()
            return

        # Password strength check
        is_strong, message = self.check_password_strength(self.password_field.value)
        if not is_strong:
            self.message.value = message
            self.message.color = ft.Colors.RED
            self.message.visible = True
            self.page.update()
            return

        # Password confirmation
        if self.password_field.value != self.confirm_password_field.value:
            self.message.value = "Las contraseñas no coinciden"
            self.message.color = ft.Colors.RED
            self.message.visible = True
            self.page.update()
            return

        # Register user
        success, msg = self.auth_manager.register_user(
            self.username_field.value, self.password_field.value, self.email_field.value
        )
        self.message.value = msg
        self.message.color = ft.Colors.GREEN if success else ft.Colors.RED
        self.message.visible = True
        if success:
            # Simulate email verification
            code = self.auth_manager.generate_verification_code(self.username_field.value)
            self.message.value = f"Código de verificación enviado: {code} (simulado)"
            self.message.color = ft.Colors.BLUE
            self.switch_view("verify_email")
        self.page.update()

    def verify_email(self, e):
        username = self.username_field.value
        code = self.verification_code_field.value
        if self.auth_manager.verify_code(username, code):
            self.message.value = "Email verificado con éxito"
            self.message.color = ft.Colors.GREEN
            self.message.visible = True
            self.switch_view("login")
        else:
            self.message.value = "Código de verificación incorrecto"
            self.message.color = ft.Colors.RED
            self.message.visible = True
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
        # Password strength check for reset
        is_strong, message = self.check_password_strength(self.password_field.value)
        if not is_strong:
            self.message.value = message
            self.message.color = ft.Colors.RED
            self.message.visible = True
            self.page.update()
            return

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