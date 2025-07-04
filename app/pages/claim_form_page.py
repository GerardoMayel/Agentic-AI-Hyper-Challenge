"""
Claim Form Page - Professional design with Zurich Insurance inspired color palette
"""

import reflex as rx
from datetime import datetime, timedelta

def claim_form_page():
    """Professional claim form page with Zurich Insurance inspired design."""
    
    return rx.box(
        # Professional Header with Zurich-inspired design
        rx.box(
            rx.vstack(
                # Logo/Title Section
                rx.box(
                    rx.hstack(
                        rx.box(
                            rx.text(
                                "ZURICH",
                                class_name="text-3xl font-bold text-white tracking-wider"
                            ),
                            class_name="bg-blue-600 px-4 py-2 rounded-lg"
                        ),
                        rx.text(
                            "INSURANCE",
                            class_name="text-2xl font-light text-gray-300 tracking-wide ml-2"
                        ),
                        class_name="items-center"
                    ),
                    class_name="mb-6"
                ),
                rx.heading(
                    "Claims Management System",
                    class_name="text-4xl md:text-5xl font-bold text-white text-center mb-4 tracking-tight"
                ),
                rx.text(
                    "Professional Insurance Claim Submission",
                    class_name="text-xl text-blue-100 text-center font-medium mb-2"
                ),
                rx.text(
                    "Complete all sections below to submit your claim for processing",
                    class_name="text-lg text-gray-300 text-center font-light"
                ),
                rx.divider(class_name="w-32 mx-auto border-blue-400 my-6 opacity-60"),
                class_name="max-w-5xl mx-auto px-6"
            ),
            class_name="w-full py-20 bg-gradient-to-br from-slate-800 via-blue-900 to-slate-900 shadow-2xl relative overflow-hidden"
        ),
        
        # Main Form Container with professional styling
        rx.box(
            rx.form(
                rx.vstack(
                    # Progress Indicator
                    rx.box(
                        rx.hstack(
                            rx.box(
                                rx.text("1", class_name="text-white font-bold"),
                                class_name="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center"
                            ),
                            rx.divider(class_name="flex-1 border-blue-300"),
                            rx.box(
                                rx.text("2", class_name="text-white font-bold"),
                                class_name="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center"
                            ),
                            rx.divider(class_name="flex-1 border-gray-300"),
                            rx.box(
                                rx.text("3", class_name="text-white font-bold"),
                                class_name="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center"
                            ),
                            class_name="w-full max-w-md mx-auto"
                        ),
                        class_name="mb-8"
                    ),
                    
                    # Step 1: Coverage Type Selection
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("1", class_name="text-white font-bold text-sm"),
                                    class_name="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"
                                ),
                                rx.heading(
                                    "Coverage Type Selection", 
                                    class_name="text-2xl font-bold text-slate-800"
                                ),
                                class_name="items-center mb-6"
                            ),
                            rx.text(
                                "Please select the type of coverage for your claim",
                                class_name="text-gray-600 mb-6 text-center"
                            ),
                            rx.select(
                                placeholder="Select your coverage type",
                                items=[
                                    "Trip Cancellation",
                                    "Trip Delay", 
                                    "Trip Interruption",
                                    "Baggage Delay",
                                    "Medical Emergency",
                                    "Accident & Sickness"
                                ],
                                class_name="w-full p-4 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm text-gray-700"
                            ),
                            class_name="w-full"
                        ),
                        class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8"
                    ),
                    
                    # Step 2: Claimant Information
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("2", class_name="text-white font-bold text-sm"),
                                    class_name="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"
                                ),
                                rx.heading(
                                    "Personal Information", 
                                    class_name="text-2xl font-bold text-slate-800"
                                ),
                                class_name="items-center mb-6"
                            ),
                            
                            # Primary Contact Information
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Primary Contact",
                                        class_name="text-lg font-semibold text-slate-700 mb-4"
                                    ),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Full Name *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.input(
                                                placeholder="Enter your complete name",
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                                required=True,
                                                pattern="[A-Za-z ]{2,50}"
                                            ),
                                            class_name="flex-1"
                                        ),
                                        rx.vstack(
                                            rx.text("Email Address *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.input(
                                                placeholder="your.email@example.com",
                                                type_="email",
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                                required=True
                                            ),
                                            class_name="flex-1"
                                        ),
                                        class_name="gap-4 flex-wrap"
                                    ),
                                    class_name="w-full"
                                ),
                                class_name="p-6 bg-gray-50 rounded-lg border border-gray-200"
                            ),
                            
                            # Additional Claimants
                            rx.vstack(
                                rx.text("Additional Claimants", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                rx.text_area(
                                    placeholder="List all additional persons included in this claim (if applicable)",
                                    rows="3",
                                    class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none"
                                ),
                                class_name="w-full mt-6"
                            ),
                            
                            # Contact Information
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Mobile Phone *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="+1 (555) 123-4567",
                                        type_="tel",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                        pattern="[0-9+\-\(\) ]{10,15}"
                                    ),
                                    class_name="flex-1"
                                ),
                                rx.vstack(
                                    rx.text("Alternative Phone", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="Alternative contact number",
                                        type_="tel",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                        pattern="[0-9+\-\(\) ]{10,15}"
                                    ),
                                    class_name="flex-1"
                                ),
                                class_name="gap-4 flex-wrap mt-6"
                            ),
                            
                            # Address Information
                            rx.vstack(
                                rx.text("Complete Mailing Address *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                rx.text_area(
                                    placeholder="Street address, apartment/suite number",
                                    rows="2",
                                    class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none"
                                ),
                                class_name="w-full mt-6"
                            ),
                            
                            rx.hstack(
                                rx.vstack(
                                    rx.text("City *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="City name",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                    ),
                                    class_name="flex-1"
                                ),
                                rx.vstack(
                                    rx.text("State/Province *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="State or province",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                    ),
                                    class_name="flex-1"
                                ),
                                rx.vstack(
                                    rx.text("Postal Code *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="ZIP/Postal code",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                        pattern="[A-Za-z0-9 ]{3,10}"
                                    ),
                                    class_name="flex-1"
                                ),
                                class_name="gap-4 flex-wrap mt-6"
                            ),
                            
                            # Policy Information
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Policy Information",
                                        class_name="text-lg font-semibold text-slate-700 mb-4"
                                    ),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Policy Number *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.input(
                                                placeholder="Enter your policy number",
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",
                                                pattern="[A-Za-z0-9\-]{5,20}"
                                            ),
                                            class_name="flex-1"
                                        ),
                                        rx.vstack(
                                            rx.text("Travel Agency", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.input(
                                                placeholder="Agency or company name",
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                            ),
                                            class_name="flex-1"
                                        ),
                                        class_name="gap-4 flex-wrap"
                                    ),
                                    rx.vstack(
                                        rx.text("Initial Deposit Date", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                        rx.input(
                                            placeholder="Select deposit date",
                                            type_="date",
                                            max=datetime.now().strftime("%Y-%m-%d"),
                                            class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm cursor-pointer"
                                        ),
                                        class_name="w-full mt-4"
                                    ),
                                    class_name="w-full"
                                ),
                                class_name="p-6 bg-gray-50 rounded-lg border border-gray-200 mt-6"
                            ),
                            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8"
                        ),
                    ),
                    
                    # Step 3: Incident Details
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.text("3", class_name="text-white font-bold text-sm"),
                                    class_name="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"
                                ),
                                rx.heading(
                                    "Incident Details", 
                                    class_name="text-2xl font-bold text-slate-800"
                                ),
                                class_name="items-center mb-6"
                            ),
                            
                            # Incident Date and Location
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Date of Incident *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="Select incident date",
                                        type_="date",
                                        max=datetime.now().strftime("%Y-%m-%d"),
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm cursor-pointer"
                                    ),
                                    class_name="flex-1"
                                ),
                                rx.vstack(
                                    rx.text("Time of Incident", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                    rx.input(
                                        placeholder="Approximate time",
                                        type_="time",
                                        class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                    ),
                                    class_name="flex-1"
                                ),
                                class_name="gap-4 flex-wrap"
                            ),
                            
                            # Incident Location
                            rx.vstack(
                                rx.text("Location of Incident *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                rx.text_area(
                                    placeholder="Describe where the incident occurred (city, country, specific location)",
                                    rows="3",
                                    class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none"
                                ),
                                class_name="w-full mt-6"
                            ),
                            
                            # Detailed Description
                            rx.vstack(
                                rx.text("Detailed Description of Incident *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                rx.text_area(
                                    placeholder="Provide a detailed description of what happened, including all relevant details, circumstances, and any witnesses",
                                    rows="6",
                                    class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none"
                                ),
                                class_name="w-full mt-6"
                            ),
                            
                            # Financial Impact
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "Financial Impact",
                                        class_name="text-lg font-semibold text-slate-700 mb-4"
                                    ),
                                    rx.hstack(
                                        rx.vstack(
                                            rx.text("Estimated Loss Amount *", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.input(
                                                placeholder="0.00",
                                                type_="number",
                                                min="0",
                                                step="0.01",
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                            ),
                                            class_name="flex-1"
                                        ),
                                        rx.vstack(
                                            rx.text("Currency", class_name="text-sm font-semibold text-slate-700 mb-2"),
                                            rx.select(
                                                placeholder="Select currency",
                                                items=["USD", "EUR", "CAD", "GBP", "MXN"],
                                                class_name="w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"
                                            ),
                                            class_name="flex-1"
                                        ),
                                        class_name="gap-4 flex-wrap"
                                    ),
                                    class_name="w-full"
                                ),
                                class_name="p-6 bg-gray-50 rounded-lg border border-gray-200 mt-6"
                            ),
                            class_name="p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8"
                        ),
                    ),
                    
                    # Submit Button Section
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "By submitting this form, you confirm that all information provided is accurate and complete.",
                                class_name="text-sm text-gray-600 text-center mb-6"
                            ),
                            rx.button(
                                "Submit Claim",
                                type_="submit",
                                class_name="w-full md:w-auto px-12 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold text-lg rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                            ),
                            rx.text(
                                "You will receive a confirmation email with your claim number",
                                class_name="text-xs text-gray-500 text-center mt-4"
                            ),
                            class_name="w-full text-center"
                        ),
                        class_name="p-8 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl shadow-lg border border-gray-200"
                    ),
                    
                    spacing="0",
                    class_name="max-w-4xl mx-auto px-4 py-8"
                ),
                class_name="w-full"
            ),
            class_name="w-full bg-gray-100 min-h-screen"
        )
    ) 