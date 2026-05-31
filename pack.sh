rm -rf app.app app.build app.dist __pycache__ .nuitka-cache nuitka-crash-report.xml
nuitka \
--onefile \
--follow-imports \
--include-data-dir=templates=templates \
--include-data-dir=static=static \
--include-data-dir=data=data \
--include-data-file=global_config.json=global_config.json \
--include-data-file=city_config.json=city_config.json \
--include-data-file=current_state.json=current_state.json \
--remove-output \
app.py