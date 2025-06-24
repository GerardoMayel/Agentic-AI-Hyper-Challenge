import reflex as rx
from app.components.navbar import navbar

@rx.page(route="/")
def index_page() -> rx.Component:
    """Página principal de la aplicación."""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading(
                "Bienvenido a Agentic AI",
                size="2xl",
                color="blue.600",
                margin_bottom="4"
            ),
            rx.text(
                "Tu asistente inteligente para análisis y comunicación",
                size="lg",
                color="gray.600",
                text_align="center",
                margin_bottom="8"
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Comenzar Chat",
                        size="lg",
                        color_scheme="blue"
                    ),
                    href="/chat"
                ),
                rx.link(
                    rx.button(
                        "Ver Dashboard",
                        size="lg",
                        variant="outline"
                    ),
                    href="/dashboard"
                ),
                spacing="4"
            ),
            width="100%",
            max_width="600px",
            padding="8",
            spacing="6"
        ),
        width="100%",
        min_height="100vh",
        background="gray.50"
    ) 