#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = "valenceb"

from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill, Alignment

brightFont = Font(name='Calibri',
                  size=11,
                  bold=True,
                  italic=False,
                  vertAlign=None,
                  underline='none',
                  strike=False,
                  color='FFFFFF')
alignment = Alignment(horizontal='general',
                      vertical='center',
                      text_rotation=0,
                      wrap_text=True,
                      shrink_to_fit=False,
                      indent=0)

bd = Side(style='thick', color="000000")


def getHeaderStyle():
    header = NamedStyle(name="header")
    header.font = brightFont
    header.fill = PatternFill("solid", fgColor="0000FF")
    header.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    header.alignment = alignment
    return header


def getProjHeaderStyle():
    projHeader = NamedStyle(name="projHeader")
    projHeader.font = Font(name='Calibri',
                           size=11,
                           bold=True,
                           italic=False,
                           vertAlign=None,
                           underline='none',
                           strike=False,
                           color='000000')
    projHeader.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    projHeader.alignment = alignment
    return projHeader


def getBodyStyle():
    bodyStyle = NamedStyle(name="body")
    bodyStyle.font = Font(name='Calibri',
                          size=11,
                          bold=False,
                          italic=False,
                          vertAlign=None,
                          underline='none',
                          strike=False,
                          color='202020')
    bodyStyle.boder = Border(left=bd, top=bd, right=bd, bottom=bd)
    bodyStyle.alignment = alignment
    return bodyStyle

def getBlackFont():
    blackFont = NamedStyle(name="blackFont")
    blackFont.font = Font(name='Calibri',
                          size=11,
                          bold=False,
                          italic=False,
                          vertAlign=None,
                          underline='none',
                          strike=False,
                          color='000000')
    blackFont.boder = Border(left=bd, top=bd, right=bd, bottom=bd)
    blackFont.alignment = alignment
    return blackFont
