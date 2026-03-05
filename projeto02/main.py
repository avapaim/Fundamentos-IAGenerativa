from classifier import classificar_mensagem

mensagem_teste = "Quero contratar o plano premium"

temperaturas = [0, 0.5, 1]

for temp in temperaturas:
    print("\n" + "=" * 50)
    print(f"Testando temperatura: {temp}")
    print("=" * 50)

    for i in range(10):
        resultado = classificar_mensagem(mensagem_teste, temperature=temp)
        print(f"Execução {i+1}: {resultado}")
        
