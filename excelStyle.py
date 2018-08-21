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
header = NamedStyle(name="header")
header.font = brightFont
header.fill = PatternFill("solid", fgColor="0000FF")
bd = Side(style='thick', color="000000")
header.border = Border(left=bd, top=bd, right=bd, bottom=bd)
header.alignment = alignment


def getHeaderStyle():
    return header


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


def getProjHeaderStyle():
    return projHeader


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


def getBodyStyle():
    return bodyStyle
