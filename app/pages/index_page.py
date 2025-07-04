"""
Index Page - Modern design with Zurich Insurance palette
"""

import reflex as rx

def index_page():
    """Main landing page with Zurich Insurance design."""
    
    return rx.box(
        # Hero Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Zurich Insurance",
                    class_name="text-5xl md:text-7xl font-bold text-white text-center mb-6 tracking-tight"
                ),
                rx.heading(
                    "Claims Management System",
                    class_name="text-3xl md:text-4xl font-semibold text-blue-100 text-center mb-8"
                ),
                rx.text(
                    "Professional insurance claims processing with advanced automation",
                    class_name="text-xl text-blue-200 text-center max-w-3xl mb-12 leading-relaxed"
                ),
                rx.divider(class_name="w-32 mx-auto border-blue-300 my-8"),
                rx.hstack(
                    rx.button(
                        "Submit Claim",
                        class_name="bg-white text-slate-800 px-12 py-4 rounded-2xl font-bold text-lg hover:bg-blue-50 transition-all duration-300 transform hover:scale-105 shadow-2xl"
                    ),
                    rx.button(
                        "View Dashboard",
                        class_name="border-2 border-white text-white px-12 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"
                    ),
                    class_name="gap-6 flex-wrap justify-center"
                ),
                class_name="max-w-6xl mx-auto px-4"
            ),
            class_name="w-full py-24 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden"
        ),
        
        # Features Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Why Choose Our System?",
                    class_name="text-4xl font-bold text-slate-800 text-center mb-16"
                ),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "🚀",
                                class_name="text-6xl mb-6"
                            ),
                            rx.heading(
                                "Fast Processing",
                                class_name="text-2xl font-bold text-slate-800 mb-4"
                            ),
                            rx.text(
                                "Automated claims processing with AI-powered document analysis for faster turnaround times.",
                                class_name="text-slate-600 text-center leading-relaxed"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "🔒",
                                class_name="text-6xl mb-6"
                            ),
                            rx.heading(
                                "Secure & Reliable",
                                class_name="text-2xl font-bold text-slate-800 mb-4"
                            ),
                            rx.text(
                                "Enterprise-grade security with encrypted data storage and secure document handling.",
                                class_name="text-slate-600 text-center leading-relaxed"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "📱",
                                class_name="text-6xl mb-6"
                            ),
                            rx.heading(
                                "Mobile Friendly",
                                class_name="text-2xl font-bold text-slate-800 mb-4"
                            ),
                            rx.text(
                                "Responsive design that works perfectly on all devices - desktop, tablet, and mobile.",
                                class_name="text-slate-600 text-center leading-relaxed"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    class_name="gap-8 flex-wrap"
                ),
                class_name="max-w-7xl mx-auto"
            ),
            class_name="w-full py-20 bg-gradient-to-br from-slate-50 to-blue-50"
        ),
        
        # Stats Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Our Track Record",
                    class_name="text-4xl font-bold text-white text-center mb-16"
                ),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "10,000+",
                                class_name="text-5xl font-bold text-blue-200 mb-2"
                            ),
                            rx.text(
                                "Claims Processed",
                                class_name="text-blue-100 text-lg font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "99.9%",
                                class_name="text-5xl font-bold text-blue-200 mb-2"
                            ),
                            rx.text(
                                "Uptime",
                                class_name="text-blue-100 text-lg font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "< 24h",
                                class_name="text-5xl font-bold text-blue-200 mb-2"
                            ),
                            rx.text(
                                "Average Response",
                                class_name="text-blue-100 text-lg font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "4.9/5",
                                class_name="text-5xl font-bold text-blue-200 mb-2"
                            ),
                            rx.text(
                                "Customer Rating",
                                class_name="text-blue-100 text-lg font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="flex-1"
                    ),
                    class_name="gap-8 flex-wrap"
                ),
                class_name="max-w-6xl mx-auto px-4"
            ),
            class_name="w-full py-20 bg-gradient-to-br from-slate-800 via-blue-800 to-blue-700"
        ),
        
        # CTA Section
        rx.box(
            rx.vstack(
                rx.heading(
                    "Ready to Get Started?",
                    class_name="text-4xl font-bold text-slate-800 text-center mb-8"
                ),
                rx.text(
                    "Join thousands of satisfied customers who trust our claims management system",
                    class_name="text-xl text-slate-600 text-center max-w-3xl mb-12"
                ),
                rx.button(
                    "Submit Your First Claim",
                    class_name="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-12 py-6 rounded-2xl font-bold text-xl hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-2xl"
                ),
                class_name="max-w-4xl mx-auto px-4"
            ),
            class_name="w-full py-20 bg-white"
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