/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Select as RadixThemesSelect, Separator as RadixThemesSeparator, Text as RadixThemesText, TextArea as RadixThemesTextArea, TextField as RadixThemesTextField } from "@radix-ui/themes"
import { Root as RadixFormRoot } from "@radix-ui/react-form"
import { EventLoopContext } from "$/utils/context"
import { Event, getRefValue, getRefValues } from "$/utils/state"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export function Root_e6f561d708506d0db40975236df8564c () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  
    const handleSubmit_72a9ef97d8ef8f1918e1a837a5797ccb = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(Event("_call_function", ({ ["function"] : (() => null), ["callback"] : null }), ({ ["preventDefault"] : true })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    




  
  return (
    jsx(
RadixFormRoot,
{className:"Root w-full",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_72a9ef97d8ef8f1918e1a837a5797ccb},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-4xl mx-auto px-4 py-8",direction:"column",gap:"0"},
jsx(
RadixThemesBox,
{className:"mb-8"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full max-w-md mx-auto",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold"},
"1"
,),),jsx(RadixThemesSeparator,{className:"flex-1 border-blue-300",size:"4"},)
,jsx(
RadixThemesBox,
{className:"w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold"},
"2"
,),),jsx(RadixThemesSeparator,{className:"flex-1 border-gray-300",size:"4"},)
,jsx(
RadixThemesBox,
{className:"w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold"},
"3"
,),),),),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"column",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack items-center mb-6",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold text-sm"},
"1"
,),),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800"},
"Coverage Type Selection"
,),),jsx(
RadixThemesText,
{as:"p",className:"text-gray-600 mb-6 text-center"},
"Please select the type of coverage for your claim"
,),jsx(
RadixThemesSelect.Root,
{className:"w-full p-4 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm text-gray-700"},
jsx(RadixThemesSelect.Trigger,{placeholder:"Select your coverage type"},)
,jsx(
RadixThemesSelect.Content,
{},
jsx(
RadixThemesSelect.Group,
{},
""
,jsx(
RadixThemesSelect.Item,
{value:"Trip Cancellation"},
"Trip Cancellation"
,),jsx(
RadixThemesSelect.Item,
{value:"Trip Delay"},
"Trip Delay"
,),jsx(
RadixThemesSelect.Item,
{value:"Trip Interruption"},
"Trip Interruption"
,),jsx(
RadixThemesSelect.Item,
{value:"Baggage Delay"},
"Baggage Delay"
,),jsx(
RadixThemesSelect.Item,
{value:"Medical Emergency"},
"Medical Emergency"
,),jsx(
RadixThemesSelect.Item,
{value:"Accident & Sickness"},
"Accident & Sickness"
,),),),),),),jsx(
RadixThemesBox,
{},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8",direction:"column",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack items-center mb-6",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold text-sm"},
"2"
,),),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800"},
"Personal Information"
,),),jsx(
RadixThemesBox,
{className:"p-6 bg-gray-50 rounded-lg border border-gray-200"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-lg font-semibold text-slate-700 mb-4"},
"Primary Contact"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Full Name *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",pattern:"[A-Za-z ]{2,50}",placeholder:"Enter your complete name",required:true},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Email Address *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "email" }),placeholder:"your.email@example.com",required:true},)
,),),),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-6",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Additional Claimants"
,),jsx(RadixThemesTextArea,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none",css:({ ["& textarea"] : null }),placeholder:"List all additional persons included in this claim (if applicable)",rows:"3"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap mt-6",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Mobile Phone *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "tel" }),pattern:"[0-9+\\-\\(\\) ]{10,15}",placeholder:"+1 (555) 123-4567"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Alternative Phone"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "tel" }),pattern:"[0-9+\\-\\(\\) ]{10,15}",placeholder:"Alternative contact number"},)
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-6",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Complete Mailing Address *"
,),jsx(RadixThemesTextArea,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none",css:({ ["& textarea"] : null }),placeholder:"Street address, apartment/suite number",rows:"2"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap mt-6",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"City *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",placeholder:"City name"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"State/Province *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",placeholder:"State or province"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Postal Code *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",pattern:"[A-Za-z0-9 ]{3,10}",placeholder:"ZIP/Postal code"},)
,),),jsx(
RadixThemesBox,
{className:"p-6 bg-gray-50 rounded-lg border border-gray-200 mt-6"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-lg font-semibold text-slate-700 mb-4"},
"Policy Information"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Policy Number *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",pattern:"[A-Za-z0-9\\-]{5,20}",placeholder:"Enter your policy number"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Travel Agency"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",placeholder:"Agency or company name"},)
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-4",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Initial Deposit Date"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm cursor-pointer",css:({ ["type"] : "date" }),max:"2025-07-01",placeholder:"Select deposit date"},)
,),),),),),jsx(
RadixThemesBox,
{},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack p-8 bg-white rounded-xl shadow-lg border border-gray-100 mb-8",direction:"column",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack items-center mb-6",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center mr-3"},
jsx(
RadixThemesText,
{as:"p",className:"text-white font-bold text-sm"},
"3"
,),),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800"},
"Incident Details"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Date of Incident *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm cursor-pointer",css:({ ["type"] : "date" }),max:"2025-07-01",placeholder:"Select incident date"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Time of Incident"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "time" }),placeholder:"Approximate time"},)
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-6",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Location of Incident *"
,),jsx(RadixThemesTextArea,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none",css:({ ["& textarea"] : null }),placeholder:"Describe where the incident occurred (city, country, specific location)",rows:"3"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-6",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Detailed Description of Incident *"
,),jsx(RadixThemesTextArea,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm resize-none",css:({ ["& textarea"] : null }),placeholder:"Provide a detailed description of what happened, including all relevant details, circumstances, and any witnesses",rows:"6"},)
,),jsx(
RadixThemesBox,
{className:"p-6 bg-gray-50 rounded-lg border border-gray-200 mt-6"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-lg font-semibold text-slate-700 mb-4"},
"Financial Impact"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-4 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Estimated Loss Amount *"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "number" }),min:"0",placeholder:"0.00",step:"0.01"},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Currency"
,),jsx(
RadixThemesSelect.Root,
{className:"w-full p-3 border-2 border-gray-200 rounded-lg focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm"},
jsx(RadixThemesSelect.Trigger,{placeholder:"Select currency"},)
,jsx(
RadixThemesSelect.Content,
{},
jsx(
RadixThemesSelect.Group,
{},
""
,jsx(
RadixThemesSelect.Item,
{value:"USD"},
"USD"
,),jsx(
RadixThemesSelect.Item,
{value:"EUR"},
"EUR"
,),jsx(
RadixThemesSelect.Item,
{value:"CAD"},
"CAD"
,),jsx(
RadixThemesSelect.Item,
{value:"GBP"},
"GBP"
,),jsx(
RadixThemesSelect.Item,
{value:"MXN"},
"MXN"
,),),),),),),),),),),jsx(
RadixThemesBox,
{className:"p-8 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl shadow-lg border border-gray-200"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm text-gray-600 text-center mb-6"},
"By submitting this form, you confirm that all information provided is accurate and complete."
,),jsx(
RadixThemesButton,
{className:"w-full md:w-auto px-12 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold text-lg rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105",css:({ ["type"] : "submit" })},
"Submit Claim"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xs text-gray-500 text-center mt-4"},
"You will receive a confirmation email with your claim number"
,),),),),)
  )
}

