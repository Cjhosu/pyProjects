for DC in at lc
do      
    for NODE in 1 2      
    do curl -k -s --connect-to ${DC}somehost${NODE}.place.net:433 -H "Host: someapp.place.com" https://someapp.place.com/_ping
    echo    
    done
done
