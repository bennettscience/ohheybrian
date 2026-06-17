function insertImageAtCursor(el, value) {
  let active_editor = OverType.getInstance(el);
  if (
    active_editor.textarea.selectionStart ||
    active_editor.textarea.selectionStart == "0"
  ) {
    let startPos = active_editor.textarea.selectionStart;
    let endPos = active_editor.textarea.selectionEnd;

    // After saving the active_editor value, rewrite the entire active_editor,
    // adding the new string in at the end (or where the cursor was)
    // sent from the submit event
    // https://javascript.info/selection-range#selection-in-form-controls

    let selected = active_editor.textarea.value.slice(startPos, endPos);

    active_editor.insertAtCursor(`![${selected}](${value})`);
  } else {
    active_editor.insertatCursor(`![](${value})`);
  }
}

function insertTextAtCursor(el, value) {
  // `editor` is a global constant variable, so only
  // interact with the one passed by the inline item.
  let active_editor = OverType.getInstance(el);
  if (
    active_editor.textarea.selectionStart ||
    active_editor.textarea.selectionStart == "0"
  ) {
    let startPos = active_editor.textarea.selectionStart;
    let endPos = active_editor.textarea.selectionEnd;

    let selected = active_editor.textarea.value.slice(startPos, endPos);
    active_editor.insertAtCursor(`[${selected}](${value})`);
  } else {
    active_editor.insertAtCursor(value);
  }
}

function insertThumbnails(value) {
  let container = document.querySelector(`#thumbnails`);
  let results = paginate(value, 15);
  console.log(results);
  for (let i = 0; i < results[0].length; i++) {
    container.insertAdjacentHTML(
      "beforeend",
      `<li><img src="${results[0][i]}" loading="lazy" /></li>`,
    );
  }
}

function paginate(items, size) {
  return items.reduce((acc, val, i) => {
    let idx = Math.floor(i / size);
    let page = acc[idx] || (acc[idx] = []);
    page.push(val);

    return acc;
  }, []);
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
  insertImageAtCursor(evt.detail.textarea, evt.detail.value);
});

htmx.on("insertImageThumbs", (evt) => {
  insertThumbnails(evt.detail.thumbnails);
});

window.showToast = showToast;
window.insertTextAtCursor = insertTextAtCursor;
window.insertThumbnails = insertThumbnails;
