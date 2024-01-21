
update () {
	echo "updating"
	for dir in ~/AUR/*/
	do
		cd ~/AUR/dropbox
		git clean -dfx
		git fetch origin
		curr=$(git rev-parse HEAD)
		target=$(git rev-parse @{u})
		if [[ "$curr" != "$target" ]]; then
			git pull
			makepkg -sic --needed
		fi
	done
}

install () {
	echo "installing" 
	dir=$1
	cd ~/AUR/
	git clone $1
	cd "$(basename "$_" .git)"
	makepkg -sic
}

help () {
	echo "
Script for managing all the AURs. 
Requires a folder ~/AUR/ to exist.
All AURs will be installed with as a git repo clone into this folder. updating will update all AURs in that folder
usage: aurman [option] 
      	-u: 		update existing packages
   	-i <arg>: 	install AUR package from <args> git repo link
       	-h: 		show this helptext"
}

# unsetting name in case it was set
noargs="true"
while getopts "hui:" opt; do
	case "$opt" in
		"i" ) install $OPTARG;;
		"u" ) update;;
		"h" | * ) help;;
	esac
	noargs="false"
done

[[ "$noargs" == "true" ]] && help

exit 0
