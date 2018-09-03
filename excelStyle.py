#!/usr/bin/env python 
# -*- coding:utf-8 -*-
__author__ = "valenceb"

from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill, Alignment

brightFont = Font(name='Arial',
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

bd = Side(style='thin', color="0088FF")


def getHeaderStyle():
    header = NamedStyle(name="header")
    header.font = brightFont
    header.fill = PatternFill("solid", fgColor="0000FF")
    header.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    header.alignment = Alignment(horizontal='center',
                      vertical='center',
                      text_rotation=0,
                      wrap_text=True,
                      shrink_to_fit=False,
                      indent=0)
    return header


def getProjHeaderStyle():
    projHeader = NamedStyle(name="projHeader")
    projHeader.font = Font(name='Arial',
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
    bodyStyle = NamedStyle(name="backlog")
    bodyStyle.font = Font(name='Arial',
                          size=11,
                          bold=False,
                          italic=False,
                          vertAlign=None,
                          underline='none',
                          strike=False,
                          color='909090')
    bodyStyle.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    bodyStyle.alignment = Alignment(horizontal='general',
                      vertical='top',
                      text_rotation=0,
                      wrap_text=True,
                      shrink_to_fit=False,
                      indent=0)
    return bodyStyle

def getBlackFont():
    blackFont = NamedStyle(name="blackFont")
    blackFont.font = Font(name='Arial',
                          size=11,
                          bold=False,
                          italic=False,
                          vertAlign=None,
                          underline='none',
                          strike=False,
                          color='000000')
    blackFont.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    blackFont.alignment = Alignment(horizontal='general',
                      vertical='top',
                      text_rotation=0,
                      wrap_text=True,
                      shrink_to_fit=False,
                      indent=0)
    return blackFont
