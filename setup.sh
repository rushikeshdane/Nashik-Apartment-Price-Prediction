mkdir -p ~/.streamlit
echo "[theme]
base='light'
primaryColor='#0029f7'
secondaryBackgroundColor='#ffc6a1'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
