installed=$(pacman -Q)

while read package; do
    for item in $installed
    do
        if [ "$package" == "$item" ]; then
            echo "installed AND in provided list: $package"
        fi
    done
done < $1



