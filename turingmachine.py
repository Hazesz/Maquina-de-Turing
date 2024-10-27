import json
import sys

def ler_json(file_path):
    """Lê o arquivo JSON que define a Máquina de Turing."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Erro: Não foi possível decodificar o arquivo {file_path}. Verifique o formato JSON.")
        sys.exit(1)

def ler_entrada(input_file):
    """Lê a fita de entrada de um arquivo de texto."""
    try:
        with open(input_file, "r") as f:
            return f.readline().strip()  # Lê apenas a primeira linha
    except FileNotFoundError:
        print(f"Erro: Arquivo {input_file} não encontrado.")
        sys.exit(1)
    except IOError:
        print(f"Erro: Problema ao ler o arquivo {input_file}.")
        sys.exit(1)

def salvar_saida(output_file, fita):
    """Salva o conteúdo final da fita em um arquivo de saída."""
    try:
        with open(output_file, 'w') as f:
            f.write("".join(fita))
    except IOError:
        print(f"Erro: Problema ao salvar no arquivo {output_file}.")
        sys.exit(1)

def buscar_transicao(transicoes, estado_atual, simbolo_atual):
    """Busca a transição apropriada para o estado e símbolo atuais."""
    return transicoes.get((estado_atual, simbolo_atual), None)

def simular_maquina(turing_machine, entrada):
    """Simula a execução da Máquina de Turing para uma fita de entrada."""
    estado_atual = turing_machine['initial']
    estados_finais = turing_machine['final']
    simbolo_branco = turing_machine['white']
    transicoes = {(t['from'], t['read']): (t['to'], t['write'], t['dir']) for t in turing_machine['transitions']}

    fita = list(entrada) if entrada else [simbolo_branco]
    index = 0

    while estado_atual not in estados_finais:
        simbolo_atual = fita[index] if index < len(fita) else simbolo_branco
        transicao = buscar_transicao(transicoes, estado_atual, simbolo_atual)

        if not transicao:  # Se não houver transição válida, parar
            break

        estado_atual, simbolo_escrever, direcao = transicao
        fita[index] = simbolo_escrever

        if direcao == 'R':
            index += 1
            if index >= len(fita):
                fita.append(simbolo_branco)
        elif direcao == 'L':
            index -= 1
            if index < 0:
                fita.insert(0, simbolo_branco)
                index = 0

    return fita, estado_atual in estados_finais

def main():
    """Função principal que coordena a execução da simulação."""
    instrucoes_arquivo = "duplo_bal.json"  # Nome do arquivo da máquina de Turing
    entrada_arquivo = "duplobal.txt"  # Nome do arquivo de entrada
    saida_arquivo = "saida.txt"  # Nome do arquivo de saída

    turing_machine = ler_json(instrucoes_arquivo)
    entrada = ler_entrada(entrada_arquivo)
    
    fita_final, aceito = simular_maquina(turing_machine, entrada)
    salvar_saida(saida_arquivo, fita_final)

    # Exibindo a entrada, saída e se foi aceito ou rejeitado
    print(f"Entrada: {entrada}")
    print(f"Saída: {''.join(fita_final)}")
    if aceito:
        print("Resultado: Aceito")
    else:
        print("Resultado: Rejeitado")

if __name__ == "__main__":
    main()
