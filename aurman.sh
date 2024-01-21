
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

while getopts "ui:" opt; do
	case "$opt" in
		"i" ) install $OPTARG;;
		"u" ) update;;
	esac
done
exit 0
