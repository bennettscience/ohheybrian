function insertAtCursor(el, value) {
  let field = document.querySelector(el);
  if (field.selectionStart || field.selectionStart == "0") {
    let startPos = field.selectionStart;
    let endPos = field.selectionEnd;

    // After saving the field value, rewrite the entire field,
    // adding the new string in at the end (or where the cursor was)
    // sent from the submit event
    field.value =
      field.value.substring(0, startPos) +
      "\n\n" +
      value +
      "\n\n" +
      field.value.substring(endPos, field.value.length);
  } else {
    field.value += value;
  }
}

function showToast(msg = "Loading...", timeout = 5000, err = false) {
  const toast = document.querySelector(`#toast`);
  // Handle message objects from hyperscript
  // For non-template returns, the backend will also return JSON with
  // the `message` key with details for the user.
  if (typeof msg === "object") {
    // HTMX returns strings, so convert it to an object
    let obj = JSON.parse(msg.xhr.responseText);
    msg = obj.message;
  }

  toast.children[0].innerText = msg;
  if (err) {
    toast.classList.add("error");
  }
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
    toast.children[0].innerText = "Loading...";
    if (err) {
      toast.classList.remove("error");
    }
  }, timeout);
}

htmx.on("showToast", (evt) => {
  showToast(evt.detail.value);
});

htmx.on("insertImgSrc", (evt) => {
  console.log(evt.detail);
  let formattedString = `![](${evt.detail.value})`;
  insertAtCursor(evt.detail.textarea, formattedString);
});

window.showToast = showToast;
window.insertAtCursor = insertAtCursor;
