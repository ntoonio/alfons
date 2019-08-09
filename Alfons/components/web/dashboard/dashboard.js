function connect() {
	client.connect({
		onSuccess:onConnect,
		onFailure: function (data) {
			console.log(data)
		},
		mqttVersion: 4,
		userName : localStorage.getItem("username"),
		password : localStorage.getItem("password")
	})
}

function onConnect() {
	console.log("Connected");
}

function onConnectionLost(responseObject) {
	if (responseObject.errorCode !== 0) {
		console.log("Connection lost... " + responseObject.errorMessage);
	}
}

function mqttPublish(topic, message) {
	const msg = new Paho.MQTT.Message(message)
	msg.destinationName = topic
	client.send(msg)
}

function createActionHTML(component) {
	if (component["type"] == "onoff") {
		return "<button onclick='mqttPublish(\"" + component["topic"] + "\", \"ON\")'>On</button><button onclick='mqttPublish(\"" + component["topic"] + "\", \"OFF\")'>Off</button>"
	}
	else {
		return "<p>Error, unknown type</p>"
	}
}

function printComponents() {
	document.getElementById("components-list-table").innerHTML = ""

	const columns = ["name", "action"]
	const headerRow = document.createElement("tr")
	columns.forEach(k => {
		const th = document.createElement("th")
		const p = document.createElement("p")
		
		p.innerText = k.charAt(0).toUpperCase() + k.slice(1).toLowerCase()

		th.appendChild(p)
		headerRow.appendChild(th)
	})
	document.getElementById("components-list-table").appendChild(headerRow)

	const components = localStorage.getItem("components")
	
	if (components == undefined) { return }

	var i = 0
	JSON.parse(components).forEach(component => {
		const tr = document.createElement("tr")
		tr.innerHTML = "<td><p>" + component["name"] + "</p></td><td>" + createActionHTML(component) + "</td>"

		document.getElementById("components-list-table").appendChild(tr)

		i += 1
	})
}

if (localStorage.getItem("username") == undefined || localStorage.getItem("password") == undefined) {
	window.location.href += "credentials/"
}

client = new Paho.MQTT.Client(window.location.hostname, 27371, "web-dashboard-" + localStorage.getItem("client-id"));

client.onConnectionLost = onConnectionLost;

connect()
printComponents()