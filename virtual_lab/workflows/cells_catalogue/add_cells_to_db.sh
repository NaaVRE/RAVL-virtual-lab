#!/bin/bash

# Merge NaaVRE_cells_RAVL/json into  NaaVRE_db.json, creating a backup
# of the original NaaVRE_db.json

set -e

backup_file() {
  filename="$1"

  next_bkp_num=$(find "$(dirname "$filename")" -maxdepth 1 -iname "$(basename "$filename").bkp.*" | \
    sed "s%.\+\/$(basename "$filename")\.bkp\.\([0-9]\+\)$%\1%g" | \
    sort -n | \
    tail -1 | \
    awk '{print $1 + 1}')
  [ -z "$next_bkp_num" ] && next_bkp_num=0

  filename_bkp="$filename.bkp.$next_bkp_num"

  cp "$filename" "$filename_bkp"
}

files_are_different() {
  cmp --silent "$1" "$2"
  echo $?
}


script_dir="$(dirname "$0")"
db_dir="$HOME/NaaVRE"
file_cells="$script_dir/NaaVRE_cells_RAVL.json"
file_db="$db_dir/NaaVRE_db.json"
file_db_merged="$db_dir/NaaVRE_db_merged.json"

jq -s '.[0] * .[1]' "$file_db" "$file_cells" > "$file_db_merged"

db_changed="$(files_are_different "$file_db" "$file_db_merged")"
if (( db_changed )); then
  backup_file "$file_db"
  mv "$file_db_merged" "$file_db"
else
  rm "$file_db_merged"
fi