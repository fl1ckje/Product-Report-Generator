pyinstaller --onefile main.py ^
    --add-data="cfg/ozon.json:cfg" ^
    --windowed