function getHttp(url) {
    return new Promise((resolve) => {
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                resolve(this.responseText);
            }
        };
        xhttp.open("GET", url);
        xhttp.send();
    });
}

let btn_open = document.getElementById('btn-open');
btn_open.addEventListener('click', () => {
	let promise = getHttp('/open-door/?args=2');
	promise.then((fulfilled) => {
		let reply = JSON.parse(fulfilled)
		console.log(reply.message);
		if (reply.message == 'fail') {
			if (confirm('The gate is still moving. It is going to stop in ' + reply.time_left + ' seconds. Are you sure you want to proceed?')) {
				getHttp('/open-door/?args=0&forced=true');
			}
		} else if (reply.message == 'unauthorized') {
			alert('Please connect to our wifi network to open the gate.')
		}
	}).catch((error) => {
		console.log(error.message);
	})
});

try {
	let btn_open_slightly = document.getElementById('btn-open-slightly');
	let btn_open_hold = document.getElementById('btn-open-hold');
	btn_open_slightly.addEventListener('click', () => {
		let promise = getHttp('/open-door/?args=3');
		promise.then((fulfilled) => {
			let reply = JSON.parse(fulfilled);
			console.log(reply.message);
			if (reply.message == 'fail') {
				if (confirm('The gate is still moving. It is going to stop in ' + reply.time_left + ' seconds. Are you sure you want to proceed?')) {
					getHttp('/open-door/?args=1&forced=true');
				}
			} else if (reply.message == 'unauthorized') {
				alert('Please connect to our wifi network to open the gate.')
			}
		}).catch((error) => {
			console.log(error.message);
		})
	});
	btn_open_hold.addEventListener('click', () => {
		let promise = getHttp('/open-door/?args=4');
		promise.then((fulfilled) => {
			let reply = JSON.parse(fulfilled);
			console.log(reply.message);
			if (reply.message == 'fail') {
				if (confirm('The gate is still moving. It is going to stop in ' + reply.time_left + ' seconds. Are you sure you want to proceed?')) {
					getHttp('/open-door/?args=1&forced=true');
				}
			} else if (reply.message == 'unauthorized') {
				alert('Please connect to our wifi network to open the gate.')
			}
		}).catch((error) => {
			console.log(error.message);
		})
	});

} catch(exception) {
	console.log('Error thrown: ' + exception.message);
}