import json
import math
from datetime import datetime
from pathlib import Path

ARQUIVO_JSON = Path(__file__).resolve().parent / "coletas.json"
MATERIAIS = ["plástico", "papel", "vidro", "metal"]
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
         "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


# ARQUIVO JSON
def carregar_coletas():
    if not ARQUIVO_JSON.exists():
        return []
    try:
        with ARQUIVO_JSON.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        raise RuntimeError(f"Erro ao ler {ARQUIVO_JSON.name}: {erro}") from erro

    if not isinstance(dados, list):
        raise RuntimeError("O arquivo JSON não contém uma lista de coletas.")

    coletas, codigos = [], set()
    for numero, item in enumerate(dados, 1):
        try:
            codigo = item["codigo"]
            data = normalizar_data(item["data"])
            material = normalizar_material(item["material"])
            peso = float(item["peso_kg"])
        except (KeyError, TypeError, ValueError) as erro:
            raise RuntimeError(f"Registro {numero} inválido no arquivo JSON.") from erro

        if (type(codigo) is not int or codigo <= 0 or codigo in codigos
                or data is None or material is None or not math.isfinite(peso) or peso <= 0):
            raise RuntimeError(f"Registro {numero} contém dados inválidos ou código repetido.")
        coletas.append({"codigo": codigo, "data": data,
                        "material": material, "peso_kg": peso})
        codigos.add(codigo)
    return coletas


def salvar_coletas(coletas):
    temporario = ARQUIVO_JSON.with_suffix(".tmp")
    try:
        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(coletas, arquivo, indent=4, ensure_ascii=False, allow_nan=False)
        temporario.replace(ARQUIVO_JSON)
        return True
    except (OSError, TypeError, ValueError) as erro:
        print(f"Erro ao salvar: {erro}")
        try:
            temporario.unlink(missing_ok=True)
        except OSError:
            pass
        return False


# VALIDAÇÃO DAS ENTRADAS
def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit() and int(valor) > 0:
            return int(valor)
        print("Digite um número inteiro maior que zero.")


def ler_peso(mensagem):
    while True:
        try:
            peso = float(input(mensagem).strip().replace(",", "."))
            if math.isfinite(peso) and peso > 0:
                return peso
        except ValueError:
            pass
        print("Digite um peso válido e maior que zero. Exemplo: 8,5")


def normalizar_data(texto):
    try:
        data = datetime.strptime(str(texto).strip(), "%d/%m/%Y")
        return data.strftime("%d/%m/%Y") if 2000 <= data.year <= 2100 else None
    except ValueError:
        return None


def ler_data(mensagem):
    while True:
        data = normalizar_data(input(mensagem))
        if data:
            return data
        print("Data inválida. Use uma data real no formato DD/MM/AAAA.")


def normalizar_material(material):
    if not isinstance(material, str):
        return None
    material = material.strip().lower()
    if material == "plastico":
        material = "plástico"
    return material if material in MATERIAIS else None


def ler_material():
    while True:
        material = normalizar_material(input(f"Material ({', '.join(MATERIAIS)}): "))
        if material:
            return material
        print("Material inválido.")


def codigo_existe(coletas, codigo):
    return any(registro["codigo"] == codigo for registro in coletas)


def novo_codigo(coletas):
    while True:
        codigo = ler_inteiro("Código da coleta: ")
        if not codigo_existe(coletas, codigo):
            return codigo
        print("Esse código já está cadastrado.")


# CADASTRO E CONSULTA
def cadastrar_coleta(coletas):
    print("\n--- NOVA COLETA ---")
    registro = {
        "codigo": novo_codigo(coletas),
        "data": ler_data("Data (DD/MM/AAAA): "),
        "material": ler_material(),
        "peso_kg": ler_peso("Peso em kg: ")
    }
    coletas.append(registro)
    if salvar_coletas(coletas):
        print("Coleta cadastrada!")
    else:
        coletas.pop()


def listar_coletas(coletas):
    print("\n--- COLETAS ---")
    if not coletas:
        print("Nenhuma coleta registrada.")
        return
    for r in coletas:
        print(f"Código: {r['codigo']} | Data: {r['data']} | "
              f"Material: {r['material'].capitalize()} | Peso: {r['peso_kg']:.2f} kg")


# ESTATÍSTICAS E RECURSÃO
def somar_pesos_recursivo(coletas, inicio=0, fim=None):
    if fim is None:
        fim = len(coletas)
    if inicio >= fim:
        return 0.0
    if fim - inicio == 1:
        return coletas[inicio]["peso_kg"]
    meio = (inicio + fim) // 2
    return (somar_pesos_recursivo(coletas, inicio, meio)
            + somar_pesos_recursivo(coletas, meio, fim))


def calcular_estatisticas(coletas):
    if not coletas:
        print("\nNão há coletas para analisar.")
        return
    total, maior, menor = 0.0, coletas[0], coletas[0]
    for r in coletas:
        total += r["peso_kg"]
        if r["peso_kg"] > maior["peso_kg"]:
            maior = r
        if r["peso_kg"] < menor["peso_kg"]:
            menor = r
    print(f"\nQuantidade: {len(coletas)} coletas")
    print(f"Peso total: {somar_pesos_recursivo(coletas):.2f} kg")
    print(f"Peso médio: {total / len(coletas):.2f} kg")
    print(f"Maior coleta: código {maior['codigo']} - {maior['peso_kg']:.2f} kg")
    print(f"Menor coleta: código {menor['codigo']} - {menor['peso_kg']:.2f} kg")
    print("Meta de 100 kg atingida! Chame a coleta externa." if total >= 100
          else f"Faltam {100 - total:.2f} kg para atingir 100 kg.")


