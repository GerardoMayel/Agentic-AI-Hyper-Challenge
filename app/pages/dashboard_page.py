import reflex as rx
from app.components.navbar import navbar
from app.state.auth_state import AuthState

@rx.page(route="/dashboard", on_load=AuthState.check_login)
def dashboard_page() -> rx.Component:
    """Página de dashboard para el analista, protegida por login."""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading(
                "Dashboard del Analista",
                size="xl",
                color="blue.600",
                margin_bottom="6"
            ),
            rx.text(
                "Bienvenido al panel de control. Aquí puedes gestionar conversaciones y configuraciones.",
                color="gray.600",
                margin_bottom="8"
            ),
            rx.hstack(
                rx.vstack(
                    rx.heading("Conversaciones Activas", size="md"),
                    rx.text("0 conversaciones en curso"),
                    rx.button("Ver Todas", variant="outline"),
                    padding="4",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    background="white",
                    width="200px"
                ),
                rx.vstack(
                    rx.heading("Emails Recibidos", size="md"),
                    rx.text("0 emails hoy"),
                    rx.button("Ver Emails", variant="outline"),
                    padding="4",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    background="white",
                    width="200px"
                ),
                rx.vstack(
                    rx.heading("Configuración", size="md"),
                    rx.text("Ajustes del sistema"),
                    rx.button("Configurar", variant="outline"),
                    padding="4",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    background="white",
                    width="200px"
                ),
                spacing="6",
                width="100%",
                justify="center"
            ),
            width="100%",
            max_width="800px",
            padding="8",
            spacing="6"
        ),
        width="100%",
        min_height="100vh",
        background="gray.50"
    ) 