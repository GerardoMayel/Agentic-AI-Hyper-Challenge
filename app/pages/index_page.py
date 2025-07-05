"""
Index Page - Simple and functional home page
"""

import reflex as rx

def index_page():
    """Simple home page with navigation to main sections."""
    
    return rx.box(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "🏢 Zurich Insurance",
                    class_name="text-5xl md:text-6xl font-bold text-white text-center mb-6 tracking-tight"
                ),
                rx.heading(
                    "Claims Management System",
                    class_name="text-3xl md:text-4xl font-semibold text-blue-100 text-center mb-8"
                ),
                rx.text(
                    "Professional insurance claims management system with advanced automation",
                    class_name="text-xl text-blue-200 text-center max-w-3xl mb-12 leading-relaxed"
                ),
                rx.divider(class_name="w-32 mx-auto border-blue-300 my-8"),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "📝 Submit Claim",
                            class_name="bg-white text-slate-800 px-8 py-4 rounded-2xl font-bold text-lg hover:bg-blue-50 transition-all duration-300 transform hover:scale-105 shadow-2xl"
                        ),
                        href="/claim-form"
                    ),
                    rx.link(
                        rx.button(
                            "📊 View Dashboard",
                            class_name="border-2 border-white text-white px-8 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"
                        ),
                        href="/dashboard"
                    ),
                    rx.link(
                        rx.button(
                            "🔐 Analyst Login",
                            class_name="border-2 border-white text-white px-8 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"
                        ),
                        href="/login"
                    ),
                    class_name="gap-4 flex-wrap justify-center"
                ),
                class_name="max-w-6xl mx-auto px-4"
            ),
            class_name="w-full py-20 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden"
        ),
        
        # Features Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Key Features",
                    class_name="text-4xl font-bold text-slate-800 text-center mb-12"
                ),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text("🚀", class_name="text-5xl mb-4"),
                            rx.heading("Fast Processing", class_name="text-xl font-bold text-slate-800 mb-3"),
                            rx.text("Automated AI-powered analysis for faster response times.", class_name="text-slate-600 text-center text-sm"),
                            class_name="text-center"
                        ),
                        class_name="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("🔒", class_name="text-5xl mb-4"),
                            rx.heading("Secure & Reliable", class_name="text-xl font-bold text-slate-800 mb-3"),
                            rx.text("Enterprise-grade security with encrypted data storage.", class_name="text-slate-600 text-center text-sm"),
                            class_name="text-center"
                        ),
                        class_name="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("📱", class_name="text-5xl mb-4"),
                            rx.heading("Multi-Platform", class_name="text-xl font-bold text-slate-800 mb-3"),
                            rx.text("Responsive design that works on all devices.", class_name="text-slate-600 text-center text-sm"),
                            class_name="text-center"
                        ),
                        class_name="p-6 bg-white rounded-xl shadow-lg border border-slate-100 flex-1"
                    ),
                    class_name="gap-6 flex-wrap"
                ),
                class_name="max-w-6xl mx-auto px-4"
            ),
            class_name="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50"
        ),
        
        # CTA Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Ready to Get Started?",
                    class_name="text-3xl font-bold text-slate-800 text-center mb-6"
                ),
                rx.text(
                    "Access our professional claims management system",
                    class_name="text-lg text-slate-600 text-center max-w-2xl mb-8"
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "📝 Submit Claim",
                            class_name="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl"
                        ),
                        href="/claim-form"
                    ),
                    rx.link(
                        rx.button(
                            "📊 View Dashboard",
                            class_name="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-600 hover:text-white transition-all duration-300 transform hover:scale-105"
                        ),
                        href="/dashboard"
                    ),
                    class_name="gap-4 flex-wrap justify-center"
                ),
                class_name="max-w-4xl mx-auto px-4"
            ),
            class_name="w-full py-16 bg-white"
        ),
        
        # Footer
        rx.box(
            rx.vstack(
                rx.text(
                    "© 2024 Zurich Insurance. All rights reserved.",
                    class_name="text-slate-500 text-center"
                ),
                rx.text(
                    "Professional insurance solutions for a secure future",
                    class_name="text-slate-400 text-center text-sm"
                ),
                class_name="max-w-4xl mx-auto px-4"
            ),
            class_name="w-full py-12 bg-slate-50 border-t border-slate-200"
        ),
        
        class_name="min-h-screen"
    ) 