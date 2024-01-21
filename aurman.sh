#/usr/bin/bash
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

list () {
	for dir in ~/AUR/*/
	do
		dir=${dir%*/}      # remove the trailing "/"
		pacman -Q "${dir##*/}"    # print everything after the final ""
	done
}

remove () {
	dir=$1
	if [ -d ~/AUR/$dir/ ]
	then
		sudo pacman -Rs $dir
		echo "cleaning up files"
		rm -fr ~/AUR/$dir

	else
		echo "package ${dir} is not known"
	fi	
}

help () {
	echo "
Script for managing all the AURs. 
Requires a folder ~/AUR/ to exist.
All AURs will be installed with as a git repo clone into this folder. updating will update all AURs in that folder
usage: aurman [option] 
      	-l:		list all installed packages
	-u: 		update all installed packages
   	-i <arg>: 	install AUR package from <args> git repo link
       	-r <arg>: 	remove an installed package
	-h: 		show this helptext"
}

set -e
# unsetting name in case it was set
noargs="true"
while getopts "r:huli:" opt; do
	case "$opt" in
		"i" ) install $OPTARG;;
		"u" ) update;;
		"l" ) list;;
		"r" ) remove $OPTARG;;
		"h" | * ) help;;
	esac
	noargs="false"
done

[[ "$noargs" == "true" ]] && help

exit 0
