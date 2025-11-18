#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
\n\
[theme]\n\
primaryColor = \"#00ffdd\"\n\
backgroundColor = \"#0e1117\"\n\
secondaryBackgroundColor = \"#1e2130\"\n\
textColor = \"#e0e0e0\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml
