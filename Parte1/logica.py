import random

def punto_a():
    """Imprime los números del 0 al 100. 
    Cuando el numero es par tambien imprime buzz
    Cuando elnumero es multiplo de 5 se imprime bazz en la misma linea."""
    for numero in range(101):
        print(numero, 'buzz' if numero % 2 == 0 else '', 'bazz' if numero % 5 == 0 else '')

def punto_b():
    """Genera una lista de Pokemon de la siguiente forma:
    De 70 nombres seleccionados en ingles el nombre del pokemon subsiguiente comienza con la letra final del nombre anterior"""
    lista_inicial_pkm = '''audino bagon baltoy banette bidoof braviary bronzor carracosta charmeleon cresselia croagunk darmanitan deino emboar emolga exeggcute gabite girafarig gulpin haxorus heatmor heatran ivysaur jellicent jumpluff kangaskhan kricketune landorus ledyba loudred lumineon lunatone machamp magnezone mamoswine nosepass petilil pidgeotto pikachu pinsir poliwrath poochyena porygon2 porygonz registeel relicanth remoraid rufflet sableye scolipede scrafty seaking sealeo silcoon simisear snivy snorlax spoink starly tirtouga trapinch treecko tyrogue vigoroth vulpix wailord wartortle whismur wingull yamask'''
    lista_pkm = lista_inicial_pkm.split(' ')
    lista_final_pkm = []
    # Aleatoriza la lista inicial
    random.shuffle(lista_pkm)
    indice = 0
    while indice < len(lista_pkm):
        if indice > 0:
            if lista_final_pkm[-1][-1] == lista_pkm[indice][0] and lista_pkm[indice] not in lista_final_pkm:
                lista_final_pkm.append(lista_pkm[indice])
                indice = 0
        else:
            lista_final_pkm.append(lista_pkm[indice])
        indice += 1
    print(lista_final_pkm)

def main(opcion):
    if opcion == 'a':
        punto_a()
    else:
        punto_b()

if __name__ == '__main__':
    print('-- Ingrese el punto del ejercicio de logica que desea ver entre a y b (otra opcion termina con la ejecucion del programa)) --')
    opcion = input()
    while opcion in ['a', 'b']:
        main(opcion)
        print('-- Ingrese el punto del ejercicio de logica que desea ver entre a y b (otra opcion termina con la ejecucion del programa)) --')
        opcion = input()
        