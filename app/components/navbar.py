"""
Navigation bar component with modern Tailwind CSS design
"""

import reflex as rx

def navbar():
    """Navigation bar component with modern design."""
    return rx.hstack(
        rx.heading(
            "Claims Management System", 
            class_name="text-xl font-bold text-white"
        ),
        rx.spacer(),
        rx.hstack(
            rx.link(
                "Home", 
                href="/", 
                class_name="text-white hover:text-blue-200 font-medium transition-colors duration-200"
            ),
            rx.link(
                "Submit Claim", 
                href="/claim-form", 
                class_name="text-white hover:text-blue-200 font-medium transition-colors duration-200"
            ),
            rx.link(
                "Dashboard", 
                href="/dashboard", 
                class_name="text-white hover:text-blue-200 font-medium transition-colors duration-200"
            ),
            rx.link(
                "Login", 
                href="/login", 
                class_name="text-white hover:text-blue-200 font-medium transition-colors duration-200"
            ),
            class_name="hidden md:flex space-x-6"
        ),
        rx.button(
            rx.text("☰", class_name="text-xl"),
            class_name="md:hidden text-white hover:bg-blue-700 p-2 rounded-lg transition-colors duration-200"
        ),
        class_name="w-full px-6 py-4 bg-gradient-to-r from-blue-900 to-blue-700 shadow-lg sticky top-0 z-50"
    ) 