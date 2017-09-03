#!/usr/bin/env python3

import docker
import argparse
import sys
from datetime import datetime


def log(mensagem, e, logfile="docker-cli.log"):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    with open('docker-cli.log', 'a') as log:
        texto = "%s \t %s \t %s \n" % (data_atual, mensagem, str(e))
        log.write(texto)

def criar_container(args):
    try:
        client = docker.from_env()
        executando = client.containers.run(args.imagem, args.comando)
        print(executando)
        return executando
    except docker.errors.ImageNotFound as e:
        log("Erro: Essa imagem nao existe!", e)
    except docker.errors.NotFound as e:
        log("Erro: Comando nao existe", e)
    except Exception as e:
        log("Erro! Nao eh possilve realizar essa acao", e)
    finally:
        print ("Comando executado")

def listar_containers():
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)

        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            print ("O container %s utiliza a imagem %s rodando o comando %s" % (conectando.short_id, conectando.attrs['Config']['Image'], conectando.attrs['Config']['Cmd']))
    except Exception as e:
        log("Erro! Nao eh possilve realizar essa acao", e)

def procurar_container(imagem):
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            if (imagem == conectando.attrs['Config']['Image']):
                print ("Achei o container %s que contem a palavra %s no nome de sua imagem: %s" % (cada_container.short_id,imagem,cada_container.attrs['Config']['Image']))
    except Exception as e:
        print("Erro! Nao eh possilve realizar essa acao", e)


def remover_container():
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            portas = conectando.attrs['HostConfig']['PortBindings']
            if isinstance(portas,dict):
                for porta, porta1 in portas.items():
                    porta1 = str(porta1)
                    porta2 = ''.join(filter(str.isdigit, porta1))
                    if int(porta2) <= 1024:
                        print ("Removendo o container %s que esta escutando na porta %s e bindando no host na porta %s" % (cada_container.short_id, porta, porta2))
                        removendo = cada_container.remove(force=True)
    except Exception as e:
        log("Erro! Nao eh possilve realizar essa acao", e)



'''parser = argparse.ArgumentParser(description="docker-cli criado na aula de python")
subparser = parser.add_subparsers()
criar_opt = subparser.add_parser('criar')
criar_opt.add_argument('--imagem', required=True)
criar_opt.add_argument('--comando', required=True)
criar_opt.set_defaults(func=criar_container)
cmd = parser.parse_args()
cmd.func(cmd)'''

#listar_containers()
#criar_container("alpine", "echo VAIIII")
procurar_container("nginx")
#remover_container()
