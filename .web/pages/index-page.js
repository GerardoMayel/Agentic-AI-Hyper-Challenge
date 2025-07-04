/** @jsxImportSource @emotion/react */


import { Fragment } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Separator as RadixThemesSeparator, Text as RadixThemesText } from "@radix-ui/themes"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export default function Component() {
    




  return (
    jsx(
Fragment,
{},
jsx(
RadixThemesBox,
{className:"min-h-screen"},
jsx(
RadixThemesBox,
{className:"w-full py-24 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-6xl mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-5xl md:text-7xl font-bold text-white text-center mb-6 tracking-tight"},
"Zurich Insurance"
,),jsx(
RadixThemesHeading,
{className:"text-3xl md:text-4xl font-semibold text-blue-100 text-center mb-8"},
"Claims Management System"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xl text-blue-200 text-center max-w-3xl mb-12 leading-relaxed"},
"Professional insurance claims processing with advanced automation"
,),jsx(RadixThemesSeparator,{className:"w-32 mx-auto border-blue-300 my-8",size:"4"},)
,jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-6 flex-wrap justify-center",direction:"row",gap:"3"},
jsx(
RadixThemesButton,
{className:"bg-white text-slate-800 px-12 py-4 rounded-2xl font-bold text-lg hover:bg-blue-50 transition-all duration-300 transform hover:scale-105 shadow-2xl"},
"Submit Claim"
,),jsx(
RadixThemesButton,
{className:"border-2 border-white text-white px-12 py-4 rounded-2xl font-bold text-lg hover:bg-white hover:text-slate-800 transition-all duration-300 transform hover:scale-105"},
"View Dashboard"
,),),),),jsx(
RadixThemesBox,
{className:"w-full py-20 bg-gradient-to-br from-slate-50 to-blue-50"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-7xl mx-auto",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-slate-800 text-center mb-16"},
"Why Choose Our System?"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-8 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-6xl mb-6"},
"\ud83d\ude80"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-4"},
"Fast Processing"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 text-center leading-relaxed"},
"Automated claims processing with AI-powered document analysis for faster turnaround times."
,),),),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-6xl mb-6"},
"\ud83d\udd12"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-4"},
"Secure & Reliable"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 text-center leading-relaxed"},
"Enterprise-grade security with encrypted data storage and secure document handling."
,),),),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-6xl mb-6"},
"\ud83d\udcf1"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-4"},
"Mobile Friendly"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 text-center leading-relaxed"},
"Responsive design that works perfectly on all devices - desktop, tablet, and mobile."
,),),),),),),jsx(
RadixThemesBox,
{className:"w-full py-20 bg-gradient-to-br from-slate-800 via-blue-800 to-blue-700"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-6xl mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-white text-center mb-16"},
"Our Track Record"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-8 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesBox,
{className:"flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-5xl font-bold text-blue-200 mb-2"},
"10,000+"
,),jsx(
RadixThemesText,
{as:"p",className:"text-blue-100 text-lg font-medium"},
"Claims Processed"
,),),),jsx(
RadixThemesBox,
{className:"flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-5xl font-bold text-blue-200 mb-2"},
"99.9%"
,),jsx(
RadixThemesText,
{as:"p",className:"text-blue-100 text-lg font-medium"},
"Uptime"
,),),),jsx(
RadixThemesBox,
{className:"flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-5xl font-bold text-blue-200 mb-2"},
"< 24h"
,),jsx(
RadixThemesText,
{as:"p",className:"text-blue-100 text-lg font-medium"},
"Average Response"
,),),),jsx(
RadixThemesBox,
{className:"flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-5xl font-bold text-blue-200 mb-2"},
"4.9/5"
,),jsx(
RadixThemesText,
{as:"p",className:"text-blue-100 text-lg font-medium"},
"Customer Rating"
,),),),),),),jsx(
RadixThemesBox,
{className:"w-full py-20 bg-white"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-4xl mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-slate-800 text-center mb-8"},
"Ready to Get Started?"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xl text-slate-600 text-center max-w-3xl mb-12"},
"Join thousands of satisfied customers who trust our claims management system"
,),jsx(
RadixThemesButton,
{className:"bg-gradient-to-r from-blue-600 to-blue-700 text-white px-12 py-6 rounded-2xl font-bold text-xl hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-2xl"},
"Submit Your First Claim"
,),),),jsx(
RadixThemesBox,
{className:"w-full py-12 bg-slate-50 border-t border-slate-200"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-4xl mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-center"},
"\u00a9 2024 Zurich Insurance. All rights reserved."
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-400 text-center text-sm"},
"Professional insurance solutions for a secure future"
,),),),),jsx(
NextHead,
{},
jsx(
"title",
{},
"App | Index-Page"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
