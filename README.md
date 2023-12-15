for i in */; do (cd "$i" && zip -r "../${i%/}.zip" *); done
