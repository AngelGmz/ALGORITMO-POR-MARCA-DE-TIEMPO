class proceso{
    id = 1,2,3,4,5,6
    colaDePeticion1 = []
    colaDePeticion2 = []
    lista_de_ok = [] //igual al número de procesos
    marcaDeTeimpo = 0
    estado = sin_acción // quiere_entrar || sin_acción || en_region_critica

    Proceso_requiere_entrar_a_zona_crítica(){
        p.estado = quiere_entrar
        msg = {
                id_región: '',
                identificador_proceso: p.id, 
                marca_tiempo: p.hora
            }
        Proceso_evía_mensaja_todos_y_a_el_mismo(msg)
        this.estado = en_espera
    }

    recibe_ok(msg){
        lista_de_ok[msg.id -1] = 1
        if ( todos_okeys_en_1() ) {
            entra_a_región_crítica()
            this.estado = region_critica
        }
    }

    salir_de_región_crítica(){
        this.estado = sin_acción
        this.colaDePeticion.forEach(peticion){
            evía_mensaje_ok(msg.identificador_proceso)
            this.colaDePeticion.filter((i) => peticion != i)   
        }
    }


    recibir_mensaje_de_petición(msg){
        if (p.estado == sin_acción){
            evía_mensaje_ok(msg.identificador_proceso)
        }
        if(p.estado == region_critica){
            colaDePeticion.append(msg)
        }
        if(p.estado == quiere_entrar){
            if(p.marcaDeTeimpo < msg.marca_tiempo){
                colaDePeticion.append(msg)
            }else{
                evía_mensaje_ok(msg.identificador_proceso)
            }
        }
    }    

}