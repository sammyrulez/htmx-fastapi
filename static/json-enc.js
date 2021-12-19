htmx.defineExtension('json-enc', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['Content-Type'] = "application/json";
        }
    },

    encodeParameters: function (xhr, parameters, elt) {
        xhr.overrideMimeType('text/json');
        struct_params = {}
        for (var prop in parameters) {
            if (prop.endsWith("_list")) {
                splits = prop.split('_')
                fieldName = splits[0]
                cmpFieldName = splits[1]
                if (!struct_params[fieldName]) {
                    struct_params[fieldName] = []
                }
                if (Array.isArray(parameters[prop])) {
                    for (let i = 0; i < parameters[prop].length; i++) {
                        if (struct_params[fieldName].length <= i) {
                            struct_params[fieldName][i] = {}
                        }
                        struct_params[fieldName][i][cmpFieldName] = parameters[prop][i]
                    }
                }
                else {
                    if (struct_params[fieldName].length == 0) {
                        struct_params[fieldName][0] = {}
                    }
                    struct_params[fieldName][0][cmpFieldName] = parameters[prop]
                }


            } else {
                struct_params[prop] = parameters[prop]
            }
        }
        out = JSON.stringify(struct_params)
        console.log("struct params ", out)
        return out;
    }
});