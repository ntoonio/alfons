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
		return "<div class='action action-onoff'><button onclick='mqttPublish(\"" + component["topic"] + "\", \"ON\")'>On</button><button onclick='mqttPublish(\"" + component["topic"] + "\", \"OFF\")'>Off</button></div>"
	}
	else {
		return "<p>Error, unknown type</p>"
	}
}

function printComponents() {
	const componentList = document.getElementById("component-list")
	
	componentList.innerHTML = ""

	const components = localStorage.getItem("components")
	
	if (components == undefined) { return }

	var i = 0
	JSON.parse(components).forEach(component => {
		const row = "<div class='row'><div class='row-name col-xl-4 col-lg-4 col-md-6 col-sm-8 col-7'><p>" + component["name"] + "</p></div><div class='row-action col-xl-8 col-lg-8 col-md-6 col-sm-4 col-5'>" + createActionHTML(component) + "</div></div>"

		componentList.innerHTML += row
		
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