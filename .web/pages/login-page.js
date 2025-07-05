/** @jsxImportSource @emotion/react */


import { Fragment } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Checkbox as RadixThemesCheckbox, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, Separator as RadixThemesSeparator, Text as RadixThemesText, TextField as RadixThemesTextField } from "@radix-ui/themes"
import NextLink from "next/link"
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
{className:"w-full min-h-screen py-12 bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800 flex items-center justify-center"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack max-w-md mx-auto px-4",direction:"column",gap:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack mb-12",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-4xl md:text-5xl font-bold text-white text-center mb-2 tracking-tight"},
"Zurich Insurance"
,),jsx(
RadixThemesText,
{as:"p",className:"text-xl text-blue-100 text-center font-medium"},
"Claims Management System"
,),jsx(RadixThemesSeparator,{className:"w-24 mx-auto border-blue-300 my-6",size:"4"},)
,),jsx(
RadixThemesBox,
{className:"p-8 bg-white rounded-2xl shadow-2xl border border-slate-100"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full max-w-md",direction:"column",gap:"3"},
jsx(
RadixThemesHeading,
{className:"text-3xl font-bold text-slate-800 text-center mb-2"},
"Welcome Back"
,),jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 text-center mb-8"},
"Sign in to access your dashboard"
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Email Address"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "email" }),placeholder:"Enter your email address",required:true},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full mt-6",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-sm font-semibold text-slate-700 mb-2"},
"Password"
,),jsx(RadixThemesTextField.Root,{className:"w-full p-4 border-2 border-slate-200 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all duration-300 bg-white shadow-sm",css:({ ["type"] : "password" }),placeholder:"Enter your password",required:true},)
,),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack w-full justify-between mt-6",direction:"row",gap:"3"},
jsx(
RadixThemesText,
{as:"label",size:"2"},
jsx(
RadixThemesFlex,
{gap:"2"},
jsx(RadixThemesCheckbox,{className:"text-slate-700 font-medium",size:"2"},)
,"Remember me"
,),),jsx(
RadixThemesLink,
{asChild:true,className:"text-blue-600 hover:text-blue-700 font-medium transition-colors",css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })},
jsx(
NextLink,
{href:"#",passHref:true},
"Forgot password?"
,),),),jsx(
RadixThemesButton,
{className:"w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-8 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-xl mt-8",css:({ ["type"] : "submit" })},
"Sign In"
,),),),jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack mt-8",direction:"column",gap:"3"},
jsx(
RadixThemesText,
{as:"p",className:"text-slate-600 text-center"},
"Don't have an account?"
,),jsx(
RadixThemesLink,
{asChild:true,className:"text-blue-600 hover:text-blue-700 font-medium transition-colors",css:({ ["&:hover"] : ({ ["color"] : "var(--accent-8)" }) })},
jsx(
NextLink,
{href:"#",passHref:true},
"Contact your administrator"
,),),),),),),jsx(
NextHead,
{},
jsx(
"title",
{},
"App | Login-Page"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
