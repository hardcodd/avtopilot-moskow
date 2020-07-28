(() => {
  const send = form => {
    const data = new FormData(form);
    data.set("action", form.action);
    if (form.action) {
      fetch("/lp/bx24/", {
        method: "POST",
        body: data
			})
				.then(response => response.json())
        .then(response => {
          response = response['data']
          if (!response["error"]) {
            alert("Спасибо!\nФорма успешно отправлена!");
          } else {
            alert(response["text"]);
          }
          form.querySelector('input[type="submit"]').classList.remove("disabled");
        })
        .catch(err => {
          form.querySelector('input[type="submit"]').classList.remove("disabled");
          alert("Произошла ошибка!\nПопробуйте перезагрузить страницу и отправить форму заново.");
          console.log(err);
        });
    }
  };

  const check_recaptcha = form => {
    const data = new FormData(form);
    const gr_KEY = data.get("google-recaptcha");
    if (gr_KEY) {
      fetch("/google-recaptcha/", {
        method: "POST",
        mode: "no-cors",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": data.get("csrfmiddlewaretoken")
        },
        body: data
      })
        .then(response => {
          return response.json();
        })
        .then(response => {
          if (response["success"]) send(form);
          else {
            form.querySelector('input[type="submit"]').classList.remove("disabled");
            alert("Попробуйте перезагрузить страницу и отправить форму заново.");
          }
        })
        .catch(err => {
          alert("ОШИБКА!");
          console.log(err);
          form.querySelector('input[type="submit"]').classList.remove("disabled");
        });
    } else {
      alert("Хакер что-ли?");
    }
  };

  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", e => {
      e.preventDefault();
      form.querySelector('input[type="submit"]').classList.add("disabled");
      check_recaptcha(form);
    });
  });
})();
