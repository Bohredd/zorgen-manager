from django.utils.safestring import mark_safe


def js_ocultar_exibir(configuracoes: dict[str, dict[str, list[str]]], usar_jquery=True):
    """
    constrói um código javascript que permite ocultar e exibir elementos dinamicamente

    configuracoes: dict[str, dict[str, list[str]]] - dicionário de configurações
    a chave deve ser o id do campo, o valor deve ser um dicionário de possíveis valores
    o valor para cada possível valor deve ser uma lista de ids de elementos para exibir
    os valores possíveis para checkbox e switch são 'on' e 'off', para radio são 'on' e ''
    # importante!!!
        quando precisar ocultar ou exibir um elemento dentro de outro que já
        está configurado altere a ordem das chaves das configurações, deixando
        os elementos mais internos por último

    plus:
    se for necessário usar com radio, basta colocar como chave o id de cada radio
    nas configs coloque "on" e os elementos a exibir, coloque "" e os elementos a ocultar
    pois não é disparado evento quando o radio altera pra falso

    este código deve ser incluído diretamente no componente de mais alto nível onde todos
    os demais a serem manipulados estejam contidos
    """

    inicializador = (
        "document.addEventListener('DOMContentLoaded',"
        if not usar_jquery
        else "jQuery("
    )

    # language=html
    return mark_safe(
        f"""
    <script>
    try{{
        const {{parentNode}} = document.currentScript

        {inicializador}()=>{{

            function get_valor_do_campo(idDoCampo){{
                const campo = parentNode.querySelector(`#${{idDoCampo}}`)
                if(['checkbox','switch','radio'].includes(campo.type)){{
                    if(campo.checked){{
                        return 'on'
                    }}else{{
                        return 'off'
                    }}
                }}
                return campo.value
            }}

            const configsDosCampos = {configuracoes}

            function get_parent_node_inputs(node){{                
                const inputs = node.querySelectorAll('input')
                const selects = node.querySelectorAll('select')
                return [...inputs,...selects]
            }}

            function remover_required_de_elementos_e_esconder(parentNodeId){{  
                const node = parentNode.querySelector(`#${{parentNodeId}}`)                  
                const elementos = get_parent_node_inputs(node)
                elementos.forEach(elemento=>{{
                    if(elemento.hasAttribute('required')){{                        
                        elemento.removeAttribute('required')
                        elemento.setAttribute('old_required',true)
                    }}
                }})
                node.style.display = 'none'
            }}

            function repor_required_de_elementos_e_exibir(parentNodeId){{  
                const node = parentNode.querySelector(`#${{parentNodeId}}`)   
                const elementos = get_parent_node_inputs(node)               
                elementos.forEach(elemento=>{{
                    if(elemento.hasAttribute('old_required')){{
                        elemento.setAttribute('required','true')
                    }}
                }})
                node.style.display = ''
            }}

            function definir_elementos_visiveis(){{
                Object.entries(configsDosCampos).forEach(([idDoCampo,configsDoCampo])=>{{                                       
                    try{{            
                        const valorDoCampo = get_valor_do_campo(idDoCampo)
                        /** primeiro esconde todos e depois exibe somente os necessários */
                        Object.values(configsDoCampo).forEach(ids=>ids.forEach(id=>{{
                            remover_required_de_elementos_e_esconder(id)
                        }}))
                        Object.entries(configsDoCampo).forEach(([valor,ids])=>{{
                            if(valorDoCampo == valor){{
                                ids.forEach(id=>repor_required_de_elementos_e_exibir(id))
                            }}
                        }})
                    }}catch(erro_ao_definir_elemento_visivel){{
                        console.log({{[idDoCampo]:erro_ao_definir_elemento_visivel}})
                    }}
                }})
            }}

            function adicionar_listeners(){{
                Object.keys(configsDosCampos).forEach((idCampo)=>{{
                    try{{                            
                        parentNode.querySelector(`#${{idCampo}}`).addEventListener(
                            'change',
                            definir_elementos_visiveis,
                        )                                   
                    }}catch(erro_ao_adicionar_listener){{
                        console.log({{[idCampo]:erro_ao_adicionar_listener}})
                    }}
                }})
            }}

            adicionar_listeners()
            definir_elementos_visiveis()
        }})
    }}catch(_){{}}
    </script>
    """
    )


