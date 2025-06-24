import reflex as rx
from typing import Optional, Dict, Any
from app.state.base_state import BaseState

class AuthState(BaseState):
    """Estado para manejar la autenticación del analista."""
    
    # Información del usuario autenticado
    user: Optional[Dict[str, Any]] = None
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    
    # Estado de autenticación
    is_authenticated: bool = False
    login_error: Optional[str] = None
    
    @rx.var
    def is_authenticated_var(self) -> bool:
        """Variable reactiva para verificar si el usuario está autenticado."""
        return self.is_authenticated
    
    def login(self, email: str, password: str):
        """
        Inicia sesión del usuario.
        
        Args:
            email: Email del usuario
            password: Contraseña del usuario
        """
        self.set_loading(True)
        self.clear_error()
        
        try:
            # Aquí implementarías la lógica real de autenticación
            # Por ahora, simulamos un login exitoso
            if email and password:
                self.user = {
                    "id": 1,
                    "email": email,
                    "name": "Analista Demo",
                    "role": "analyst"
                }
                self.user_id = self.user["id"]
                self.user_email = self.user["email"]
                self.user_name = self.user["name"]
                self.is_authenticated = True
                
                self.show_success("Inicio de sesión exitoso")
                return rx.redirect("/dashboard")
            else:
                self.login_error = "Email y contraseña son requeridos"
                
        except Exception as e:
            self.login_error = f"Error en el inicio de sesión: {str(e)}"
        finally:
            self.set_loading(False)
    
    def logout(self):
        """Cierra la sesión del usuario."""
        self.user = None
        self.user_id = None
        self.user_email = None
        self.user_name = None
        self.is_authenticated = False
        self.login_error = None
        
        self.show_info("Sesión cerrada exitosamente")
        return rx.redirect("/")
    
    def check_login(self):
        """Protector de rutas para páginas que requieren autenticación."""
        if not self.is_authenticated:
            return rx.redirect("/login")
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Obtiene la información del usuario actual."""
        return self.user
    
    def update_user_info(self, **kwargs):
        """Actualiza la información del usuario."""
        if self.user:
            self.user.update(kwargs)
            # Actualizar también las variables individuales
            if "email" in kwargs:
                self.user_email = kwargs["email"]
            if "name" in kwargs:
                self.user_name = kwargs["name"]
    
    def require_auth(self, redirect_to: str = "/login"):
        """
        Decorador para requerir autenticación.
        
        Args:
            redirect_to: Ruta a la que redirigir si no está autenticado
        """
        if not self.is_authenticated:
            return rx.redirect(redirect_to) 