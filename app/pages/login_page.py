"""
Login Page - Modern design with Zurich Insurance palette
"""

import reflex as rx

def login_page():
    """Login page with Zurich Insurance design."""
    
    return rx.box(
        # Background with gradient
        rx.box(
            rx.vstack(
                # Logo and Title
                rx.vstack(
                    rx.heading(
                        "Zurich Insurance",
                        class_name="text-4xl md:text-5xl font-bold text-white text-center mb-2 tracking-tight"
                    ),
                    rx.text(
                        "Claims Management System",
                        class_name="text-xl text-blue-100 text-center font-medium"
                    ),
                    rx.divider(class_name="w-24 mx-auto border-blue-300 my-6"),
                    class_name="mb-12"
                ),
                
                # Login Form
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "Welcome Back",
                            class_name="text-3xl font-bold text-slate-800 text-center mb-2"
                        ),
                        rx.text(
                            "Sign in to access your dashboard",
                            class_name="text-slate-600 text-center mb-8"
                        ),
                        
                        # Email Field
                        rx.vstack(
                            rx.text("Email Address", class_name="text-sm font-semibold text-slate-700 mb-2"),
                            rx.input(
                                placeholder="Enter your email address",
                                type_="email",
                                class_name="w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                required=True
                            ),
                            class_name="w-full"
                        ),
                        
                        # Password Field
                        rx.vstack(
                            rx.text("Password", class_name="text-sm font-semibold text-slate-700 mb-2"),
                            rx.input(
                                placeholder="Enter your password",
                                type_="password",
                                class_name="w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                required=True
                            ),
                            class_name="w-full mt-6"
                        ),
                        
                        # Remember Me and Forgot Password
                        rx.hstack(
                            rx.checkbox(
                                "Remember me",
                                class_name="text-slate-700 font-medium"
                            ),
                            rx.link(
                                "Forgot password?",
                                class_name="text-blue-600 hover:text-blue-700 font-medium transition-colors",
                                href="#"
                            ),
                            class_name="w-full justify-between mt-6"
                        ),
                        
                        # Login Button
                        rx.button(
                            "Sign In",
                            type_="submit",
                            class_name="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl mt-8"
                        ),
                        
                        class_name="w-full max-w-md"
                    ),
                    class_name="p-8 bg-white rounded-2xl shadow-2xl border border-slate-100"
                ),
                
                # Footer
                rx.vstack(
                    rx.text(
                        "Don't have an account?",
                        class_name="text-slate-600 text-center"
                    ),
                    rx.link(
                        "Contact your administrator",
                        class_name="text-blue-600 hover:text-blue-700 font-medium transition-colors",
                        href="#"
                    ),
                    class_name="mt-8"
                ),
                
                class_name="max-w-md mx-auto px-4"
            ),
            class_name="w-full min-h-screen py-12 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 flex items-center justify-center"
        ),
        
        class_name="min-h-screen"
    ) 