# ORDENAÇÃO E PESQUISA
def ordenar_por_peso(coletas):  # Bubble Sort
    lista = coletas.copy()
    for fim in range(len(lista) - 1, 0, -1):
        for i in range(fim):
            if lista[i]["peso_kg"] > lista[i + 1]["peso_kg"]:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
    return lista


def ordenar_por_codigo(coletas):  # Selection Sort
    lista = coletas.copy()
    for i in range(len(lista) - 1):
        menor = i
        for j in range(i + 1, len(lista)):
            if lista[j]["codigo"] < lista[menor]["codigo"]:
                menor = j
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista


def buscar_codigo(coletas, alvo):  # Pesquisa binária
    lista = ordenar_por_codigo(coletas)
    inicio, fim = 0, len(lista) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        codigo = lista[meio]["codigo"]
        if codigo == alvo:
            return lista[meio]
        if codigo < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None


def buscar_material(coletas, material):  # Pesquisa sequencial
    return [r for r in coletas if r["material"] == material]


# FILA DE PEDIDOS (FIFO)
def adicionar_pedido(fila):
    solicitante = input("Bloco/apartamento: ").strip()
    if not solicitante:
        print("A identificação não pode ficar vazia.")
        return
    fila.append({"solicitante": solicitante, "material": ler_material(),
                 "peso_kg": ler_peso("Peso estimado em kg: ")})
    print(f"Pedido adicionado na posição {len(fila)}.")


def exibir_fila(fila):
    print("\n--- FILA DE PEDIDOS ---")
    if not fila:
        print("Nenhum pedido pendente.")
        return
    for posicao, p in enumerate(fila, 1):
        print(f"{posicao}º - {p['solicitante']} | {p['material']} | {p['peso_kg']:.2f} kg")


def atender_pedido(fila, coletas):
    if not fila:
        print("A fila está vazia.")
        return
    pedido = fila[0]
    print(f"Atendendo {pedido['solicitante']} - {pedido['material']} - {pedido['peso_kg']:.2f} kg")
    registro = {"codigo": novo_codigo(coletas), "data": ler_data("Data (DD/MM/AAAA): "),
                "material": pedido["material"], "peso_kg": pedido["peso_kg"]}
    coletas.append(registro)
    if salvar_coletas(coletas):
        fila.pop(0)
        print("Pedido atendido e salvo!")
    else:
        coletas.pop()
        print("O pedido continua na fila porque não foi possível salvar.")


# RELATÓRIO EM MATRIZ: MÊS x MATERIAL
def gerar_relatorio_matriz(coletas):
    if not coletas:
        print("Não há coletas registradas.")
        return
    while True:
        entrada = input("Ano do relatório (ex.: 2026): ").strip()
        if entrada.isdigit() and 2000 <= int(entrada) <= 2100:
            ano = int(entrada)
            break
        print("Digite um ano válido entre 2000 e 2100.")

    matriz = [[0.0] * len(MATERIAIS) for _ in range(12)]
    for r in coletas:
        _, mes, ano_registro = r["data"].split("/")
        if int(ano_registro) == ano:
            matriz[int(mes) - 1][MATERIAIS.index(r["material"])] += r["peso_kg"]

    cabecalho = f"{'Mês':<6}" + "".join(f" | {m.capitalize():>10}" for m in MATERIAIS) + f" | {'Total':>10}"
    print("\n" + cabecalho + "\n" + "-" * len(cabecalho))
    total_ano = 0.0
    for mes, valores in zip(MESES, matriz):
        total_mes = sum(valores)
        total_ano += total_mes
        print(f"{mes:<6}" + "".join(f" | {v:>10.2f}" for v in valores) + f" | {total_mes:>10.2f}")
    print(f"Total de {ano}: {total_ano:.2f} kg")


# MENU PRINCIPAL
def menu():
    try:
        coletas = carregar_coletas()
    except RuntimeError as erro:
        print(f"ERRO: {erro}\nPrograma encerrado para proteger os dados.")
        return

    fila = []  # A fila é mantida apenas enquanto o programa estiver aberto.
    while True:
        print("\n====== SISTEMA DE COLETA DE RECICLÁVEIS ======")
        print("1. Cadastrar coleta\n2. Listar coletas\n3. Estatísticas")
        print("4. Ordenar por peso\n5. Buscar por código\n6. Buscar por material")
        print("7. Adicionar pedido à fila\n8. Ver/atender fila\n9. Relatório mensal\n0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_coleta(coletas)
        elif opcao == "2":
            listar_coletas(coletas)
        elif opcao == "3":
            calcular_estatisticas(coletas)
        elif opcao == "4":
            listar_coletas(ordenar_por_peso(coletas))
        elif opcao == "5":
            resultado = buscar_codigo(coletas, ler_inteiro("Código para pesquisar: "))
            listar_coletas([resultado] if resultado else [])
        elif opcao == "6":
            listar_coletas(buscar_material(coletas, ler_material()))
        elif opcao == "7":
            adicionar_pedido(fila)
        elif opcao == "8":
            exibir_fila(fila)
            if fila and input("Atender o primeiro pedido? (s/n): ").strip().lower() == "s":
                atender_pedido(fila, coletas)
        elif opcao == "9":
            gerar_relatorio_matriz(coletas)
        elif opcao == "0":
            print("Encerrando. As coletas são salvas automaticamente ao cadastrar.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
