mkdir $1/rescued
for file in $1*; do
	date=$(exif $file -t=0x0132 -m | sed "s/://g")
	if [ -n "$file" ]; then
		mv $file "$1/rescued/${date}.jpg"
	fi
done
