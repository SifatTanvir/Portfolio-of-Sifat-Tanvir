/**
 * Static-site contact: POSTs to FormSubmit (no PHP). Falls back to mailto if the request fails.
 */
(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var endpoint = form.getAttribute("data-formsubmit-endpoint");
  if (!endpoint) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    var loading = form.querySelector(".loading");
    var errEl = form.querySelector(".error-message");
    var sentEl = form.querySelector(".sent-message");

    var name = (form.querySelector('[name="name"]') || {}).value || "";
    var email = (form.querySelector('[name="email"]') || {}).value || "";
    var subject = (form.querySelector('[name="subject"]') || {}).value || "";
    var message = (form.querySelector('[name="message"]') || {}).value || "";

    if (loading) loading.classList.add("d-block");
    if (errEl) {
      errEl.classList.remove("d-block");
      errEl.innerHTML = "";
    }
    if (sentEl) sentEl.classList.remove("d-block");

    function showError(msg) {
      if (loading) loading.classList.remove("d-block");
      if (errEl) {
        errEl.innerHTML = msg;
        errEl.classList.add("d-block");
      }
    }

    function showSent() {
      if (loading) loading.classList.remove("d-block");
      if (sentEl) sentEl.classList.add("d-block");
      form.reset();
    }

    fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        subject: subject,
        message: message,
        _replyto: email,
        _captcha: false,
      }),
    })
      .then(function (res) {
        return res.text().then(function (text) {
          var data = {};
          try {
            data = text ? JSON.parse(text) : {};
          } catch (e) {}
          return { ok: res.ok, status: res.status, data: data };
        });
      })
      .then(function (result) {
        var d = result.data || {};
        var accepted =
          result.ok &&
          (d.success === true ||
            d.success === "true" ||
            d.ok === true ||
            d.status === "success");

        if (accepted) {
          if (sentEl) {
            sentEl.textContent = "Your message has been sent. Thank you!";
          }
          showSent();
          return;
        }

        var msg =
          d.message ||
          d.error ||
          (result.status === 422
            ? "Confirm the FormSubmit email in your inbox (first time only), then try again."
            : "Could not send from this browser.");
        showError(msg + " Opening your email app instead…");
        setTimeout(function () {
          mailtoFallback();
        }, 500);
      })
      .catch(function () {
        showError("Network error. Opening your email app instead…");
        setTimeout(function () {
          mailtoFallback();
        }, 500);
      });
  });

  function mailtoFallback() {
    var name = (form.querySelector('[name="name"]') || {}).value || "";
    var email = (form.querySelector('[name="email"]') || {}).value || "";
    var subject = (form.querySelector('[name="subject"]') || {}).value || "";
    var message = (form.querySelector('[name="message"]') || {}).value || "";
    var loading = form.querySelector(".loading");
    var errEl = form.querySelector(".error-message");
    var sentEl = form.querySelector(".sent-message");

    if (loading) loading.classList.remove("d-block");
    if (errEl) errEl.classList.remove("d-block");

    var body =
      "Name: " + name + "\nEmail: " + email + "\n\n" + message;
    var href =
      "mailto:sifattanvirsam@gmail.com?subject=" +
      encodeURIComponent(subject || "Portfolio contact") +
      "&body=" +
      encodeURIComponent(body);
    window.location.href = href;

    if (sentEl) {
      sentEl.textContent =
        "If your email app did not open, send mail to sifattanvirsam@gmail.com.";
      sentEl.classList.add("d-block");
    }
    form.reset();
  }
})();
