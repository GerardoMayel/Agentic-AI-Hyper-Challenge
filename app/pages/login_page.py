import reflex as rx
from app.components.navbar import navbar
from app.state.auth_state import AuthState

@rx.page(route="/login")
def login_page() -> rx.Component:
    """Página de inicio de sesión."""
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.heading(
                "Iniciar Sesión",
                size="xl",
                color="blue.600",
                margin_bottom="6"
            ),
            rx.vstack(
                rx.input(
                    placeholder="Email",
                    id="email",
                    type_="email",
                    required=True,
                    width="100%"
                ),
                rx.input(
                    placeholder="Contraseña",
                    id="password",
                    type_="password",
                    required=True,
                    width="100%"
                ),
                rx.button(
                    "Iniciar Sesión",
                    width="100%",
                    color_scheme="blue",
                    on_click=AuthState.login
                ),
                rx.link(
                    "¿No tienes cuenta? Regístrate",
                    href="/register",
                    color="blue.600",
                    text_decoration="underline"
                ),
                width="100%",
                max_width="400px",
                spacing="4",
                padding="6",
                border="1px solid",
                border_color="gray.200",
                border_radius="lg",
                background="white"
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