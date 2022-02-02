
def generic_model_mutation_process(model, data, id=None, commit=True):
    """Crea y actualiza objetos en base a un model y un id.
    No tiene ningún tipo de restricción.
    Usado para el guardado de modelos en las mutaciones basicas.

    Args:
        model (Django.model):  Model de Django.
        data (dict): Contiene los fields del objeto a creat/actualizar.
        id (int, optional): Para buscar el objeto a actualizar. Por defecto tiene el valor None.
        commit (bool, optional): Indica si se debe guardar el objeto. Por defecto tiene el valor True.

    Returns:
        Django.model: instancia del modelo entregado
    """
    
    if id:
        item = model.objects.get(id=id)
        try:
            del data['id']
        except KeyError:
            # Sacar el id por si envían el data tal cual llega.
            pass

        for field, value in data.items():
            setattr(item, field, value)

    else:
        item = model(**data)
        # TODO: Verificaciones, auto_ids, hashing, asserts, etc.

    if commit:
        item.save()

    return item
