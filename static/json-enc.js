htmx.defineExtension('json-enc', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['Content-Type'] = "application/json";
        }
    },
    
    encodeParameters : function(xhr, parameters, elt) {
        xhr.overrideMimeType('text/json');
        console.log(parameters)
        struct_params = {}
        for (var prop in parameters) { 
            console.log(prop, parameters[prop] )
            if(prop.endsWith("_list")){
                console.log(prop, "is a list element")
                splits = prop.split('_')
                fieldName = splits[0]
                cmpFieldName = splits[1]
                if(!struct_params[fieldName]){
                    struct_params[fieldName] = []
                }
                if(Array.isArray(parameters[prop])){
                    for(let i = 0; i <parameters[prop].length; i++ ){
                        if(struct_params[fieldName].length <= i ){
                            struct_params[fieldName][i] = {} 
                        }
                        struct_params[fieldName][i][cmpFieldName] = parameters[prop][i]
                    }
                }
                else{
                    if(struct_params[fieldName].length == 0){
                        struct_params[fieldName][0] = {}
                    }
                    struct_params[fieldName][0][cmpFieldName] = parameters[prop]
                }
         
                
            }else{
                struct_params[prop] = parameters[prop] 
            }
        }
        console.log("struct params ",JSON.stringify(struct_params))
        return (JSON.stringify(parameters));
    }
});