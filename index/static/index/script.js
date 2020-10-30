document.addEventListener("DOMContentLoaded", () => {
	const csrf = Cookies.get('csrftoken');
	document.querySelectorAll("#delete").forEach(element => {
		element.addEventListener('click', btn => {
			fetch('/delete', {
				method: "POST",
				headers: {'X-CSRFToken': csrf},
				body: JSON.stringify({
					passcode: element.dataset.delete
				})
			})
			.then(response => response.json())
			.then(result => {
				if(result.message === "Success"){
					element.parentNode.parentNode.parentNode.removeChild(element.parentNode.parentNode);
				}
			})
		})
	})
})