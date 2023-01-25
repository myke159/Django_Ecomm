def Moeda(valor):
    valor = f'{valor:_.2f}'
    valor = valor.replace('.', ',').replace('_', ".")
    return valor

