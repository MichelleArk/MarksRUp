if [ $# -ne 2 ]
then
    echo "USAGE: ./checkMarks.sh <UTORID> <PIN>"
else
    ./rosiScraper $1 $2
    while sleep $[$RANDOM % 1800 + 2700];
    caffeinate -t 4500 &
    do ./rosiScraper $1 $2;
    done
fi
