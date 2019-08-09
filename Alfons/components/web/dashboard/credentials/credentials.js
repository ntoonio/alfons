function saveCredentials() {
	localStorage.setItem("username", document.getElementById("username-input").value)
	localStorage.setItem("password", document.getElementById("password-input").value)
	localStorage.setItem("client-id", document.getElementById("client-id-input").value)

	var url = window.location.href
	if (url.substr(-1) == "/") url = url.substr(0, url.length - 2)
	url = url.split("/")
	url.pop()
	window.location = url.join("/") + "/"
}

function makeId(length) {
	var result = ""
	var characters = "abcdef0123456789"
	var charactersLength = characters.length
	for (var i = 0; i < length; i++) {
		result += characters.charAt(Math.floor(Math.random() * charactersLength))
	}
	return result
}

document.getElementById("username-input").value = localStorage.getItem("username")
document.getElementById("client-id-input").value = makeId(7)