// Copyright (c) 2026 Martin.Bechard@DevConsult.ca
// AI attribution: Generated with AI assistance.
// Provides the accessible dialog and form-control demonstrations on the interaction page.

(() => {
  "use strict";

  const triggers = Array.from(document.querySelectorAll("[data-dialog-open]"));
  const dialog = document.querySelector("[data-dialog]");
  const close = document.querySelector("[data-dialog-close]");
  const preference = document.querySelector("[data-preference]");
  const preferenceStatus = document.querySelector("[data-preference-status]");
  const demoForm = document.querySelector("[data-demo-form]");
  const email = document.querySelector("[data-email]");
  const emailError = document.querySelector("[data-email-error]");
  const formStatus = document.querySelector("[data-form-status]");
  let activeTrigger = null;

  function closeDialog() {
    if (!dialog || dialog.hidden) return;
    dialog.hidden = true;
    document.body.classList.remove("dialog-open");
    triggers.forEach((trigger) => trigger.setAttribute("aria-expanded", "false"));
    if (activeTrigger) activeTrigger.focus();
  }

  function openDialog(event) {
    activeTrigger = event.currentTarget;
    dialog.hidden = false;
    document.body.classList.add("dialog-open");
    activeTrigger.setAttribute("aria-expanded", "true");
    dialog.querySelector("select, button").focus();
  }

  if (triggers.length && dialog && close) {
    triggers.forEach((trigger) => trigger.addEventListener("click", openDialog));
    close.addEventListener("click", closeDialog);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) closeDialog();
    });
    dialog.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeDialog();
    });
  }

  if (preference && preferenceStatus) {
    preference.addEventListener("change", () => {
      preferenceStatus.textContent = preference.checked
        ? "Weekly summary enabled"
        : "Weekly summary disabled";
    });
  }

  if (demoForm && email && emailError && formStatus) {
    demoForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const valid = email.validity.valid;
      emailError.hidden = valid;
      formStatus.hidden = !valid;
      if (valid) {
        formStatus.focus();
      } else {
        email.focus();
      }
    });
  }
})();
