#!/usr/bin/env python3
"""Заголовок секции тарифов: '2 тарифа' → '5 тарифов' только на telegram-странице."""
from pathlib import Path

F = Path('/root/framerexport/full-site-export-may21/product/product-telegram/index.html')

SCRIPT = (
  '<script id="glavnoe-telegram-tariff-title">'
  '(function(){'
    'function tryReplace(){'
      'var els=document.querySelectorAll("h1,h2,h3");'
      'for(var i=0;i<els.length;i++){'
        'var t=els[i].textContent.trim();'
        'if(t==="2 тарифа"||t==="3 тарифа"){'
          'els[i].textContent="5 тарифов";'
          'return true;'
        '}'
      '}'
      'return false;'
    '}'
    'if(tryReplace())return;'
    'var obs=new MutationObserver(function(){if(tryReplace())obs.disconnect();});'
    'obs.observe(document.body,{childList:true,subtree:true,characterData:true});'
    'setTimeout(function(){obs.disconnect();},8000);'
  '})();'
  '</script>'
)

MARK = 'id="glavnoe-telegram-tariff-title"'
h = F.read_text(encoding='utf-8')
if MARK in h:
    print('SKIP — already injected')
else:
    new = h.replace('</head>', SCRIPT + '</head>', 1)
    F.write_text(new, encoding='utf-8')
    print('OK product-telegram: title 2→5 тарифов script injected')
