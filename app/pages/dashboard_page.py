"""
Dashboard Page - Modern design with Zurich Insurance palette
"""

import reflex as rx

def dashboard_page():
    """Dashboard page with Zurich Insurance design."""
    
    return rx.box(
        # Header
        rx.box(
            rx.vstack(
                rx.heading(
                    "Claims Dashboard",
                    class_name="text-4xl md:text-5xl font-bold text-white text-center mb-4 tracking-tight"
                ),
                rx.text(
                    "Monitor and manage insurance claims",
                    class_name="text-xl text-blue-100 text-center font-medium"
                ),
                rx.divider(class_name="w-24 mx-auto border-blue-300 my-4"),
                class_name="max-w-4xl mx-auto px-4"
            ),
            class_name="w-full py-16 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden"
        ),
        
        # Stats Cards
        rx.box(
            rx.vstack(
                rx.heading(
                    "System Overview",
                    class_name="text-3xl font-bold text-slate-800 text-center mb-12"
                ),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "📊",
                                class_name="text-5xl mb-4"
                            ),
                            rx.heading(
                                "Total Claims",
                                class_name="text-2xl font-bold text-slate-800 mb-2"
                            ),
                            rx.heading(
                                "1,247",
                                class_name="text-4xl font-bold text-blue-600 mb-2"
                            ),
                            rx.text(
                                "+12% this month",
                                class_name="text-green-600 font-semibold"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "⏳",
                                class_name="text-5xl mb-4"
                            ),
                            rx.heading(
                                "Pending",
                                class_name="text-2xl font-bold text-slate-800 mb-2"
                            ),
                            rx.heading(
                                "89",
                                class_name="text-4xl font-bold text-orange-600 mb-2"
                            ),
                            rx.text(
                                "Under review",
                                class_name="text-slate-600 font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "✅",
                                class_name="text-5xl mb-4"
                            ),
                            rx.heading(
                                "Approved",
                                class_name="text-2xl font-bold text-slate-800 mb-2"
                            ),
                            rx.heading(
                                "1,158",
                                class_name="text-4xl font-bold text-green-600 mb-2"
                            ),
                            rx.text(
                                "92.9% approval rate",
                                class_name="text-slate-600 font-medium"
                            ),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"
                    ),
                    class_name="gap-8 flex-wrap"
                ),
                class_name="max-w-7xl mx-auto"
            ),
            class_name="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50"
        ),
        
        # Recent Claims Cards
        rx.box(
            rx.vstack(
                rx.heading(
                    "Recent Claims",
                    class_name="text-3xl font-bold text-slate-800 text-center mb-12"
                ),
                rx.vstack(
                    # Claim 1
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("CLM-2024-001", class_name="font-bold text-slate-800 text-lg"),
                                rx.text("John Smith", class_name="text-slate-600"),
                                class_name="flex-1"
                            ),
                            rx.vstack(
                                rx.text("Trip Cancellation", class_name="font-medium text-slate-700"),
                                rx.text("$2,500", class_name="font-bold text-green-600 text-lg"),
                                class_name="flex-1 text-center"
                            ),
                            rx.vstack(
                                rx.badge(
                                    "Approved",
                                    class_name="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
                                ),
                                rx.text("2024-01-15", class_name="text-slate-500 text-sm"),
                                class_name="flex-1 text-center"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"
                    ),
                    
                    # Claim 2
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("CLM-2024-002", class_name="font-bold text-slate-800 text-lg"),
                                rx.text("Maria Garcia", class_name="text-slate-600"),
                                class_name="flex-1"
                            ),
                            rx.vstack(
                                rx.text("Baggage Delay", class_name="font-medium text-slate-700"),
                                rx.text("$800", class_name="font-bold text-orange-600 text-lg"),
                                class_name="flex-1 text-center"
                            ),
                            rx.vstack(
                                rx.badge(
                                    "Pending",
                                    class_name="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium"
                                ),
                                rx.text("2024-01-14", class_name="text-slate-500 text-sm"),
                                class_name="flex-1 text-center"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"
                    ),
                    
                    # Claim 3
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("CLM-2024-003", class_name="font-bold text-slate-800 text-lg"),
                                rx.text("David Johnson", class_name="text-slate-600"),
                                class_name="flex-1"
                            ),
                            rx.vstack(
                                rx.text("Trip Interruption", class_name="font-medium text-slate-700"),
                                rx.text("$1,200", class_name="font-bold text-green-600 text-lg"),
                                class_name="flex-1 text-center"
                            ),
                            rx.vstack(
                                rx.badge(
                                    "Approved",
                                    class_name="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"
                                ),
                                rx.text("2024-01-13", class_name="text-slate-500 text-sm"),
                                class_name="flex-1 text-center"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"
                    ),
                    
                    # Claim 4
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("CLM-2024-004", class_name="font-bold text-slate-800 text-lg"),
                                rx.text("Sarah Wilson", class_name="text-slate-600"),
                                class_name="flex-1"
                            ),
                            rx.vstack(
                                rx.text("Trip Delay", class_name="font-medium text-slate-700"),
                                rx.text("$300", class_name="font-bold text-blue-600 text-lg"),
                                class_name="flex-1 text-center"
                            ),
                            rx.vstack(
                                rx.badge(
                                    "In Review",
                                    class_name="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
                                ),
                                rx.text("2024-01-12", class_name="text-slate-500 text-sm"),
                                class_name="flex-1 text-center"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"
                    ),
                    
                    # Claim 5
                    rx.box(
                        rx.hstack(
                            rx.vstack(
                                rx.text("CLM-2024-005", class_name="font-bold text-slate-800 text-lg"),
                                rx.text("Michael Brown", class_name="text-slate-600"),
                                class_name="flex-1"
                            ),
                            rx.vstack(
                                rx.text("Trip Cancellation", class_name="font-medium text-slate-700"),
                                rx.text("$1,800", class_name="font-bold text-red-600 text-lg"),
                                class_name="flex-1 text-center"
                            ),
                            rx.vstack(
                                rx.badge(
                                    "Rejected",
                                    class_name="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium"
                                ),
                                rx.text("2024-01-11", class_name="text-slate-500 text-sm"),
                                class_name="flex-1 text-center"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"
                    ),
                    
                    class_name="space-y-6 max-w-4xl mx-auto w-full"
                ),
                class_name="max-w-7xl mx-auto"
            ),
            class_name="w-full py-16 bg-white"
        ),
        
        # Quick Actions
        rx.box(
            rx.vstack(
                rx.heading(
                    "Quick Actions",
                    class_name="text-3xl font-bold text-slate-800 text-center mb-12"
                ),
                rx.hstack(
                    rx.button(
                        rx.vstack(
                            rx.text("📋", class_name="text-4xl mb-3"),
                            rx.text("New Claim", class_name="font-bold text-slate-800"),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"
                    ),
                    rx.button(
                        rx.vstack(
                            rx.text("📊", class_name="text-4xl mb-3"),
                            rx.text("View Reports", class_name="font-bold text-slate-800"),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"
                    ),
                    rx.button(
                        rx.vstack(
                            rx.text("⚙️", class_name="text-4xl mb-3"),
                            rx.text("Settings", class_name="font-bold text-slate-800"),
                            class_name="text-center"
                        ),
                        class_name="p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"
                    ),
                    class_name="gap-8 flex-wrap"
                ),
                class_name="max-w-5xl mx-auto"
            ),
            class_name="w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50"
        ),
        
        class_name="min-h-screen"
    ) 