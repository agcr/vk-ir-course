URL="$1"
DST_FILE="$2"

function getPageInformation() {
	local pageUrl="$1"

	wget --quiet -O - "$pageUrl" > page.html
	wget --quiet -O - "$pageUrl" | sed -n "/window.cloudSettings/,/};<\/script>/p"
}

function ensureFileExists() {
	local pageInformation="$1"

	echo "$pageInformation" |  grep -q '"not_exists"' && {
		echo "Error: file does not exist" >&2
		exit 1
	}
}

function extractDownloadUrl() {
	local pageUrl="$1" pageInformation="$2" storageUrl filePath

	storageUrl=$(echo "$pageInformation" | sed -r 's|</?script[^>]*>|\n|g' | sed -n 's|.*\(window.cloudSettings=.*}\)|\1|p' | sed -n 's/.*\(weblink_get[^}]*}\).*/\1/p' | sed -n 's|.*\(https://[^"]*\)".*|\1|p')
  filePath=$(echo "$pageUrl" | awk -F '/public/' '{print $2}')

	[ -z "$storageUrl" ] || [ -z "$filePath" ] && {
		echo "Error: failed to extract storage's url or file path" >&2
		exit 1
	}

	echo "$storageUrl/$filePath"
}

pageInformation=$(getPageInformation "$URL")
ensureFileExists "$pageInformation"
downloadUrl=$(extractDownloadUrl "$URL" "$pageInformation")

wget --continue --no-check-certificate --referer="$URL" "$downloadUrl" -O "$DST_FILE"
rm -f page.html