export default function Component() {
    




  return (
    jsx(
Fragment,
{},
jsx(
RadixThemesBox,
{},
jsx(
RadixThemesBox,
{className:"w-full py-20 bg-gradient-to-br from-slate-800 via-blue-900 to-slate-900 shadow-2xl relative overflow-hidden"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-5xl mx-auto px-6",direction:"column",gap:"3"},
jsx(
RadixThemesBox,
{className:"mb-6"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack items-center",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"bg-blue-600 px-4 py-2 rounded-lg"},
jsx(
RadixThemesText,
{as:"p",className:"text-3xl font-bold text-white tracking-wider"},
"ZURICH"
,),),jsx(
RadixThemesText,
{as:"p",className:"text-2xl font-light text-gray-300 tracking-wide ml-2"},
"INSURANCE"
,),),),jsx(
RadixThemesHeading,
{className:"text-4xl md:text-5xl font-bold text-white text-center mb-4 tracking-tight"},
"Claims Management System"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xl text-blue-100 text-center font-medium mb-2"},
"Professional Insurance Claim Submission"
,),jsx(
RadixThemesText,
{as:"p",className:"text-lg text-gray-300 text-center font-light"},
"Complete all sections below to submit your claim for processing"
,),jsx(RadixThemesSeparator,{className:"w-32 mx-auto border-blue-400 my-6 opacity-60",size:"4"},)
,),),jsx(
RadixThemesBox,
{className:"w-full bg-gray-100 min-h-screen"},
jsx(Root_e6f561d708506d0db40975236df8564c,{},)
,),),jsx(
NextHead,
{},
jsx(
"title",
{},
"App | Claim-Form"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
