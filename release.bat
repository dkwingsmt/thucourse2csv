@echo off
python26 py2exe_setup.py
move dist thucourse2csv
zip -0 -r thucourse2csv thucourse2csv.zip
del -r thucourse2csv
@echo on
echo Done.
