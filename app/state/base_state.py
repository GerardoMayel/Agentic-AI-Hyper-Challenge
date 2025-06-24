import reflex as rx
from typing import Optional, Dict, Any

class BaseState(rx.State):
    """Estado base de la aplicación con funcionalidades comunes."""
    
    # Configuración general
    app_name: str = "Agentic AI"
    environment: str = "development"
    
    # Estado de carga y errores
    loading: bool = False
    error_message: Optional[str] = None
    
    # Configuración de la aplicación
    config: Dict[str, Any] = {}
    
    def set_loading(self, loading: bool):
        """Establece el estado de carga."""
        self.loading = loading
    
    def set_error(self, message: str):
        """Establece un mensaje de error."""
        self.error_message = message
    
    def clear_error(self):
        """Limpia el mensaje de error."""
        self.error_message = None
    
    def show_success(self, message: str):
        """Muestra un mensaje de éxito (placeholder para notificaciones)."""
        print(f"Éxito: {message}")
        # Aquí podrías implementar un sistema de notificaciones
    
    def show_info(self, message: str):
        """Muestra un mensaje informativo."""
        print(f"Info: {message}")
    
    def update_config(self, key: str, value: Any):
        """Actualiza la configuración de la aplicación."""
        self.config[key] = value
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración."""
        return self.config.get(key, default) 