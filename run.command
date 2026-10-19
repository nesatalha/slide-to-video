#!/bin/bash
# Mac'te Finder'dan çift tıklayarak kaynak koddan çalıştırmak için (Terminal penceresi açılır).
cd "$(dirname "$0")"
./run.sh
status=$?
echo
read -n 1 -s -r -p "Pencereyi kapatmak için bir tuşa basın."
exit $status