def js_consultar_cep(
    id_cep,
    *,
    id_logradouro="",
    id_estado="",
    id_ibge="",
    id_bairro="",
    id_cidade="",
    id_ddd="",
    id_latitude="",
    id_longitude="",
):
    """
    script auxiliar para consulta de ceps
    pesquisa em 3 apis diferentes no momento
    para funcionar basta preencher os argumentos os mesmos são auto explicativos
    """
    ids_campos = [
        id_logradouro,
        id_estado,
        id_ibge,
        id_cidade,
        id_ddd,
        id_latitude,
        id_longitude,
        id_bairro,
    ]

    for arg in ids_campos:
        assert type(arg) == str, "todos os argumentos da função devem ser strings"

    fontes = """
    // URLs das APIs a serem consultadas, a primeira é a mais completa
    const fontes = [
        {url:`https://cep.awesomeapi.com.br/json/${cep}`,config:configs_awesomeapi},
        {url:`https://viacep.com.br/ws/${cep}/json/`,config:configs_viacep},
        {url:`https://ws.apicep.com/cep/${cep}.json`,config:configs_apicep},
    ]
    """

    # language=javascript
    configs = f"""
    const configs_awesomeapi = {{
        "address": '{id_logradouro}',
        "city": '{id_cidade}',
        "state": '{id_estado}',
        "city_ibge": '{id_ibge}',
        "ddd": '{id_ddd}',
        "district": '{id_bairro}',
        "lng": '{id_longitude}',
        "lat": '{id_latitude}',
    }};
    const configs_apicep = {{
        "address": '{id_logradouro}',
        "city": '{id_cidade}',
        "state": '{id_estado}',                
        "district": '{id_bairro}',
    }};
    const configs_viacep = {{
        "logradouro": '{id_logradouro}',
        "localidade": '{id_cidade}',
        "uf": '{id_estado}',
        "ibge": '{id_ibge}',
        "ddd": '{id_ddd}',
        "bairro": '{id_bairro}',
    }};
    """

    # language=javascript
    consultar_cep = f"""
    async function consultarCep(cep) {{

        console.log('pesquisando cep')

        {fontes}

        // Executa as requisições HTTP em paralelo até que uma delas retorne um resultado válido
        for (let fonte of fontes) {{
            try {{
                const response = await fetch(fonte.url);
                const data = await response.json();
                if(response.ok && ('cep' in data || 'code' in data)){{
                    return preencher_campos(data,fonte.config);
                }}
            }} catch (error) {{
                // Ignora erros e tenta a próxima API
                console.error(error);
            }}
        }};

        alert("CEP não encontrado.");
        preencher_campos({{'erro':''}})

        // Caso nenhuma das APIs tenha retornado um resultado válido, lança um erro
        throw new Error("Não foi possível obter as informações do CEP.");
    }}
    """

    # language=javascript
    preencher_campos = """
    function preencher_campos(dados,config){

        // limpa os campos antes de inserir os dados novos
        limpar_campos()

        console.log('preenchendo campos')

        if (!("erro" in dados)) {
            //Atualiza os campos com os valores.

            Object.entries(dados).forEach(([chave,valor])=>{
                const idCampoAlvo = config[chave]
                if (idCampoAlvo){
                    try{
                        document.getElementById(idCampoAlvo).value = valor
                    }catch(erro_ao_preencher_campo){
                        console.log(`Erro ao preencher campo ${chave}: `,erro_ao_preencher_campo)
                    }
                }else{
                    console.log(`pulado campo ${chave}`)
                }
            })

        } else {
            //CEP não Encontrado.
            limpar_campos()
        }
    }
    """

    # language=javascript
    limpar_campos = """
    function limpar_campos(){
        console.log('limpando campos')
        ids_campos.forEach(id_campo=>{
            try{
                document.getElementById(id_campo).value = ''                            
            }catch(_){

            }
        }) 
    }
    """

    # language=javascript
    onblur = f"""
    function onBlurCep (e) {{

        {limpar_campos}

        const ids_campos = {ids_campos}

        {preencher_campos}

        {configs}

        {consultar_cep}

        let cep = e.target.value;

        const validacep = /^[0-9]{8}$/;

        if (cep != "") {{
            cep = cep.replace(/\D/g, "");
            if (cep.length===8) {{
                //Preenche os campos com "..." enquanto consulta webservice.
                ids_campos.forEach(id_campo=>{{
                    try{{
                        document.getElementById(id_campo).value = '...'
                    }}catch(_){{}}
                }})

                consultarCep(cep);

            }} else {{
                limpar_campos()                    
                alert("Formato de CEP inválido!");
            }}
        }}
    }};
    """

    return mark_safe(
        # language=html
        f"""
    <script>
    document.addEventListener('DOMContentLoaded',()=>{{
        {onblur}
        const input = document.getElementById('{id_cep}')
        if(!input){{
            console.log('Não foi possível adicionar evento no campo cep')
        }}else{{     
            console.log({{input}})       
            input.addEventListener('blur',onBlurCep)
        }}
    }})
    </script>
    """
    )
