
pip -V
#pip install --target=local_lib --upgrade --no-cache-dir git+https://github.com/jaraco/path.git > install_path.log 2>&1
PYTHONPATH=local_lib pip show path > /dev/null 2>&1
if [ $? -eq 0 ]; then
    PYTHONPATH=local_lib python3 my_program.py
else
    echo "Échec : package non trouvé"
fi
