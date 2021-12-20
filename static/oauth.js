htmx.defineExtension('oauth', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            token = window.localStorage.getItem('sect_token')
            if (token) {
                evt.detail.headers['Authorization'] = "Bearer " + token;
            }
        }
        if (name === "htmx:afterRequest") {
            token = evt.detail.xhr.getResponseHeader('Authorization-Token')
            if(token){
                window.localStorage.setItem('sect_token',token)
            }
           
        }
    },
});