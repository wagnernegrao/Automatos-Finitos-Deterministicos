import re, sys

def leArquivo():
	arquivo = open(sys.argv[1], "r")
	automato = []
	##-----Adiciona cada linha na lista-----
	for linha in arquivo:
		automato.append(linha)
	##--------------------------------------
	arquivo.close()
	return automato

def limpaPrimeiraLinha(automato):
	primeira_linha = automato[0]
	regex = re.compile(r'\{[^\}]*\}')
	dados = re.findall(regex, primeira_linha)
	result = []
	for elemento in dados:
		result.append(elemento.strip("{}").replace(" ", "").split(","))
	return result

def buscaEstadoInicial(automato):
	primeira_linha = automato[0]
	regex = re.compile(r"Z|,\sq\w*,\s{")
	dado = re.findall(regex, primeira_linha)
	estado_inicial = [elemento.strip(",{ ") for elemento in dado]
	return estado_inicial

def leRegrasDeTransicao(automato):
	regras = []
	for i in range(1, len(automato)):
		automato[i] = automato[i].strip("\n").replace(" ", "").split(",")
		regras.append(automato[i])
	return regras

def leituraDaPalavra(estado_inicial, estados_finais, regras):
	palavra = sys.argv[2]
	estado_atual = estado_inicial[0]

	i = 0
	for letra in palavra:
		validacao = False

		for regra in regras:
			regra_estado_entrada, regra_letra, regra_estado_saida = regra
			if (regra_estado_entrada == estado_atual) and (
			    regra_letra == letra):
				print("(" + estado_atual + ", " + palavra[i:] + ") = " +
				      regra_estado_saida)
				estado_atual = regra_estado_saida
				validacao = True
				break
		i += 1

		if not validacao:
			return False
	if estado_atual in estados_finais:
		return True
	else:
		return False

def automatoValido(alfabeto, estados, estados_finais, regras):
	if len(estados[0]) == 0:
		print("\nO conjunto de estados deve ser >= 1\nAPRESENTE UM " +
		      "ARQUIVO VÁLIDO	")
		return False
	for estado in estados_finais:
		if estado not in estados:
			print("\nEstado Final " + estado +
			      "\nnão está no conjunto de estados possíveis do automato " +
			      str(estados) + "\nAPRESENTE UM ARQUIVO VÁLIDO")
			return False

	for regra in regras:
		regra_estado_entrada, regra_letra, regra_estado_saida = regra
		if regra_estado_entrada not in estados:
			print(
			    "\nEstado " + regra_estado_entrada + " da regra " + str(regra)
			    + "\nnão está no conjunto de estados possíveis do automato " +
			    str(estados) + "\nAPRESENTE UM ARQUIVO VÁLIDO")
			return False
		if regra_estado_saida not in estados:
			print("\nEstado " + regra_estado_saida + " da regra " + str(regra)
			      + "\nnão está no conjunto de estados possíveis do automato "
			      + str(estados) + "\nAPRESENTE UM ARQUIVO VÁLIDO")
			return False
		if regra_letra not in alfabeto:
			print("\nSímbolo " + regra_letra + " da regra " + str(regra) +
			      "\nnão está no conjunto de símbolos possíveis do automato " +
			      str(alfabeto) + "\nAPRESENTE UM ARQUIVO VÁLIDO")
			return False
	return True

def main():
	##-------Le arquivo-----------------------------------
	automato = leArquivo()
	##-------Pega dos dados da primeira linha da lista----
	dados = limpaPrimeiraLinha(automato)
	##-------Busca estado inicial-------------------------
	estado_inicial = buscaEstadoInicial(automato)
	##-------Le as regras para transicao------------------
	regras = leRegrasDeTransicao(automato)
	##-------Atribui os devidos elementos-----------------
	alfabeto = dados[0]
	estados = dados[1]
	estados_finais = dados[2]
	##-------Printa as informações------------------------
	print("\n-> Alfabeto: {}".format(alfabeto))
	print("-> Estados: {}".format(estados))
	print("-> Estado Inicial: {}".format(estado_inicial))
	print("-> Estado Final: {}".format(estados_finais))
	print("-> Regras de Transição: ")
	for regra in regras:
		print(regra)
	print()
	##-------Testa se a palavra e valida ou nao-----------
	if automatoValido(alfabeto, estados, estados_finais, regras):
		print("Processamento: ")
		validade = leituraDaPalavra(estado_inicial, estados_finais, regras)
		if validade == True:
			return ("\nPalavra Valida")
		else:
			return ("\nPalavra Invalida")
	else:
		return ""

if len(sys.argv) != 3:
	print("Requer um arquivo txt e uma palavra para processar")
	print("Tente: python3 main.py <arquivo-txt> <palavra>")
else:
	print(main())
