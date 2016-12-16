function clearPageBreaks() {
    for (var e = document.querySelectorAll("pb"), t = 0; t < e.length; t++) e[t].style.display = "none";
    for (var e = document.querySelectorAll(".-teibp-pb"), t = 0; t < e.length; t++) e[t].style.display = "none"
}

function addPageBreaks() {
    for (var e = document.querySelectorAll("pb"), t = 0; t < e.length; t++) e[t].style.display = "inline";
    for (var e = document.querySelectorAll(".-teibp-pb"), t = 0; t < e.length; t++) e[t].style.display = "inline"
}

function init() {
    var e = document.getElementById("pbToggle");
    null != e && (e.onclick = function() {
        this.checked ? clearPageBreaks() : addPageBreaks()
    }, addPageBreaks(), document.getElementById("pbToggle").checked = !1);
    var t = document.querySelector("html > head > title"),
        n = document.querySelector("tei-title");
    null != t && null != n && (t.textContent = n.textContent)
    
    // Bind and action to the appChoice radio buttons
    var sources = document.querySelectorAll('input[type=radio][name="appChoice"]');   
    Array.prototype.forEach.call(sources, function(radio) {
       radio.addEventListener('change', changeHandler);
    });
}

function changeHandler(event) {
    if ( this.value === 'lem' ) {
        // hide all the rdg
        for (var e = document.querySelectorAll("rdg"), t = 0; t < e.length; t++) e[t].style.display = "none";
        // show the lem
        for (var e = document.querySelectorAll("lem"), t = 0; t < e.length; t++) e[t].style.display = "inline";
    }
    else {
        // hide all the app children (lem and rdg)
        for (var e = document.querySelectorAll("app > *"), t = 0; t < e.length; t++) e[t].style.display = "none";
        // show the matching rdg
        for (var e = document.querySelectorAll("rdg[wit*=\\" + this.value + "]"), t = 0; t < e.length; t++) e[t].style.display = "inline";
    }
}

function blockUI() {
    var e = document.querySelector("body"),
        t = document.createElement("div");
    t.setAttribute("class", "blocker"), e.appendChild(t)
}

function unblockUI() {
    var e = document.querySelector(".blocker");
    e && e.parentNode.removeChild(e)
}

function switchThemes(e) {
    document.getElementById("maincss").href = e.options[e.selectedIndex].value
}

function showFacs(e, t, n) {
    for (var o = "", c = document.querySelectorAll(".-teibp-thumbnail"), r = 0; r < c.length; r++) o += "<img id='" + c[r].parentNode.parentNode.parentNode.getAttribute("id") + "' src='" + c[r].getAttribute("src") + "' alt='facsimile page image'/>";
    var l = ["<html>", "<head>", "<title></title>", document.querySelector("#maincss").outerHTML, document.querySelector("#customcss").outerHTML, null != document.querySelector("#teibp-tagusage-css") ? document.querySelector("#teibp-tagusage-css").outerHTML : "", null != document.querySelector("#teibp-rendition-css") ? document.querySelector("#teibp-rendition-css").outerHTML : "", "<script src='../js/teibp.js'></script>", "</head>", "<body>", "<script>blockUI();</script>", document.querySelector("teiHeader").outerHTML, "<div id='resizable'>", "<div class='facsImage'>", o, "</div>", "</div>", document.querySelector("footer").outerHTML, "<script>", "document.getElementById('" + n + "').scrollIntoView();", "unblockUI();", "</script>", "</body>", "</html>"].join("\n");
    facsWindow = window.open("about:blank"), facsWindow.document.write(l), facsWindow.document.close()
}
document.addEventListener ? (document.addEventListener("DOMContentLoaded", init, !1), window.addEventListener("load", init, !1)) : document.attachEvent && (document.attachEvent("onreadystatechange", init), window.attachEvent("onload", init));
