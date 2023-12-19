let url = window.location.host
let get_full_url = window.location.href
function getSocketScheme() { return window.location.protocol == "http:" ? "ws:" : "wss:"; }

let scheme = getSocketScheme()
