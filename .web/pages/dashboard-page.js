/** @jsxImportSource @emotion/react */


import { Fragment } from "react"
import { Badge as RadixThemesBadge, Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Separator as RadixThemesSeparator, Text as RadixThemesText } from "@radix-ui/themes"
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
{className:"w-full py-16 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 shadow-2xl relative overflow-hidden"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-4xl mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-4xl md:text-5xl font-bold text-white text-center mb-4 tracking-tight"},
"Claims Dashboard"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xl text-blue-100 text-center font-medium"},
"Monitor and manage insurance claims"
,),jsx(RadixThemesSeparator,{className:"w-24 mx-auto border-blue-300 my-4",size:"4"},)
,),),jsx(
RadixThemesBox,
{className:"w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-7xl mx-auto",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-3xl font-bold text-slate-800 text-center mb-12"},
"System Overview"
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
{as:"p",className:"text-5xl mb-4"},
"\ud83d\udcca"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-2"},
"Total Claims"
,),jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-blue-600 mb-2"},
"1,247"
,),jsx(
RadixThemesText,
{as:"p",className:"text-green-600 font-semibold"},
"+12% this month"
,),),),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-5xl mb-4"},
"\u23f3"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-2"},
"Pending"
,),jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-orange-600 mb-2"},
"89"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 font-medium"},
"Under review"
,),),),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-5xl mb-4"},
"\u2705"
,),jsx(
RadixThemesHeading,
{className:"text-2xl font-bold text-slate-800 mb-2"},
"Approved"
,),jsx(
RadixThemesHeading,
{className:"text-4xl font-bold text-green-600 mb-2"},
"1,158"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 font-medium"},
"92.9% approval rate"
,),),),),),),jsx(
RadixThemesBox,
{className:"w-full py-16 bg-white"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-7xl mx-auto",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-3xl font-bold text-slate-800 text-center mb-12"},
"Recent Claims"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack space-y-6 max-w-4xl mx-auto w-full",direction:"column",gap:"3"},
jsx(
RadixThemesBox,
{className:"p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800 text-lg"},
"CLM-2024-001"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600"},
"John Smith"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-medium text-slate-700"},
"Trip Cancellation"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-green-600 text-lg"},
"$2,500"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesBadge,
{className:"bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"},
"Approved"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-sm"},
"2024-01-15"
,),),),),jsx(
RadixThemesBox,
{className:"p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800 text-lg"},
"CLM-2024-002"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600"},
"Maria Garcia"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-medium text-slate-700"},
"Baggage Delay"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-orange-600 text-lg"},
"$800"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesBadge,
{className:"bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium"},
"Pending"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-sm"},
"2024-01-14"
,),),),),jsx(
RadixThemesBox,
{className:"p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800 text-lg"},
"CLM-2024-003"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600"},
"David Johnson"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-medium text-slate-700"},
"Trip Interruption"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-green-600 text-lg"},
"$1,200"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesBadge,
{className:"bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium"},
"Approved"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-sm"},
"2024-01-13"
,),),),),jsx(
RadixThemesBox,
{className:"p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800 text-lg"},
"CLM-2024-004"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600"},
"Sarah Wilson"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-medium text-slate-700"},
"Trip Delay"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-blue-600 text-lg"},
"$300"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesBadge,
{className:"bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"},
"In Review"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-sm"},
"2024-01-12"
,),),),),jsx(
RadixThemesBox,
{className:"p-6 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"row",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800 text-lg"},
"CLM-2024-005"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600"},
"Michael Brown"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"font-medium text-slate-700"},
"Trip Cancellation"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-red-600 text-lg"},
"$1,800"
,),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack flex-1 text-center",direction:"column",gap:"3"},
jsx(
RadixThemesBadge,
{className:"bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium"},
"Rejected"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-500 text-sm"},
"2024-01-11"
,),),),),),),),jsx(
RadixThemesBox,
{className:"w-full py-16 bg-gradient-to-br from-slate-50 to-blue-50"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-5xl mx-auto",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-3xl font-bold text-slate-800 text-center mb-12"},
"Quick Actions"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack gap-8 flex-wrap",direction:"row",gap:"3"},
jsx(
RadixThemesButton,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-4xl mb-3"},
"\ud83d\udccb"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800"},
"New Claim"
,),),),jsx(
RadixThemesButton,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-4xl mb-3"},
"\ud83d\udcca"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800"},
"View Reports"
,),),),jsx(
RadixThemesButton,
{className:"p-8 bg-white rounded-2xl shadow-xl border border-slate-100 hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex-1"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack text-center",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-4xl mb-3"},
"\u2699\ufe0f"
,),jsx(
RadixThemesText,
{as:"p",className:"font-bold text-slate-800"},
"Settings"
,),),),),),),),jsx(
NextHead,
{},
jsx(
"title",
{},
"App | Dashboard-Page"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
