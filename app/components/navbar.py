import reflex as rx
from app.state.auth_state import AuthState

def navbar() -> rx.Component:
    """
    Componente de navegación principal de la aplicación.
    Muestra diferentes opciones según el estado de autenticación.
    """
    return rx.hstack(
        rx.heading("Agentic AI", size="lg", color="blue.600"),
        rx.spacer(),
        rx.cond(
            AuthState.is_authenticated,
            rx.hstack(
                rx.link("Dashboard", href="/dashboard", color="gray.600"),
                rx.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    color_scheme="red",
                    size="sm"
                ),
                spacing="4"
            ),
            rx.hstack(
                rx.link("Iniciar Sesión", href="/login", color="gray.600"),
                rx.link("Registrarse", href="/register", color="blue.600"),
                spacing="4"
            )
        ),
        width="100%",
        padding="4",
        border_bottom="1px solid",
        border_color="gray.200",
        background="white"
    ) 